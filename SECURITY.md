# Security policy

Beacon is a course project, but it is written as if it were a real SaaS, so it has a real policy (lesson 8.1).

## Reporting a vulnerability

Please report it privately: see [`/.well-known/security.txt`](src/core/trust.ts) on a running Beacon
(`Contact:`), or open a GitHub security advisory on this repository. Do not open a public issue.

We acknowledge reports within two business days, keep you informed, do not pursue good-faith research that
respects user data, and credit you in the release notes if you wish.

## What is in scope

The application in this repository: authentication, tenant isolation (one organization reading or changing
another's data), the SSRF guard on monitor and webhook URLs, the public API and its keys, webhook signatures,
the admin panel and impersonation, the AI incident summaries (prompt injection that reaches the public status
page). The threat model is [docs/security/threat-model.md](docs/security/threat-model.md).

## For contributors

- Never commit a secret. `npm run hooks:install` once per clone runs gitleaks before every commit; CI scans
  the whole history. If a secret lands anyway, **rotate it first** (see [docs/security/secrets.md](docs/security/secrets.md)).
- A new vendor that receives customer data goes into `SUBPROCESSORS` in `src/core/trust.ts` in the same pull request.
