# syntax=docker/dockerfile:1
#
# Lesson 7.4: ONE image for Beacon, built once per commit, tagged with the git
# SHA, and promoted unchanged from staging to production. The same image runs
# every process; only the command differs:
#
#   web      (default)                    node_modules/.bin/next start
#   worker   node dist/scripts/worker.mjs the job queues (lesson 5.1)
#   migrate  node dist/scripts/migrate.mjs the RELEASE step, before a deploy (lesson 7.4)
#
# Multi-stage: build tools and dev dependencies stay in the build stages; the
# final image has production dependencies, the build output, and no .env file
# (configuration comes from the environment at runtime, twelve-factor).
#
#   docker build --build-arg GIT_SHA=$(git rev-parse HEAD) -t beacon:$(git rev-parse --short HEAD) .

# The base image, pinned to a tagged version (hadolint DL3006). To change Node
# or the distribution, edit this one line; every stage below builds FROM base.
FROM node:22-bookworm-slim AS base

# 1. Every dependency, for building. Cached until package-lock.json changes.
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

# 2. Production dependencies only: what the final image gets. Same base image
#    as the runtime, so native modules (argon2, sharp) match its libc.
FROM base AS prod-deps
WORKDIR /app
COPY package.json package-lock.json ./
# `npm ci --omit=dev` still keeps dev tools that a production package lists as an *optional peer*
# (better-auth does, for drizzle-kit and vitest), plus everything they depend on. The script walks the
# lockfile from our own dependencies and deletes the rest: code that isn't in the image can't break
# or be exploited in production.
COPY scripts/prune-prod-deps.mjs ./scripts/
RUN npm ci --omit=dev --no-audit --no-fund && npm cache clean --force \
 && node scripts/prune-prod-deps.mjs

# 3. The build: Next.js, then the worker and CLIs bundled to plain JavaScript
#    (tsx is a dev dependency and is not in the final image).
FROM base AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Public values are baked into the browser bundle at BUILD time (lesson 6.2, 7.2).
ARG GIT_SHA=unknown
ARG NEXT_PUBLIC_SENTRY_DSN=
ARG NEXT_PUBLIC_PLAUSIBLE_DOMAIN=
ARG SENTRY_ORG=
ARG SENTRY_PROJECT=
ENV NEXT_TELEMETRY_DISABLED=1 \
    NEXT_PUBLIC_APP_RELEASE=${GIT_SHA} \
    NEXT_PUBLIC_SENTRY_DSN=${NEXT_PUBLIC_SENTRY_DSN} \
    NEXT_PUBLIC_PLAUSIBLE_DOMAIN=${NEXT_PUBLIC_PLAUSIBLE_DOMAIN} \
    SOURCE_MAPS=1
# Lesson 7.2: browser source maps are built, uploaded to Sentry for this release when the
# (optional) build secret is given, then DELETED: they never ship in the image or to browsers.
RUN --mount=type=secret,id=sentry_auth_token,required=false \
    npm run build && npm run build:scripts && sh scripts/sentry-sourcemaps.sh

# 4. The runtime image.
FROM base AS runtime
WORKDIR /app
ARG GIT_SHA=unknown
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    APP_RELEASE=${GIT_SHA} \
    PORT=3000 \
    HOSTNAME=0.0.0.0 \
    STORAGE_LOCAL_DIR=/app/.storage
LABEL org.opencontainers.image.source="https://github.com/Tamoura/system-design-for-vibe-coders" \
      org.opencontainers.image.revision=${GIT_SHA} \
      org.opencontainers.image.title="beacon"

COPY --from=prod-deps --chown=1000:1000 /app/node_modules ./node_modules
COPY --from=build --chown=1000:1000 /app/.next ./.next
COPY --from=build --chown=1000:1000 /app/dist ./dist
COPY --chown=1000:1000 package.json next.config.ts ./
# next.config.ts is compiled when `next start` boots, so the files it imports must be here too:
# the security headers (lesson 8.1). Keep that module free of imports so this stays one file.
COPY --chown=1000:1000 src/core/security-headers.ts ./src/core/security-headers.ts
COPY --chown=1000:1000 drizzle ./drizzle
# Uploaded files with the local storage driver: mount a volume here (or use STORAGE_DRIVER=s3).
RUN mkdir -p /app/.storage && chown 1000:1000 /app/.storage

# Never run as root: the `node` user (uid 1000) that comes with the official image.
USER 1000:1000
EXPOSE 3000

# Liveness (lesson 7.2): the process answers. Readiness (/api/ready) is for the load balancer.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:'+(process.env.PORT||3000)+'/api/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]

# Exec form: the process is PID 1 and receives SIGTERM, so the worker drains its
# jobs and Next.js finishes in-flight requests before the platform kills them.
CMD ["node_modules/.bin/next", "start"]
