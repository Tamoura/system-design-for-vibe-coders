import { metrics, type Counter, type Histogram } from '@opentelemetry/api';

/*
 * Lesson 7.2 (🟡): what Beacon measures.
 *
 * RED for everything request-driven (the lesson's checklist):
 *   Rate      http_server_requests_total{method, route, status_class}
 *   Errors    the same counter, status_class="5xx"; jobs_total{queue, outcome="failed"}
 *   Duration  http_server_duration_seconds{method, route}, job_duration_seconds{queue} (histograms:
 *             dashboards show p50/p95/p99, never an average)
 *
 * And Beacon's own health signal, the one no HTTP dashboard shows:
 *   checks_executed_total{region, result}   checks that actually ran
 *   check_lag_seconds{region}               how late a check ran after its scheduled slot
 * If the scheduler silently skips monitors, or workers fall behind, customers
 * get late alerts while every endpoint looks healthy. These two catch it.
 *
 * CARDINALITY: labels are small closed sets (method, a route TEMPLATE, a
 * status class, a queue name, a region). Never an org id, a user id or a URL:
 * with 50,000 orgs that is 50,000 time series per metric, and the metrics
 * server falls over. Per-tenant questions are answered from logs and traces.
 */

type Instruments = {
  httpRequests: Counter;
  httpDuration: Histogram;
  jobs: Counter;
  jobDuration: Histogram;
  checksExecuted: Counter;
  checkLag: Histogram;
};

let cached: { provider: unknown; instruments: Instruments } | null = null;

/** Created lazily, and again if the meter provider changes (initTelemetry runs after some modules load). */
function instruments(): Instruments {
  const provider = metrics.getMeterProvider();
  if (cached && cached.provider === provider) return cached.instruments;
  const meter = metrics.getMeter('beacon');
  const seconds = (boundaries: number[]) => ({ unit: 's', advice: { explicitBucketBoundaries: boundaries } });
  const made: Instruments = {
    httpRequests: meter.createCounter('http_server_requests_total', { description: 'HTTP requests handled by the API, by route template and status class' }),
    httpDuration: meter.createHistogram('http_server_duration_seconds', { description: 'API request duration', ...seconds([0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]) }),
    jobs: meter.createCounter('jobs_total', { description: 'Queue jobs run by the worker, by queue and outcome' }),
    jobDuration: meter.createHistogram('job_duration_seconds', { description: 'How long a job ran', ...seconds([0.01, 0.05, 0.1, 0.5, 1, 2.5, 5, 10, 30, 60]) }),
    checksExecuted: meter.createCounter('checks_executed_total', { description: 'Uptime checks that ran, by region and result' }),
    checkLag: meter.createHistogram('check_lag_seconds', { description: 'Seconds between a check slot and the check actually running', ...seconds([0.5, 1, 2, 5, 10, 15, 30, 60, 120, 300]) }),
  };
  cached = { provider, instruments: made };
  return made;
}

/** The checker's region. Beacon runs one today; the label is there for the multi-region checkers of lesson 7.4. */
export const checkRegion = () => process.env.CHECK_REGION ?? 'local';

export function recordHttpRequest(method: string, route: string, status: number, seconds: number) {
  const i = instruments();
  i.httpRequests.add(1, { method, route, status_class: `${Math.floor(status / 100)}xx` });
  i.httpDuration.record(seconds, { method, route });
}

export function recordJob(queue: string, outcome: 'completed' | 'failed', seconds: number) {
  const i = instruments();
  i.jobs.add(1, { queue, outcome });
  i.jobDuration.record(seconds, { queue });
}

export function recordCheck(result: 'up' | 'down', lagSeconds: number | null) {
  const i = instruments();
  const region = checkRegion();
  i.checksExecuted.add(1, { region, result });
  if (lagSeconds !== null) i.checkLag.record(Math.max(0, lagSeconds), { region });
}

/**
 * A route TEMPLATE for the `route` label: `/api/orgs/acme/monitors/9b2c…` →
 * `/api/orgs/:org/monitors/:id`. Slugs, uuids and prefixed ids (mon_…) are
 * replaced, so the label has one value per endpoint, not one per org.
 */
export function routeTemplate(pathname: string): string {
  const parts = pathname.split('/');
  return parts
    .map((part, i) => {
      if (i > 0 && parts[i - 1] === 'orgs' && parts[i - 2] === 'api') return ':org';
      if (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(part)) return ':id';
      if (/^[a-z]{2,5}_[A-Za-z0-9]{6,}$/.test(part)) return ':id';
      return part;
    })
    .join('/');
}
