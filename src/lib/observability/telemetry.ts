import { context, metrics, propagation, trace, SpanKind, SpanStatusCode, type Attributes, type Context, type Span } from '@opentelemetry/api';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { resourceFromAttributes } from '@opentelemetry/resources';
import { ConsoleMetricExporter, MeterProvider, PeriodicExportingMetricReader, type IMetricReader } from '@opentelemetry/sdk-metrics';
import { BatchSpanProcessor, ConsoleSpanExporter, NodeTracerProvider, SimpleSpanProcessor, type SpanExporter } from '@opentelemetry/sdk-trace-node';
import { ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION } from '@opentelemetry/semantic-conventions';

/*
 * Lesson 7.2 (🟡): OpenTelemetry, the vendor-neutral way to emit traces and
 * metrics. Beacon instruments itself once, with the OTel SDK; WHERE the data
 * goes is configuration:
 *
 *   OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318   an OTel Collector (docker-compose.observability.yml
 *                                                       forwards to Tempo + Prometheus + Grafana; SigNoz,
 *                                                       Honeycomb or Datadog take the same OTLP)
 *   OTEL_EXPORTER=console                               print spans and metrics (debugging)
 *   neither                                             nothing is exported, but trace ids are still
 *                                                       created and propagated (logs keep their traceId)
 *
 * What is instrumented, by hand, where Beacon's interesting work is:
 *   - every API request (src/lib/observability/http.ts): a SERVER span + RED metrics
 *   - enqueue (src/lib/queue): a PRODUCER span, and the trace context copied INTO the
 *     job's payload, because "across a queue it does not happen by itself"
 *   - every job in the worker: a CONSUMER span whose parent is the enqueuing span,
 *     so one trace shows request → enqueue → job → check
 *   - checks: `checks_executed_total` and the `check_lag_seconds` histogram
 *
 * Auto-instrumentation (HTTP, pg) is one package away
 * (@opentelemetry/auto-instrumentations-node); it is left out to keep the
 * course repo's dependency list short and the spans easy to read.
 */

export type TelemetryOptions = {
  /** Tests pass an in-memory exporter/reader. */
  spanExporter?: SpanExporter;
  metricReader?: IMetricReader;
};

const g = globalThis as unknown as { beaconTelemetry?: { service: string; tracerProvider: NodeTracerProvider; meterProvider: MeterProvider } };

export function initTelemetry(service: string, options: TelemetryOptions = {}) {
  if (g.beaconTelemetry) return g.beaconTelemetry;
  const resource = resourceFromAttributes({
    [ATTR_SERVICE_NAME]: service,
    [ATTR_SERVICE_VERSION]: process.env.APP_RELEASE ?? 'dev',
    'deployment.environment.name': process.env.APP_ENV ?? process.env.NODE_ENV ?? 'development',
  });

  const exporterKind = process.env.OTEL_EXPORTER_OTLP_ENDPOINT ? 'otlp' : process.env.OTEL_EXPORTER === 'console' ? 'console' : null;
  const spanExporter = options.spanExporter ?? (exporterKind === 'otlp' ? new OTLPTraceExporter() : exporterKind === 'console' ? new ConsoleSpanExporter() : null);
  const tracerProvider = new NodeTracerProvider({
    resource,
    spanProcessors: spanExporter ? [options.spanExporter ? new SimpleSpanProcessor(spanExporter) : new BatchSpanProcessor(spanExporter)] : [],
  });
  // Sets the global tracer, the AsyncLocalStorage context manager and the
  // W3C `traceparent` propagator.
  tracerProvider.register();

  const metricReader =
    options.metricReader ??
    (exporterKind
      ? new PeriodicExportingMetricReader({
          exporter: exporterKind === 'otlp' ? new OTLPMetricExporter() : new ConsoleMetricExporter(),
          exportIntervalMillis: Number(process.env.OTEL_METRIC_EXPORT_INTERVAL ?? 15_000),
        })
      : null);
  const meterProvider = new MeterProvider({ resource, readers: metricReader ? [metricReader] : [] });
  metrics.setGlobalMeterProvider(meterProvider);

  g.beaconTelemetry = { service, tracerProvider, meterProvider };
  return g.beaconTelemetry;
}

/** Flush what is buffered (the worker calls this on SIGTERM). */
export async function shutdownTelemetry(): Promise<void> {
  const t = g.beaconTelemetry;
  if (!t) return;
  await Promise.allSettled([t.tracerProvider.forceFlush(), t.meterProvider.forceFlush()]);
}

export const tracer = () => trace.getTracer('beacon');

/**
 * Run `fn` inside a span. The span ends when `fn` settles; an exception marks
 * it as an error (and is rethrown).
 */
export async function withSpan<T>(name: string, options: { kind?: SpanKind; attributes?: Attributes; parent?: Context }, fn: (span: Span) => Promise<T>): Promise<T> {
  return tracer().startActiveSpan(name, { kind: options.kind ?? SpanKind.INTERNAL, attributes: options.attributes }, options.parent ?? context.active(), async (span) => {
    try {
      return await fn(span);
    } catch (err) {
      span.recordException(err as Error);
      span.setStatus({ code: SpanStatusCode.ERROR, message: (err as Error).message });
      throw err;
    } finally {
      span.end();
    }
  });
}

/*
 * Trace context in a job payload (lesson 7.2 🟡: "put the trace context into
 * the job data and restore it in the worker, or your trace ends at the queue").
 * `traceparent` is the W3C header's value: version-traceid-spanid-flags.
 */
export type TraceCarrier = { traceparent?: string; tracestate?: string };

export function injectTraceContext(): TraceCarrier {
  const carrier: TraceCarrier = {};
  propagation.inject(context.active(), carrier);
  return carrier;
}

export function extractTraceContext(carrier: TraceCarrier | undefined): Context {
  return carrier ? propagation.extract(context.active(), carrier) : context.active();
}

export { SpanKind, SpanStatusCode };
