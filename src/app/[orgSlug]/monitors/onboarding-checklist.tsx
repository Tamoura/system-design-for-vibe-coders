import Link from 'next/link';
import { can } from '@/core/permissions';
import type { Role } from '@/core/roles';
import type { OnboardingState } from '@/core/onboarding';

/**
 * Lesson 6.1 (🟡): the "Getting started" checklist, drawn from the milestones
 * stored on the org (src/lib/onboarding.ts). Every member sees the org's
 * progress, whenever they joined; once every step is done it disappears for
 * good, so a second admin who joins later never sees it. Each call to action
 * is shown only to roles that may do it (the pages check again).
 */
export function OnboardingChecklist({ orgSlug, role, state }: { orgSlug: string; role: Role; state: OnboardingState }) {
  if (state.complete) return null;
  return (
    <section id="getting-started" className="card grid checklist" aria-labelledby="getting-started-title" data-testid="onboarding-checklist">
      <div className="row">
        <h2 id="getting-started-title" className="h2">Getting started</h2>
        <span className="muted">{state.done} of {state.total} done</span>
        <progress max={state.total} value={state.done} aria-label="Onboarding progress" />
      </div>
      <ol className="checklist-steps">
        {state.steps.map((s) => (
          <li key={s.milestone} className={s.reachedAt ? 'done' : undefined} data-milestone={s.milestone} data-done={Boolean(s.reachedAt)}>
            {/* Not colour alone: the mark and the words say it too. */}
            <span className="check" aria-hidden="true">{s.reachedAt ? '✓' : '○'}</span>
            <div>
              <strong>{s.title}</strong>
              <span className="sr-only">{s.reachedAt ? ' (done)' : ' (to do)'}</span>
              <div className="muted">{s.hint}</div>
            </div>
            {!s.reachedAt && s.path && s.permission && can(role, s.permission) && (
              <Link href={`/${orgSlug}${s.path}`} className="btn secondary">Do it</Link>
            )}
          </li>
        ))}
      </ol>
    </section>
  );
}
