import { PgBoss, type ConstructorOptions } from 'pg-boss';
import { QUEUES } from './queues';

/*
 * Lesson 5.1: set up the queue's tables. `npm run db:migrate` calls this after
 * Beacon's own migrations, and the tests call it on their in-memory Postgres.
 *
 * pg-boss keeps its tables in their own schema (`pgboss`) and migrates them
 * itself when its version changes, so they are not in drizzle/. What Beacon
 * adds on top:
 *
 *  1. one row per queue in QUEUES (./queues.ts), with its retry settings;
 *  2. privileges for `beacon_app`, the role tenant queries run as (lesson 2.4).
 *     A job enqueued inside withOrg() is an INSERT in that transaction, made by
 *     beacon_app, so it may add jobs, read the queue settings, and read back the
 *     id of the job it added. Nothing else: it cannot read other jobs' payloads,
 *     change or delete jobs. Only the worker, connecting as the owner, can.
 */
export const QUEUE_SCHEMA = 'pgboss';
const APP_ROLE = 'beacon_app';

export async function installQueues(connection: Pick<ConstructorOptions, 'connectionString' | 'max' | 'db' | 'backend'>): Promise<void> {
  // migrate: true (the default) creates or upgrades pg-boss's schema. No
  // maintenance and no cron in this short-lived instance.
  const boss = new PgBoss({ ...connection, schema: QUEUE_SCHEMA, supervise: false, schedule: false });
  boss.on('error', (err) => console.error('[queue]', err));
  await boss.start();
  for (const [name, options] of Object.entries(QUEUES)) {
    if (await boss.getQueue(name)) {
      // Retry settings may change between releases; the policy of an existing queue cannot.
      const { policy: _policy, ...changeable } = options as typeof options & { policy?: string };
      await boss.updateQueue(name, changeable);
    } else {
      await boss.createQueue(name, options);
    }
  }
  const db = boss.getDb();
  const { rows } = await db.executeSql(`select distinct table_name from ${QUEUE_SCHEMA}.queue`);
  const grants = [
    `GRANT USAGE ON SCHEMA ${QUEUE_SCHEMA} TO ${APP_ROLE}`,
    `GRANT SELECT ON ${QUEUE_SCHEMA}.queue TO ${APP_ROLE}`,
    ...rows.map((r: { table_name: string }) => `GRANT INSERT, SELECT (id) ON ${QUEUE_SCHEMA}.${r.table_name} TO ${APP_ROLE}`),
  ];
  for (const statement of grants) await db.executeSql(statement);
  await boss.stop({ graceful: false });
}
