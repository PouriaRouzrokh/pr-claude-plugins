---
name: web-quality-audit
description: Measures the performance (Core Web Vitals), accessibility (WCAG 2.2 AA), SEO, and best practices of a running web app with Lighthouse and axe-core, then produces a prioritized fix report in which every finding cites measured evidence, a concrete fix, and the skill that owns it. Includes Next.js-specific fixes. Use before deploys, after UI work, or when the user asks for a site audit, a Lighthouse run, a performance or Core Web Vitals check, an accessibility (a11y, WCAG) check, or an SEO review.
argument-hint: "[optional: URL or routes to audit]"
license: MIT. Adapted from addyosmani/web-quality-skills. See NOTICE.md.
---

# Web Quality Audit

Audit a running web app for performance, accessibility, SEO, and best practices, and turn the measurements into a prioritized fix list.

## Core Principles

- **Measure first**: Every finding cites a metric, an audit id, or a rule id with its value. Anything found only by reading code is labeled a hypothesis.
- **Production build for performance**: Dev servers inflate LCP and TBT. Accessibility and SEO results are valid on either.
- **Mobile first**: Run mobile, then desktop. Report them separately.
- **Values over scores**: Category scores summarize; metric values and failing audits are the evidence.
- **Automation is partial**: axe and Lighthouse catch only part of accessibility barriers (published estimates range from about a third to just over half). Manual checks are part of the audit, not optional extras.
- **Leave nothing behind**: Delete report files, downloaded drivers, and servers you started, unless the user wants them kept.

---

## Phase 0: Scope

**Arguments**: $ARGUMENTS

- **URL or routes given**: Audit those.
- **Empty**: Audit the home page plus the two or three most important routes (main landing, primary flow, a content page). Ask if the choice is unclear.

Note which routes need authentication and whether the target is local, staging, or production.

---

## Phase 1: Get a Running Target

1. Check whether the app is already serving: `lsof -nP -iTCP:<port> -sTCP:LISTEN` and `curl -sI <url>`.
2. If it is not running, follow the `run-local` skill to start it.
3. For performance numbers, serve a production build on a spare port as a background task, for example `npm run build && npx next start -p 3100` (use the project's package manager and framework equivalent). If only a dev server is possible, label performance results as non-representative.
4. Confirm prerequisites: Node 22.19+ (Lighthouse 13) and an installed Chrome. `jq` is optional.

---

## Phase 2: Measure

Write reports to the session scratchpad when one exists, otherwise to `.web-quality-audit/` in the project root. Shell variables do not persist between Bash calls, so set them in each call.

```bash
OUT=.web-quality-audit; URL=http://localhost:3100/
mkdir -p "$OUT"
npx --yes lighthouse "$URL" --output=json --output-path="$OUT/lh-mobile.json" \
  --form-factor=mobile --chrome-flags="--headless=new" --quiet
npx --yes lighthouse "$URL" --output=json --output-path="$OUT/lh-desktop.json" \
  --preset=desktop --chrome-flags="--headless=new" --quiet
npx --yes @axe-core/cli "$URL" --tags wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa,best-practice \
  --save axe.json --dir "$OUT"
```

- Lighthouse defaults to mobile emulation and throttling. For desktop, use `--preset=desktop`; `--form-factor=desktop` on its own fails with a screen-emulation mismatch error.
- For several routes, name files per route (`lh-mobile-pricing.json`). axe accepts several URLs in one run.
- For any performance decision, run the mobile Lighthouse command three times (`lh-mobile-1.json` to `-3`) and report the median.
- **Authenticated routes**: pass a session cookie with `--extra-headers=<file.json>` (Lighthouse only; keep the file out of git and delete it afterwards). axe CLI cannot send headers, so audit those routes with Lighthouse's accessibility category or Playwright with `@axe-core/playwright`.

**Troubleshooting**:

- **axe: "This version of ChromeDriver only supports Chrome version N"**: `@axe-core/cli` bundles the latest ChromeDriver, which often differs from the installed Chrome. Install a driver for the local Chrome major version and pass its absolute path (on Linux, read the version from `google-chrome --version`):

  ```bash
  OUT=.web-quality-audit; URL=http://localhost:3100/
  CHROME_MAJOR=$("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version | grep -oE '[0-9]+' | head -1)
  DRIVER=$(npx --yes @puppeteer/browsers install "chromedriver@$CHROME_MAJOR" --path "$PWD/$OUT/drivers" --format "{{path}}" | tail -1)
  npx --yes @axe-core/cli "$URL" --tags wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa,best-practice \
    --chromedriver-path "$DRIVER" --save axe.json --dir "$OUT"
  ```

  The axe maintainers' alternative is `npx browser-driver-manager install chrome`, which installs Chrome for Testing and a matching driver under the home directory.
- **Lighthouse `runtimeError` or `NO_FCP`**: The page did not render. Check the server and the URL, or raise `--max-wait-for-load`.
- **Containers or CI**: Add `--no-sandbox` to `--chrome-flags` only when Chrome fails to launch without it.

**No runnable page**: Run the vendored static smoke test on built HTML (for example a static export in `out/`), and label its results hypotheses: `bash ${CLAUDE_SKILL_DIR}/scripts/analyze.sh <file-or-directory>`. It needs `jq`.

---

## Phase 3: Extract the Evidence

Summarize every report into Markdown tables of category scores, Core Web Vitals with ratings, failing audits with offending nodes, axe violations with WCAG criteria, and medians across repeated runs:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/summarize.mjs .web-quality-audit/*.json
```

For ad-hoc questions, query the JSON directly:

```bash
jq '.categories | map_values(if .score then .score * 100 | round else null end)' .web-quality-audit/lh-mobile.json
jq '.audits["largest-contentful-paint"].numericValue' .web-quality-audit/lh-mobile.json
jq '.[0].violations[] | {id, impact, nodes: (.nodes | length)}' .web-quality-audit/axe.json
```

A Lighthouse audit fails when its score is below 0.9 and its `scoreDisplayMode` is `binary`, `numeric`, or `metricSavings`.

---

## Phase 4: Interpret

| Metric | Good | Poor | Source |
|--------|------|------|--------|
| LCP | ≤ 2.5 s | > 4 s | Lighthouse lab, CrUX field |
| INP | ≤ 200 ms | > 500 ms | Field data or a recorded interaction only |
| CLS | ≤ 0.1 | > 0.25 | Lighthouse lab, CrUX field |
| TBT (lab proxy for INP) | ≤ 200 ms | > 600 ms | Lighthouse lab |

A Lighthouse navigation never interacts with the page, so it cannot measure INP. Use TBT as the lab proxy, and cite field INP from PageSpeed Insights (public URLs only) or the project's RUM when available. Lab and field values are different samples; never present one as the other.

Read the reference for each failing area:

- **Performance and Core Web Vitals**: [references/core-web-vitals.md](references/core-web-vitals.md) (Lighthouse 13 insight ids, LCP/INP/CLS fixes, Next.js fixes)
- **Accessibility**: [references/accessibility.md](references/accessibility.md) (WCAG 2.2 AA checklist, manual test protocol, fix patterns). Run the manual protocol on each audited route.
- **SEO**: [references/seo.md](references/seo.md) (metadata, robots and sitemap, canonical, JSON-LD, Next.js Metadata API). Run its HTTP-level checks; Lighthouse cannot see `robots.txt` coverage or sitemap health.
- **Best practices**: Fix failing Lighthouse best-practice audits (`errors-in-console`, `deprecations`, `inspector-issues`, `image-aspect-ratio`, `is-on-https`) at the source. For security headers, CSP, and dependency vulnerabilities, recommend Claude Code's built-in `/security-review` rather than auditing them here.

For qualities tools cannot measure, apply the `frontend-design` skill's `reference/audit.md` (design-level accessibility, theming, responsive behavior) and `reference/harden.md` (long text, empty and error states, i18n). For React and Next.js performance rules, read its `reference/react-rules/`.

---

## Phase 5: Map Findings to Fixes

| Evidence | Fix | Owner skill |
|----------|-----|-------------|
| `lcp-discovery-insight`, `lcp-breakdown-insight`, `image-delivery-insight` | `next/image` with `sizes`; LCP image eager with `fetchPriority="high"` | `frontend-design` |
| `font-display-insight`, font-driven CLS | `next/font` | `frontend-design` |
| `cls-culprits-insight` | Dimensions, `aspect-ratio`, reserved slots | `frontend-design` |
| High TBT, `unused-javascript`, `legacy-javascript-insight` | Server Components, `next/dynamic`, no barrel imports | `frontend-design` (`reference/react-rules/`) |
| `third-parties-insight` | `next/script` with `lazyOnload`, facades | `frontend-design` (`reference/react-rules/`) |
| `document-latency-insight`, slow TTFB | Static or cached rendering, parallel fetching | `feature-dev` |
| `cache-insight`, `modern-http-insight`, redirects | Cache headers, CDN, HTTP/2+ | `run-public` |
| axe or Lighthouse accessibility rule ids | Pattern from the accessibility reference | `frontend-design` |
| `document-title`, `meta-description`, `canonical`, `is-crawlable`, `robots-txt` | Metadata API, `app/robots.ts`, `app/sitemap.ts` | `web-quality-audit` (apply directly) |
| `errors-in-console`, `deprecations` | Fix the underlying error | `feature-dev` |
| Security headers, CSP, HSTS | Review and harden | `/security-review` (built in) |

Fix small, well-evidenced items directly when the user asks for fixes. Route larger changes to the owner skill.

---

## Phase 6: Report

Assign severity from the evidence:

| Severity | Criteria |
|----------|----------|
| **Critical** | axe `critical`; a Core Web Vital in the poor band; production page not indexable; page fails to render |
| **High** | axe `serious`; a Core Web Vital or TBT needing improvement; a category score below 50; missing title or description on key routes |
| **Medium** | axe `moderate`; failing insights with measurable savings; missing sitemap, canonical, or structured data |
| **Low** | axe `minor`; small savings; informational diagnostics |

Raise severity for failures on primary flows (sign-up, checkout, navigation). Structure the report as follows. The Agentic column is Lighthouse 13's `agentic-browsing` category (see [references/seo.md](references/seo.md)); write `n/a` when the report lacks it, and treat it as informational, not a release gate.

```markdown
## Web Quality Audit: <app> (<date>)

**Target**: <URLs>, <production build | dev server>, Lighthouse <version>, axe-core <version>

### Scores
| Route | Form factor | Perf | A11y | Best practices | SEO | Agentic | LCP | CLS | TBT |
|-------|-------------|------|------|----------------|-----|---------|-----|-----|-----|

### Findings
| # | Severity | Category | Evidence | Fix | Owner skill |
|---|----------|----------|----------|-----|-------------|
| 1 | Critical | A11y | axe `button-name` (critical, WCAG 4.1.2), 3 nodes: `header > button.menu` | Add `aria-label` to the icon button in `components/header.tsx` | frontend-design |
| 2 | High | Perf | LCP 3.4 s mobile, median of 3; `lcp-discovery-insight` 0.00: hero is lazy-loaded | Give the hero `next/image` `loading="eager"` and `fetchPriority="high"` | frontend-design |

### Not covered by automation
Manual accessibility checks done or pending, field INP availability, hypotheses from source review.

### Recommended order
1. ...
```

---

## Phase 7: Verify and Clean Up

1. After fixes, re-run the same commands under the same conditions and report before and after values.
2. State what remains unverified: field data needs new visits, and manual accessibility checks need a person.
3. Stop any server you started for the audit.
4. Delete `.web-quality-audit/` (reports, cookie files, downloaded drivers) unless the user asks to keep it. Never commit report files.

---

## Safety Guidelines

- Audit only sites the user owns or controls, and space out runs: repeated Lighthouse and axe runs against someone else's production site can look like load testing.
- Keep authenticated audits to read-only pages. Flows that submit, purchase, or delete data change real state when a tool loads them.
- Present scores as summaries and source-only findings as hypotheses, because neither proves a measured failure or a pass.
- Report what was measured rather than promising ranking or field Core Web Vitals gains, which depend on crawling, traffic, and time outside the audit's control.
