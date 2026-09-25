/**
 * Lesson 7.1: Beacon's staff, from the command line. The first superadmin
 * has to come from somewhere: a shell on a server, not a button anyone could
 * find. After that, superadmins manage staff at /internal/staff. Every change
 * is a platform audit event, named after the operating-system user.
 *
 *   npm run staff                                         list staff and their roles
 *   npm run staff -- add ana@beacon.test support "Joined the support team, HR-812"
 *   npm run staff -- add ana@beacon.test superadmin "…"   (roles: support, billing, engineer, superadmin)
 *   npm run staff -- remove ana@beacon.test "Left the company"
 *
 * The person signs up (and verifies their email) first. It replaces Module 6's
 * BEACON_STAFF_EMAILS: move those addresses here once.
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import { eq } from 'drizzle-orm';
import { db, schema, sql } from '../src/db';
import { isStaffRole, STAFF_ROLES } from '../src/core/staff';
import { cliAuditSource } from '../src/lib/audit';
import { grantStaffRole, listStaff, revokeStaff } from '../src/lib/admin/staff';
import { InvalidRequestError } from '../src/lib/errors';

const [command, email, ...rest] = process.argv.slice(2);
const source = cliAuditSource('npm run staff');

try {
  switch (command) {
    case undefined:
    case 'list':
      for (const s of await listStaff()) console.log(`${s.role.padEnd(11)} ${s.email}  (since ${s.since.toISOString().slice(0, 10)})`);
      break;
    case 'add': {
      const [role, ...why] = rest;
      if (!email || !isStaffRole(role)) throw new InvalidRequestError('usage', `usage: npm run staff -- add <email> <${STAFF_ROLES.join('|')}> "<reason>"`);
      await grantStaffRole({ email, role, reason: why.join(' ') || 'granted from the command line' }, source);
      console.log(`✓ ${email} is now staff: ${role}`);
      break;
    }
    case 'remove': {
      const [user] = email ? await db.select({ id: schema.staffUsers.id }).from(schema.staffUsers).innerJoin(schema.users, eq(schema.users.id, schema.staffUsers.userId)).where(eq(schema.users.email, email.toLowerCase())) : [];
      if (!user) throw new InvalidRequestError('not_staff', `${email ?? '(no email)'} is not staff.`);
      await revokeStaff(user.id, rest.join(' ') || 'removed from the command line', source);
      console.log(`✓ ${email} is no longer staff`);
      break;
    }
    default:
      throw new InvalidRequestError('usage', `Unknown command "${command}". Commands: list, add, remove.`);
  }
} catch (err) {
  if (!(err instanceof InvalidRequestError)) throw err;
  console.error(err.message);
  process.exitCode = 1;
} finally {
  await sql.end();
}
