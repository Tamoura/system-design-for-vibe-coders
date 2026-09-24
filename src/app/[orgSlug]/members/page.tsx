import { can, canGrantRole, roleChangeRefusal } from '@/core/permissions';
import { ROLES } from '@/core/roles';
import { forPage, requirePermission } from '@/lib/access';
import { listOpenInvitations } from '@/lib/invitations';
import { listMembers } from '@/lib/members';
import { changeRoleAction, resendInvitationAction, revokeInvitationAction } from './actions';
import { InviteForm } from './invite-form';

export const dynamic = 'force-dynamic';

export default async function MembersPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  // Every role may see who is in the org; changing it needs "member.manage".
  const ctx = await forPage(requirePermission(orgSlug, 'member.read'), `/${orgSlug}/members`);
  const members = await listMembers(ctx);
  const manage = can(ctx.role, 'member.manage');
  const invitations = manage ? await listOpenInvitations(ctx) : [];
  const grantable = ROLES.filter((r) => canGrantRole(ctx.role, r));
  return (
    <section className="grid">
      <h1 style={{ margin: 0 }}>Members</h1>
      <div className="card">
        <table>
          <tbody>
            {members.map((m) => {
              // Only offer the role changes the server would accept.
              const options = ROLES.filter((r) => r !== m.role && !roleChangeRefusal(ctx, m, r));
              return (
                <tr key={m.userId}>
                  <td><strong>{m.name}</strong>{m.userId === ctx.userId && <span className="muted"> (you)</span>}</td>
                  <td className="muted">{m.email}</td>
                  <td data-role={m.email}>{m.role}</td>
                  <td>
                    {options.length > 0 && (
                      <form action={changeRoleAction.bind(null, ctx.orgSlug, m.userId)} className="row">
                        <select name="role" aria-label={`New role for ${m.email}`} defaultValue={options[0]}>
                          {options.map((r) => <option key={r} value={r}>{r}</option>)}
                        </select>
                        <button className="link-btn">Change role</button>
                      </form>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {manage && (
        <>
          <InviteForm orgSlug={ctx.orgSlug} roles={grantable} />
          {invitations.length > 0 && (
            <div className="card grid">
              <strong>Open invitations</strong>
              <table>
                <tbody>
                  {invitations.map((i) => (
                    <tr key={i.id}>
                      <td>{i.email}</td>
                      <td>{i.role}</td>
                      <td className={i.state === 'expired' ? 'error' : 'muted'}>
                        {i.state === 'expired' ? 'expired' : `expires ${i.expiresAt.toISOString().slice(0, 10)}`}
                      </td>
                      <td className="row">
                        <form action={resendInvitationAction.bind(null, ctx.orgSlug, i.id)}><button className="link-btn">Resend</button></form>
                        <form action={revokeInvitationAction.bind(null, ctx.orgSlug, i.id)}><button className="link-btn">Revoke</button></form>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </section>
  );
}
