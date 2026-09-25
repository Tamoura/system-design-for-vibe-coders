import { listFlagsForAdmin } from '@/lib/flags/store';
import { requireStaff } from '@/lib/staff';
import { deleteStaleFlagAction, removeOverrideAction, setMasterSwitchAction } from './actions';
import { OverrideForm, RolloutForm } from './flag-forms';

export const dynamic = 'force-dynamic';

const KIND_HELP = {
  release: 'Release flag: temporary, delete it once rolled out',
  ops: 'Ops kill switch: long-lived by design',
  permission: 'Permission flag: a beta for chosen organizations',
  experiment: 'Experiment',
} as const;

/**
 * Lesson 6.3: the flag dashboard. One card per flag declared in
 * src/core/flags.ts: what it is, who owns it, when it must be gone, and its
 * rules: the master switch (the kill switch), the rollout percentage (by a
 * stable hash of flag + org, so raising it only adds orgs) and per-org overrides.
 * The same operations exist on the command line: `npm run flags`.
 */
export default async function FlagsPage() {
  await requireStaff();
  const flags = await listFlagsForAdmin();
  return (
    <section className="grid">
      <h1>Feature flags</h1>
      <p className="muted" style={{ margin: 0 }}>
        Evaluated on the server, per organization. Every process reloads the rules every {Number(process.env.FLAGS_REFRESH_SECONDS ?? 15)} seconds.
        Plans and limits are not flags: they live in the entitlements (lesson 3.2).
      </p>
      {flags.map((f) => {
        const on = f.rule?.enabled ?? false;
        return (
          <article key={f.key} className="card grid" data-flag={f.key} aria-labelledby={`flag-${f.key}`}>
            <div className="row">
              <h2 id={`flag-${f.key}`} className="h2"><code>{f.key}</code></h2>
              {f.definition && <span className="badge">{KIND_HELP[f.definition.kind]}</span>}
              {f.expired && <span className="badge status-down">past its expiry: remove it</span>}
            </div>
            {f.definition ? (
              <>
                <p style={{ margin: 0 }}>{f.definition.description}</p>
                <div className="muted">
                  Owner: {f.definition.owner} · Expires: {f.definition.expires ?? 'never (ops flag)'} · Safe default: {f.definition.defaultValue ? 'on' : 'off'}
                </div>
                <div className="muted">Cleanup: {f.definition.cleanup}</div>
              </>
            ) : (
              <div className="row error">
                Not declared in the code any more. Delete it, and never reuse the name.
                <form action={deleteStaleFlagAction.bind(null, f.key)}><button className="link-btn">Delete</button></form>
              </div>
            )}
            <div className="row" data-testid="flag-state">
              <strong>{!f.rule ? 'No rule yet: safe default for everyone' : on ? `On for ${f.rule.rolloutPercent}% of organizations` : 'Switched OFF for everyone'}</strong>
              {f.definition && (on ? (
                <form action={setMasterSwitchAction.bind(null, f.key, false)}>
                  <button className="btn secondary" data-testid="kill-switch">Kill switch: turn off for everyone</button>
                </form>
              ) : (
                <form action={setMasterSwitchAction.bind(null, f.key, true)}>
                  <button className="btn secondary" data-testid="switch-on">Switch on (rollout and overrides apply)</button>
                </form>
              ))}
            </div>
            {f.definition && <RolloutForm flagKey={f.key} percent={f.rule?.rolloutPercent ?? 0} />}
            {f.overrides.length > 0 && (
              <table>
                <caption className="sr-only">Overrides for {f.key}</caption>
                <thead><tr><th scope="col">Organization</th><th scope="col">Value</th><th scope="col"><span className="sr-only">Actions</span></th></tr></thead>
                <tbody>
                  {f.overrides.map((o) => (
                    <tr key={o.orgSlug}>
                      <td>{o.orgName} <span className="muted">({o.orgSlug})</span></td>
                      <td>{o.enabled ? 'on' : 'off'}</td>
                      <td>
                        <form action={removeOverrideAction.bind(null, f.key, o.orgSlug)}>
                          <button className="link-btn">Remove</button>
                        </form>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            {f.definition && <OverrideForm flagKey={f.key} />}
          </article>
        );
      })}
    </section>
  );
}
