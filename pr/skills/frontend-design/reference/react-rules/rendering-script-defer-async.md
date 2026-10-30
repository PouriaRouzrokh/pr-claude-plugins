---
title: Use defer or async on Script Tags
impact: HIGH
impactDescription: eliminates render-blocking
tags: rendering, script, defer, async, performance
---

## Use defer or async on Script Tags

**Impact: HIGH (eliminates render-blocking)**

Script tags without `defer` or `async` block HTML parsing while the script downloads and executes. This delays First Contentful Paint and Time to Interactive.

- **`defer`**: Downloads in parallel, executes after HTML parsing completes, maintains execution order
- **`async`**: Downloads in parallel, executes immediately when ready, no guaranteed order

In static HTML, use `defer` for scripts that depend on the DOM or on each other, and `async` for independent scripts such as analytics.

**Incorrect (blocks rendering):**

```tsx
export default function Document() {
  return (
    <html>
      <head>
        <script src="https://example.com/analytics.js" />
        <script src="/scripts/utils.js" />
      </head>
      <body>{/* content */}</body>
    </html>
  )
}
```

**Correct (non-blocking, React 19):**

```tsx
export default function Document() {
  return (
    <html>
      <head>
        <script src="https://example.com/analytics.js" async />
        <script src="/scripts/utils.js" async />
      </head>
      <body>{/* content */}</body>
    </html>
  )
}
```

In React 19, a `<script>` with `src` and `async` can be rendered from any component: React hoists it to `<head>` and de-duplicates scripts with the same `src`. React's docs mark `defer` as incompatible with streaming server rendering, so in streamed apps (including the Next.js App Router) use `async` and make scripts that depend on each other wait for the `load` event. To start a download even earlier, call `preinit(src, { as: 'script' })` from `react-dom`.

**In Next.js**, prefer `next/script` and choose a `strategy`:

```tsx
import Script from 'next/script'

export default function Page() {
  return (
    <>
      {/* Tag managers, analytics: load soon after hydration (the default) */}
      <Script src="https://example.com/analytics.js" strategy="afterInteractive" />
      {/* Chat and social widgets: load during idle time */}
      <Script src="https://example.com/chat-widget.js" strategy="lazyOnload" />
    </>
  )
}
```

Reserve `strategy="beforeInteractive"` for scripts the whole site needs before hydration, such as bot detectors or cookie consent managers. It must be placed in the root layout.

Reference: [MDN script element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#defer), [React `<script>`](https://react.dev/reference/react-dom/components/script), [Next.js Script](https://nextjs.org/docs/app/api-reference/components/script)
