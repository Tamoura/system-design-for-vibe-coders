import { sql, type SQL } from 'drizzle-orm';
import { db } from '@/db';

/**
 * Lesson 2.4: the one door to tenant data.
 *
 * Every query on a table that carries organization_id (monitors,
 * check_results, incidents, and later incident_updates and files) runs inside
 * `withOrg(orgId, (tx) => …)`. It opens a transaction and sets two things that
 * last only until that transaction ends:
 *
 *   app.current_org = orgId      read by the row-level security policies
 *                                (drizzle/0007_row_level_security.sql)
 *   role            = beacon_app a role that owns nothing and has no
 *                                BYPASSRLS, so the policies apply to it
 *
 * The code inside still writes `where organization_id = …` (lesson 1.2's
 * scoped data access). Row-level security is defence in depth: if one of
 * those clauses goes missing, Postgres adds it anyway, and a row written with
 * another org's id is refused ("new row violates row-level security policy").
 *
 * Why transaction-local (`set_config(…, true)`) and not `SET`: behind a pooler
 * such as PgBouncer in transaction mode, the next transaction on this server
 * connection may belong to another request. A session-level SET would leak
 * this org into it; a transaction-local setting ends with COMMIT.
 *
 * Rules: use only `tx` inside the callback (the global `db` is a different
 * connection without the tenant context), and do no network calls (email,
 * S3, Stripe) inside it: a transaction holds its connection until it ends.
 */
export const APP_DB_ROLE = 'beacon_app';

export type TenantTx = Parameters<Parameters<typeof db.transaction>[0]>[0];

export async function withOrg<T>(orgId: string, fn: (tx: TenantTx) => Promise<T>): Promise<T> {
  return db.transaction(async (tx) => {
    await tx.execute(sql`select set_config('app.current_org', ${orgId}, true), set_config('role', ${APP_DB_ROLE}, true)`);
    return fn(tx);
  });
}

/**
 * The rows of a hand-written SQL query run with `tx.execute()`. Drizzle hands
 * back the driver's own result: an array from postgres.js (the app), an
 * object with `rows` from PGlite (the tests). Column names are as in SQL.
 */
export async function selectRows<T>(tx: TenantTx, query: SQL): Promise<T[]> {
  const result = (await tx.execute(query)) as unknown as T[] | { rows: T[] };
  return Array.isArray(result) ? result : result.rows;
}
