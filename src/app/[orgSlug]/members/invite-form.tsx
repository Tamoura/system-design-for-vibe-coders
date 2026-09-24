'use client';

import { useActionState } from 'react';
import type { Role } from '@/core/roles';
import { inviteAction, type InviteFormState } from './actions';

/** `roles` holds only the roles this user may grant (canGrantRole), computed on the server. */
export function InviteForm({ orgSlug, roles }: { orgSlug: string; roles: Role[] }) {
  const [state, action, pending] = useActionState<InviteFormState, FormData>(inviteAction.bind(null, orgSlug), {});
  return (
    <form action={action} className="card grid">
      <strong>Invite a teammate</strong>
      <div className="row">
        <input name="email" type="email" placeholder="sam@acme.com" aria-label="Email" required style={{ flex: 1, minWidth: 220 }} />
        <select name="role" aria-label="Role" defaultValue={roles.includes('member') ? 'member' : roles[roles.length - 1]}>
          {roles.map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
        <button className="btn" disabled={pending}>{pending ? 'Sending…' : 'Send invitation'}</button>
      </div>
      {state.error && <span className="error">{state.error}</span>}
      {state.sent && <span className="muted">{state.sent}</span>}
    </form>
  );
}
