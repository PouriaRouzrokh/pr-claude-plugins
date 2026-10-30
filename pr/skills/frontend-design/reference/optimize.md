# Optimize

Find the real bottleneck for this interface, fix it, and measure the change. Optimizing what isn't slow wastes time and adds complexity. For React and Next.js specifics, apply the rules in [react-rules/REACT-BEST-PRACTICES.md](react-rules/REACT-BEST-PRACTICES.md) rather than the generic advice here.

## Contents

- [Measure first](#measure-first)
- [Core Web Vitals](#core-web-vitals)
- [Loading](#loading)
- [Rendering and animation](#rendering-and-animation)
- [Responsiveness (INP)](#responsiveness-inp)
- [Verify](#verify)

## Measure first

1. **Collect numbers:** Core Web Vitals (LCP, INP, CLS), plus FCP and Total Blocking Time in the lab; bundle sizes (JS, CSS, fonts, images); request count and waterfall; frame rate and long tasks during interaction.
2. **Locate the cause:** initial load, interaction, or animation? Large images, too much JavaScript, render-blocking resources, layout thrashing, or third-party scripts?
3. **Size the impact:** who is affected (all users, mobile, slow connections) and whether it is perceptible.

Useful tools: Lighthouse and the Performance panel in Chrome DevTools (or `web-quality-audit` for a full Lighthouse run), WebPageTest, the Chrome UX Report for field data, and the project's bundle analyzer. Lab runs on a fast desktop are not representative; throttle CPU and network to approximate mid-range phones.

## Core Web Vitals

Thresholds are for the 75th percentile of page loads.

| Metric | Good | Poor | Typical fixes |
|--------|------|------|---------------|
| **LCP** (largest contentful paint) | ≤ 2.5s | > 4s | Serve the LCP image early (`fetchpriority="high"`, never `loading="lazy"`), right-sized and in AVIF/WebP; cut render-blocking CSS and JS; server-render or statically generate; use a CDN |
| **INP** (interaction to next paint) | ≤ 200ms | > 500ms | Break up long tasks, do less work per interaction, defer non-critical JS, move heavy computation to a worker |
| **CLS** (cumulative layout shift) | ≤ 0.1 | > 0.25 | Set `width`/`height` or `aspect-ratio` on media and embeds; reserve space for late content; never insert content above what the user is reading; match fallback font metrics |

## Loading

**Images**
- Use AVIF or WebP, sized to the rendered dimensions, with `srcset` and an accurate `sizes` ([adapt.md](adapt.md#responsive-images)).
- `loading="lazy"` and `decoding="async"` for below-the-fold images only; the hero gets `fetchpriority="high"`.

```html
<img src="hero-1200.avif" srcset="hero-800.avif 800w, hero-1200.avif 1200w, hero-2000.avif 2000w"
     sizes="100vw" width="2000" height="1125" fetchpriority="high" alt="…">
<img src="gallery-1.avif" width="600" height="400" loading="lazy" decoding="async" alt="…">
```

**JavaScript**
- Split by route and lazy-load heavy, below-the-fold, or interaction-only components (`import()`, `React.lazy`, `next/dynamic`).
- Remove unused dependencies; check what each large import really costs.
- Load third-party scripts with `defer`/`async` or after interaction, and question each one.

**CSS**
- Remove unused CSS; inline only the critical CSS when the build supports it.
- Use `content-visibility: auto` with `contain-intrinsic-size` on long, offscreen sections (Baseline since 2025).

**Fonts**
- Self-host WOFF2, subset to the scripts you need, load only the weights you use (a variable font often replaces several files).
- Preload the one or two fonts used above the fold; use `font-display: swap` (or `optional` when layout stability matters more than the brand face on first view).
- Tune fallback metrics with `size-adjust` and the override descriptors ([typeset.md](typeset.md#font-loading)).

**Network**
- Cache static assets with long-lived, content-hashed URLs; compress with Brotli.
- `preconnect` to critical third-party origins; `preload` only what the parser discovers late.
- Prefetch likely next pages through the framework's router or speculation rules (Chromium only; other browsers ignore them safely).
- Under HTTP/2 and HTTP/3, many small files are fine; prefer good caching over aggressive bundling into one file.

## Rendering and animation

- **Layout thrashing:** don't interleave DOM reads and writes in a loop. Batch reads, then writes:

```js
const heights = items.map((el) => el.offsetHeight);           // read all
items.forEach((el, i) => { el.style.height = `${heights[i] * 2}px`; }); // then write all
```

- **Animated properties:** `transform` and `opacity` run on the compositor; layout properties (`width`, `height`, `top`, `left`, margins) force layout every frame. Blur, filters, masks, and large shadows are paint-heavy: keep them small and isolated. See [animate.md](animate.md#implement-to-the-runtime).
- **`will-change`:** apply only just before a known expensive animation and remove it after; left on at rest, it wastes memory.
- **DOM size:** keep it lean; virtualize long lists and tables (TanStack Virtual or similar) instead of rendering thousands of rows.
- **Containment:** `contain: layout paint` on independent widgets limits how far a change ripples.
- **Observers over listeners:** use `IntersectionObserver` for visibility and `ResizeObserver` for size, not scroll or resize handlers; if a scroll handler is unavoidable, make it passive and throttle with `requestAnimationFrame`.

## Responsiveness (INP)

- Give immediate visual feedback, then do the work: update the pressed state first, defer the expensive part.
- Break long tasks so the browser can paint between chunks. `scheduler.yield()` is the cleanest tool where supported (Chromium and Firefox as of 2026); fall back to `setTimeout(0)`:

```js
const yieldToMain = () =>
  globalThis.scheduler?.yield ? scheduler.yield() : new Promise((r) => setTimeout(r, 0));

for (const chunk of chunks) {
  process(chunk);
  await yieldToMain();
}
```

- Debounce input-driven work such as search (around 200–300ms), and move heavy parsing, filtering, or image processing to a Web Worker.
- In React, keep urgent updates urgent and mark the rest as transitions (`useTransition`, `useDeferredValue`).

## Verify

- Compare before and after with the same throttling settings, and with field data when the project has real-user monitoring.
- Test on a throttled mid-range mobile profile, not only a fast desktop.
- Confirm no functionality, accessibility, or visual regressions: optimization that breaks behavior is not an improvement.
- Fix the biggest bottleneck first; micro-optimizations rarely move the vitals.

When the user-facing numbers move, finish with a polish pass ([polish.md](polish.md)).
