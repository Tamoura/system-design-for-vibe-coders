# SaaS Building Blocks — Outline

31 lessons in 10 modules. Every lesson climbs the same ladder — 🟢 essentials →
🟡 going deeper → 🔴 at scale — and the level badge says where it *starts*.
The running example is **Beacon**: uptime monitoring and public status pages for teams.

## Module 0 — Orientation: Every SaaS Is the Same App
| # | Lesson | Level |
|---|---|---|
| 0.1 | The 80% nobody sells: the anatomy of every SaaS | 🟢 |
| 0.2 | How to read a giant open-source codebase without drowning | 🟢 |
| 0.3 | The reference shelf: the SaaS codebases and starter kits we study | 🟢 |

## Module 1 — Identity & Access
| # | Lesson | Level |
|---|---|---|
| 1.1 | Authentication: proving who someone is | 🟢 |
| 1.2 | Users, organizations & invitations: the multi-tenant skeleton | 🟢 |
| 1.3 | Authorization: roles, permissions, and "can this user do this?" | 🟡 |
| 1.4 | Enterprise identity: SSO, SAML, OIDC and SCIM | 🔴 |

## Module 2 — Data
| # | Lesson | Level |
|---|---|---|
| 2.1 | The data layer: Postgres, ORMs, migrations and seeds | 🟢 |
| 2.2 | File uploads and object storage | 🟢 |
| 2.3 | Search: from `LIKE '%x%'` to a search engine | 🟡 |
| 2.4 | Multi-tenancy deep dive: isolation, noisy neighbours, residency | 🔴 |

## Module 3 — Money
| # | Lesson | Level |
|---|---|---|
| 3.1 | Subscriptions and payments: checkout, webhooks, the customer portal | 🟢 |
| 3.2 | Plans, limits and entitlements: turning pricing into code | 🟡 |
| 3.3 | Usage-based billing and metering | 🔴 |

## Module 4 — Communication
| # | Lesson | Level |
|---|---|---|
| 4.1 | Transactional email that actually arrives | 🟢 |
| 4.2 | Notifications: in-app, push, Slack, SMS — and preferences | 🟡 |
| 4.3 | Real-time and collaboration: WebSockets to CRDTs | 🔴 |

## Module 5 — Background Work & Integrations
| # | Lesson | Level |
|---|---|---|
| 5.1 | Background jobs, queues and scheduled tasks | 🟡 |
| 5.2 | The public API: API keys, versioning and rate limits | 🟡 |
| 5.3 | Outbound webhooks and third-party integrations | 🟡 |
| 5.4 | Workflow engines and durable execution | 🔴 |

## Module 6 — Product & Growth
| # | Lesson | Level |
|---|---|---|
| 6.1 | The app shell: marketing site, onboarding, dashboard and settings | 🟢 |
| 6.2 | Analytics: product, web and the event pipeline | 🟡 |
| 6.3 | Feature flags and experiments | 🟡 |

## Module 7 — Operating the SaaS
| # | Lesson | Level |
|---|---|---|
| 7.1 | The admin panel: support tools and impersonation | 🟡 |
| 7.2 | Observability: logs, errors, metrics and traces | 🟡 |
| 7.3 | Audit logs and activity feeds | 🟡 |
| 7.4 | Deployment, environments and self-hostable SaaS | 🔴 |

## Module 8 — Trust & the Frontier
| # | Lesson | Level |
|---|---|---|
| 8.1 | Security and compliance: secrets, encryption, SOC 2, GDPR | 🔴 |
| 8.2 | AI features as a SaaS component | 🔴 |

## Module 9 — Capstone
| # | Lesson | Level |
|---|---|---|
| 9.1 | Assemble Beacon: reference architecture, build-vs-buy and a 90-day plan | 🔴 |

## Appendices
- [The repo catalog](./REPOS.md) — every repository in the course, by component.
- [Learning paths](./README.md#learning-paths) — Beginner, Intermediate and Advanced tracks.
