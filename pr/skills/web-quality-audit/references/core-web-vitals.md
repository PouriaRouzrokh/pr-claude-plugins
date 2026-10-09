# Core Web Vitals and Performance

Read this reference when a Lighthouse run shows a failing Core Web Vital, a performance score below 90, or failing performance insights.

## Contents

- [Thresholds](#thresholds)
- [Lab versus field evidence](#lab-versus-field-evidence)
- [Repeatable lab runs](#repeatable-lab-runs)
- [Lighthouse 13 insight audits](#lighthouse-13-insight-audits)
- [LCP: Largest Contentful Paint](#lcp-largest-contentful-paint)
- [INP: Interaction to Next Paint](#inp-interaction-to-next-paint)
- [CLS: Cumulative Layout Shift](#cls-cumulative-layout-shift)
- [Next.js fixes](#nextjs-fixes)
- [Field monitoring](#field-monitoring)
- [Sources](#sources)

## Thresholds

| Metric | Measures | Good | Needs improvement | Poor |
|--------|----------|------|-------------------|------|
| **LCP** | Loading | ≤ 2.5 s | 2.5 – 4 s | > 4 s |
| **INP** | Responsiveness | ≤ 200 ms | 200 – 500 ms | > 500 ms |
| **CLS** | Visual stability | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |
| TBT (lab proxy for INP) | Main-thread blocking during load | ≤ 200 ms | 200 – 600 ms | > 600 ms |

Google assesses field data at the **75th percentile** of page visits, separately for phone and desktop.

**INP needs interaction.** A Lighthouse navigation run never clicks or types, so it reports no INP. Use Total Blocking Time (TBT) as the lab proxy, and get real INP from field data (CrUX through PageSpeed Insights for public URLs, or first-party RUM) or from a recorded interaction in the Chrome DevTools Performance panel.

## Lab versus field evidence

| Evidence | What it represents | Best use |
|----------|--------------------|----------|
| CrUX field data | Real Chrome users over a rolling 28 days | Decide whether users have a problem |
| First-party RUM | The site's own user sessions | Segment by route, device, and release |
| Lighthouse lab run | One synthetic, throttled navigation | Reproduce load problems, prevent regressions |
| DevTools performance trace | One observed session, optionally with interactions | Diagnose LCP, INP, and CLS causes |
| Source inspection | Inferred from code | Hypotheses only |

A `PerformanceObserver` result from one browser tab is a single-session lab observation, not field data.

| Field | Lab | Interpretation |
|-------|-----|----------------|
| Poor | Poor | Reproducible user problem: trace and fix the dominant bottleneck |
| Poor | Good | The lab run missed real conditions: test real devices, routes, and interactions |
| Good | Poor | The throttled cold load is fragile, but users are not currently failing |
| Unavailable | Any | Diagnose with lab data; recommend RUM if production impact matters |

Localhost, staging, new, and low-traffic pages usually have no CrUX record. Treat missing field data as **unavailable**, never as passing.

## Repeatable lab runs

Record the conditions with every result: final URL and page state, Lighthouse version, form factor, throttling, cache state, and whether the server ran a production build.

- Audit a production build (`next build && next start`). Dev servers ship unminified code, compile routes on demand, and inject HMR clients, so their LCP and TBT are not representative.
- For any decision based on a lab metric, run the same configuration three times and report the median and range (`summarize.mjs` computes this when given several runs of the same URL and form factor).
- Lighthouse scores are weighted summaries that change between versions. Cite metric values and audit ids as evidence, not the score alone.

## Lighthouse 13 insight audits

Lighthouse 13 replaced many older performance audits with shared Performance Insights. Failing insights have a score below 0.9 and usually list `metricSavings`.

| Audit id | Signals | Typical fix |
|----------|---------|-------------|
| `lcp-breakdown-insight` | Which LCP subpart dominates: TTFB, load delay, load duration, render delay | Fix the dominant subpart only |
| `lcp-discovery-insight` | LCP image found late or lazy-loaded | Put it in the initial HTML with high fetch priority; never lazy-load it |
| `document-latency-insight` | Slow server response, redirects, no compression | Cache, render statically, remove redirects |
| `render-blocking-insight` | CSS or sync scripts delaying first render | Split or inline critical CSS, defer scripts |
| `network-dependency-tree-insight` | Long request chains | Preload or preconnect only the proven critical chain |
| `image-delivery-insight` | Oversized or legacy-format images | Resize, serve AVIF/WebP, set `sizes` |
| `font-display-insight` | Invisible text while fonts load | `font-display: swap` or `optional` |
| `cls-culprits-insight` | Shifted nodes and their causes | Reserve space (see [CLS](#cls-cumulative-layout-shift)) |
| `third-parties-insight` | Main-thread and transfer cost by third-party origin | Defer, lazy-load, or replace with a facade |
| `forced-reflow-insight` | Layout reads interleaved with writes | Batch reads before writes |
| `legacy-javascript-insight`, `duplicated-javascript-insight` | Polyfills or duplicated modules in bundles | Modern browserslist, dedupe dependencies |
| `unused-javascript`, `bootup-time`, `mainthread-work-breakdown` | JavaScript cost that drives TBT | Code-split, move work to the server |
| `cache-insight` | Short cache lifetimes on static assets | Long `max-age` with `immutable` for hashed files |
| `dom-size-insight` | Very large DOM | Virtualize long lists, paginate |
| `viewport-insight` | Missing mobile viewport meta tag | `width=device-width, initial-scale=1` |

## LCP: Largest Contentful Paint

The LCP element is usually a hero image, a poster frame, a background image, or a large text block. Find it in `lcp-breakdown-insight` or with this single-session snippet:

```javascript
new PerformanceObserver((list) => {
  const last = list.getEntries().at(-1);
  console.log('LCP element:', last.element, 'time:', last.startTime);
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

| Dominant subpart | Cause | Fix |
|------------------|-------|-----|
| TTFB (> 800 ms) | Slow server work, no cache, cold starts | Static or cached rendering, CDN, parallel data fetching |
| Resource load delay | Image discovered late (CSS background, client-rendered) | Render an `<img>` in server HTML with `fetchpriority="high"` |
| Resource load duration | Image too large | Resize, compress, modern format, correct `sizes` |
| Element render delay | Render-blocking CSS/JS, client-side rendering, font blocking | Server rendering, defer scripts, `font-display: swap` |

Add `<link rel="preload">` only when the trace shows late discovery that cannot be fixed in markup; speculative preloads compete for bandwidth.

## INP: Interaction to Next Paint

INP has three phases. Find the dominant one in a trace before changing code:

| Phase | Evidence | Fix |
|-------|----------|-----|
| Input delay | Long tasks already running when the user acts | Reduce startup JavaScript, split long tasks, delay third parties |
| Processing time | Slow event handlers | Do less synchronous work, move computation to a Web Worker |
| Presentation delay | Expensive style, layout, or paint after the handler | Shrink the updated DOM, avoid forced layout |

Yield to the main thread inside long work so the browser can paint feedback first:

```javascript
async function processInChunks(items, work, chunkSize = 100) {
  for (let i = 0; i < items.length; i += chunkSize) {
    items.slice(i, i + chunkSize).forEach(work);
    if (globalThis.scheduler?.yield) await scheduler.yield();
    else await new Promise((resolve) => setTimeout(resolve, 0));
  }
}
```

In React, wrap non-urgent state updates in `startTransition` so typing and clicking stay responsive. Memoize only where a profile shows repeated expensive renders.

To observe slow interactions in one session (lab, not field INP):

```javascript
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 200) console.warn('Slow interaction', entry.name, entry.duration, entry.target);
  }
}).observe({ type: 'event', buffered: true, durationThreshold: 40 });
```

## CLS: Cumulative Layout Shift

The element that moves is often the victim; find the trigger in `cls-culprits-insight`.

- **Media without dimensions.** Give every `<img>`, `<video>`, and `<iframe>` `width`/`height` or a CSS `aspect-ratio`.
- **Late content above the fold.** Banners, consent bars, ads, and async components need a reserved container sized before the content arrives, or should render as overlays.
- **Web font swaps.** Use a metric-matched fallback (`size-adjust`, `ascent-override`, `descent-override`); `next/font` generates one automatically.
- **Layout animations.** Animate `transform` and `opacity` instead of `top`, `left`, `width`, or `height`.

```javascript
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!entry.hadRecentInput) {
      console.log('Shift', entry.value, entry.sources?.map((source) => source.node));
    }
  }
}).observe({ type: 'layout-shift', buffered: true });
```

## Next.js fixes

**LCP image.** Use `next/image` with explicit `sizes`. `next/image` lazy-loads by default, and `fetchPriority="high"` alone does not change that. In Next.js 16 and later, give the single LCP image `loading="eager"` plus `fetchPriority="high"`, or `preload` when it must start from `<head>` (the `priority` prop is deprecated). On Next.js 15 and earlier, use `priority`.

```tsx
import Image from 'next/image';

<Image src="/hero.jpg" alt="Product dashboard" fill sizes="100vw" loading="eager" fetchPriority="high" />
```

**Fonts.** `next/font` self-hosts the font, removes the external request, and generates a metric-matched fallback that prevents layout shift.

```tsx
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], display: 'swap' });
// <html lang="en" className={inter.className}>
```

**JavaScript cost (TBT, INP).** Keep components as Server Components unless they need state or browser APIs. Load heavy client-only widgets with `next/dynamic`; `ssr: false` is only allowed inside a Client Component.

```tsx
'use client';
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('./chart'), { ssr: false, loading: () => <ChartSkeleton /> });
```

**Third-party scripts.** Load them through `next/script` with `strategy="afterInteractive"` or `"lazyOnload"`, and use facades for embeds such as video players and chat widgets.

**Server response.** Prefer static or cached rendering, fetch independent data in parallel, and stream slow sections behind `<Suspense>`.

For React and Next.js performance rules with code examples, read the `frontend-design` skill's `reference/react-rules/`. The most relevant rules for audit findings:

| Finding | Rules |
|---------|-------|
| `unused-javascript`, high TBT | `bundle-barrel-imports`, `bundle-dynamic-imports`, `bundle-conditional` |
| `third-parties-insight` | `bundle-defer-third-party` |
| Slow TTFB, `document-latency-insight` | `async-parallel`, `async-suspense-boundaries`, `server-parallel-fetching`, `server-cache-react` |
| Slow interactions | `rerender-transitions`, `rendering-usetransition-loading`, `rerender-memo` |
| Long lists, large DOM | `rendering-content-visibility` |

## Field monitoring

For production RUM in Next.js, report metrics with `useReportWebVitals` from `next/web-vitals` in a Client Component, or use the `web-vitals` library (its `attribution` build identifies the slow interaction or shifted element). Field data reflects a fix only after enough new visits, typically days for RUM and up to 28 days for CrUX.

## Sources

- [web.dev: LCP](https://web.dev/articles/lcp), [INP](https://web.dev/articles/inp), [CLS](https://web.dev/articles/cls)
- [Optimize INP](https://web.dev/articles/optimize-inp) and [`scheduler.yield()`](https://web.dev/articles/optimize-long-tasks)
- [Lighthouse performance insights](https://developer.chrome.com/blog/moving-lighthouse-to-insights)
- [Next.js Image component](https://nextjs.org/docs/app/api-reference/components/image), [Font optimization](https://nextjs.org/docs/app/getting-started/fonts), [Lazy loading](https://nextjs.org/docs/app/guides/lazy-loading)
