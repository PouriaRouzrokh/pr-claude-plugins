---
name: atlas-development
description: "ATLAS (Architect, Trace, Link, Assemble, Stress-test) is this toolkit's development philosophy for building production-ready software instead of demos: define the problem and success metric, design data and integrations before code, validate every connection before building, assemble in thin end-to-end slices, and prove it works with evidence. Includes a variant for ML and data pipelines. Use when planning or building features, MVPs, or applications, or when deciding how much process a task needs."
---

# ATLAS Development Framework

Most failed AI-assisted builds fail the same ways: code before a clear goal, a data model discovered halfway through, an integration that turns out not to work after hours of building on it, and "done" without proof. ATLAS puts a cheap check in front of each of those failures. It is a way of thinking, not a form to fill in: apply the steps that pay for themselves on the task at hand.

| Step | Phase | Question it answers |
|------|-------|---------------------|
| **A** | Architect | What problem, for whom, and how will we know it worked? |
| **T** | Trace | What data, integrations, and stack does it need, and what can break? |
| **L** | Link | Does every connection actually work, before we build on it? |
| **A** | Assemble | How do we build it in layers that stay coherent? |
| **S** | Stress-test | What evidence shows it works, including when things go wrong? |

## How Much Process

| Task | Apply |
|------|-------|
| New application or MVP | All five steps (`create-prd` → `mvp-dev`) |
| Feature with new integrations, schema changes, or architectural choices | T, L, A, S (`feature-dev`, full depth) |
| Feature that follows existing patterns | L, A, S, briefly (`feature-dev`, light depth) |
| Bug fix | Not ATLAS: use `systematic-debugging` (root cause, regression test, fix) |
| One-line change, docs, refactor without behavior change | Just do it and verify |

## A — Architect

Know what you are building before touching code.

1. **Problem**, in one sentence. If it will not fit in one sentence, it is not understood yet.
2. **User**, specifically: "me", "the clinic's front-desk staff", not "everyone".
3. **Success**, measurably: "a radiologist can find a prior study in under 10 seconds", not "it works".
4. **Constraints**: budget (including API and compute costs), time, required platforms or services, compliance.

Output: a brief (problem, user, success metric, constraints), or a full PRD from `create-prd`.

## T — Trace

Design the parts that are expensive to change later.

- **Data model**: entities, fields, relationships, ownership, and lifecycle. Schema changes cascade into every layer, so settle them first.
- **Integrations map**: every external service with its purpose, auth method, rate limits, cost, and whether access already exists.

  | Service | Purpose | Auth | Limits / cost | Access confirmed? |
  |---------|---------|------|---------------|-------------------|

- **Stack**: propose it with current, verified versions (check Context7 or official docs, not memory), and get the user's approval.
- **Failure modes**: rate limits, token expiry, timeouts, invalid input, partial failures, an MCP server or API being down. Decide how each is handled.

## L — Link

Prove every connection works before building on it. Hours of building on a broken integration is the most avoidable waste in software.

- [ ] Database connects; a trivial query returns rows or an empty result, not an error
- [ ] Each API key works with a real request, and the response shape matches expectations
- [ ] OAuth or auth flows complete end to end
- [ ] MCP servers list their tools and one simple call succeeds
- [ ] Environment variables load in every runtime (dev server, tests, scripts, deployment)
- [ ] Rate limits and quotas are known and acceptable

Everything green before Assemble. Record the results (in the architecture RFD for MVPs).

## A — Assemble

Build in layers, but integrate early.

- **Contracts first**: the schema and API shapes from Trace.
- **Then a thin end-to-end slice**: one real path through every layer (data → logic → API → UI) working before widening. It surfaces integration problems while they are still cheap.
- **Then widen** feature by feature, keeping each layer's responsibility clear: UI renders and collects input; the server owns business rules and validation; the database is the source of truth.
- Use the project's existing component libraries and patterns; do not reinvent primitives.
- Write tests alongside the code (`test-driven-development`), and keep configuration out of code.

## S — Stress-test

Show evidence, not confidence.

- **Verify behavior directly**: run the test suite, call the endpoints, exercise the UI in a browser at mobile and desktop widths. Use the verification gate in `test-driven-development`: only claim what fresh output shows.
- **Break it on purpose**: invalid input, empty states, long text, slow or failing network, expired auth, concurrent use.
- **Review**: `/simplify` for quality, then `/code-review high` for bugs, and `/security-review` for anything touching auth, payments, uploads, or personal data (it needs an `origin` remote; without one, use a security-focused `pr:code-reviewer` agent); `web-quality-audit` for web performance and accessibility.
- **Acceptance**: confirm the original problem is solved for the original user, against the success metric from Architect.
- **Leave it clean**: no temporary scripts, debug output, or test data; code that reads as if a careful senior engineer wrote it.

For production releases, add two more checks: **Validate** (input sanitization, abuse cases, dependency audit) and **Monitor** (logging, error tracking, alerts, and a way to roll back).

## ATLAS for ML and Data Pipelines

| Step | What it means here |
|------|--------------------|
| Architect | The decision the model supports, the metric that matters (and its threshold), the baseline to beat, and data or compute budgets. |
| Trace | Data sources, labeling, splits (by patient, site, or time to prevent leakage), preprocessing contract, experiment tracking, and where artifacts live. |
| Link | Data access works at full scale, a single batch flows through the whole pipeline, GPUs and environments are available, and the evaluation script runs on a trivial model. |
| Assemble | Data pipeline → baseline → model, with configuration-driven experiments and fixed seeds. |
| Stress-test | Beat the baseline on held-out data, check for leakage, examine subgroups and failure cases, confirm reproducibility from a clean environment. |

## Multi-Agent Use

Use subagents for independent work: parallel exploration in Trace, competing designs in Assemble, separate review dimensions in Stress-test. When agents must negotiate (architects settling a shared schema, reviewers challenging each other's findings), first try named subagents that message each other with `SendMessage`; use agent teams (experimental, interactive only, much more expensive) only when that is not enough. Architect stays a conversation with the user.

## Anti-Patterns

1. **Building before designing**: leads to rewrites when the real requirements surface.
2. **Skipping Link**: hours lost on integrations that never worked.
3. **No data model**: schema changes cascade into every layer.
4. **"Done" without evidence**: broken code shipped with confidence.
5. **Hard-coded configuration**: every environment change becomes a code change.
6. **Messy handoff**: debug leftovers and duplication erode trust even when the code works.

## Related Skills

| Phase | Skills |
|-------|--------|
| Architect | `create-prd` |
| Trace, Link | `feature-dev`, `mvp-dev` |
| Assemble | `frontend-design`, `generate-image`, `generate-svg`, `generate-video`, `test-driven-development` |
| Stress-test | `test-driven-development`, `systematic-debugging`, `web-quality-audit`, `writing-clearly-and-concisely` |
