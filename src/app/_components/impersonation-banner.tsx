import type { ImpersonationInfo } from '@/lib/impersonation';

/**
 * Lesson 7.1: the unmissable banner. On every page of the customer app while
 * Beacon staff view it: whose account, read-only, until when, and a way out.
 * It protects the staff member as much as the customer: nobody forgets they
 * are "being Ana" and starts clicking.
 */
export function ImpersonationBanner({ info, viewing }: { info: ImpersonationInfo; viewing: string }) {
  const minutes = Math.max(0, Math.ceil((info.expiresAt.getTime() - Date.now()) / 60_000));
  return (
    <div className="impersonation-banner" role="alert" data-testid="impersonation-banner">
      <span>
        <strong>Viewing as {viewing}</strong> · {info.readOnly ? 'read-only' : 'can make changes'} · ends in {minutes} min (at{' '}
        {info.expiresAt.toISOString().slice(11, 16)} UTC) · staff: {info.staffEmail} · recorded in this organization’s audit log
      </span>
      <form method="post" action="/api/impersonation/exit">
        <button className="btn secondary" data-testid="impersonation-exit">Exit</button>
      </form>
    </div>
  );
}
