import { STAFF_PERMISSIONS, STAFF_ROLES } from '@/core/staff';
import { listStaff } from '@/lib/admin/staff';
import { requireStaff } from '@/lib/staff';

export const dynamic = 'force-dynamic';

/**
 * Lesson 7.1: who has back-office access, with which role. Superadmins only.
 * The first superadmin comes from `npm run staff -- add … superadmin` on a
 * server; after that, here. Both write a platform audit event with a reason.
 */
export default async function StaffPage({ searchParams }: { searchParams: Promise<{ done?: string; error?: string }> }) {
  const me = await requireStaff('staff.manage');
  const flash = await searchParams;
  const staff = await listStaff();
  return (
    <section className="grid">
      <h1>Staff</h1>
      {flash.done && <p className="card" role="status">✓ {flash.done}</p>}
      {flash.error && <p className="card error" role="alert">{flash.error}</p>}
      <div className="card">
        <table data-testid="staff-list">
          <thead>
            <tr><th scope="col">Email</th><th scope="col">Role</th><th scope="col">Since</th><th scope="col"></th></tr>
          </thead>
          <tbody>
            {staff.map((s) => (
              <tr key={s.staffId}>
                <td>{s.email}</td>
                <td>{s.role}</td>
                <td>{s.since.toISOString().slice(0, 10)}</td>
                <td>
                  {s.staffId !== me.staffId && (
                    <details>
                      <summary>Remove</summary>
                      <form method="post" action={`/api/internal/staff/${s.staffId}`} className="row">
                        <input type="hidden" name="back" value="/internal/staff" />
                        <input name="reason" required minLength={8} placeholder="Reason" />
                        <button className="btn secondary">Remove</button>
                      </form>
                    </details>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <form method="post" action="/api/internal/staff" className="card grid">
        <h2>Grant or change a role</h2>
        <input type="hidden" name="back" value="/internal/staff" />
        <label className="row">Email <input name="email" type="email" required placeholder="someone@beacon.test" /></label>
        <label className="row">
          Role
          <select name="role">{STAFF_ROLES.map((r) => <option key={r} value={r}>{r}</option>)}</select>
        </label>
        <label className="row">Reason <input name="reason" required minLength={8} placeholder="e.g. joined the support team, HR-812" style={{ minWidth: '24rem' }} /></label>
        <div><button className="btn">Save</button></div>
      </form>
      <div className="card">
        <h2>What each role can do</h2>
        <ul>
          {STAFF_ROLES.map((r) => <li key={r}><strong>{r}</strong>: {STAFF_PERMISSIONS[r].join(', ')}</li>)}
        </ul>
      </div>
    </section>
  );
}
