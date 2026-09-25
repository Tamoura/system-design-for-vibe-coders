import Link from 'next/link';
import { searchCustomers } from '@/lib/admin/customers';
import { requireStaff } from '@/lib/staff';

export const dynamic = 'force-dynamic';

/**
 * Lesson 7.1 (🟢): "find a customer". One box: part of an org name, part of
 * a member's email ("ana@", "@acme.test"), a Stripe customer id (cus_…) or
 * an org id. A GET form, so a search is a link support can paste in a ticket.
 */
export default async function CustomersPage({ searchParams }: { searchParams: Promise<{ q?: string }> }) {
  await requireStaff('customers.read');
  const q = ((await searchParams).q ?? '').trim();
  const started = performance.now();
  const hits = q ? await searchCustomers(q) : [];
  const ms = Math.round(performance.now() - started);
  return (
    <section className="grid">
      <h1>Find a customer</h1>
      <form className="row" role="search" action="/internal">
        <label htmlFor="q" className="sr-only">Search</label>
        <input id="q" name="q" defaultValue={q} placeholder="Org name, member email, cus_… or org id" style={{ minWidth: '28rem' }} autoFocus />
        <button className="btn">Search</button>
      </form>
      {q && (
        <div className="card">
          <p className="muted" style={{ marginTop: 0 }}>{hits.length} organization(s) for “{q}” in {ms} ms</p>
          {hits.length > 0 && (
            <table data-testid="customer-results">
              <thead>
                <tr><th scope="col">Organization</th><th scope="col">Plan</th><th scope="col">Members</th><th scope="col">Matched on</th></tr>
              </thead>
              <tbody>
                {hits.map((h) => (
                  <tr key={h.id}>
                    <td><Link href={`/internal/orgs/${h.id}`}>{h.name}</Link> <span className="muted">/{h.slug}</span></td>
                    <td>{h.plan}</td>
                    <td>{h.members}</td>
                    <td className="muted">{h.matched}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </section>
  );
}
