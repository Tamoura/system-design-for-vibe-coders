/*
 * Lesson 7.2 (🟢): browser errors. Next.js runs this file in the browser
 * before the app starts. With NEXT_PUBLIC_SENTRY_DSN set at BUILD time,
 * uncaught errors and unhandled rejections go to Sentry (or GlitchTip),
 * tagged with the release (NEXT_PUBLIC_APP_RELEASE, the git SHA). Without it,
 * nothing is loaded at all.
 *
 * Readable stack traces need the source maps: CI builds with
 * SENTRY_AUTH_TOKEN and uploads them (see .github/workflows/ci.yml), so
 * "a.b is not a function at main.8f3a.js:1:48213" reads as the real file.
 */
const dsn = process.env.NEXT_PUBLIC_SENTRY_DSN;

if (dsn) {
  import('@sentry/browser').then((Sentry) => {
    Sentry.init({
      dsn,
      release: process.env.NEXT_PUBLIC_APP_RELEASE,
      environment: process.env.NEXT_PUBLIC_APP_ENV,
      // Errors only: no session replay, no tracing. (No personal data is sent unless you opt in.)
    });
  });
}

export {};
