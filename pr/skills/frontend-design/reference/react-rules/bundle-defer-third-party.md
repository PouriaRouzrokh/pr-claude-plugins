---
title: Defer Non-Critical Third-Party Libraries
impact: MEDIUM
impactDescription: loads after hydration
tags: bundle, third-party, analytics, defer
---

## Defer Non-Critical Third-Party Libraries

Analytics, logging, error tracking, session replay, and chat widgets don't block user interaction. Load them after hydration.

**Incorrect (heavy SDK in the initial client bundle):**

```tsx
// app/providers.tsx
'use client'

import { ReplayWidget } from 'heavy-replay-sdk'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <ReplayWidget />
    </>
  )
}
```

**Correct (loads after hydration, from a Client Component):**

```tsx
// app/deferred-widgets.tsx
'use client'

import dynamic from 'next/dynamic'

const ReplayWidget = dynamic(
  () => import('heavy-replay-sdk').then(m => m.ReplayWidget),
  { ssr: false }
)

export function DeferredWidgets() {
  return <ReplayWidget />
}
```

```tsx
// app/layout.tsx (Server Component)
import { DeferredWidgets } from './deferred-widgets'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <DeferredWidgets />
      </body>
    </html>
  )
}
```

`ssr: false` only works inside a Client Component. Calling it from a Server Component such as the root layout fails with "`ssr: false` is not allowed with `next/dynamic` in Server Components", so wrap the dynamic import in a small `'use client'` file and render that from the layout.

For third parties delivered as a script tag rather than an npm package, use `next/script` with `strategy="lazyOnload"` (chat, social widgets) or `"afterInteractive"` (tag managers, analytics); see [Use defer or async on Script Tags](./rendering-script-defer-async.md). Small, purpose-built components such as `@vercel/analytics` already inject a deferred script and don't need this wrapper.

Reference: [Next.js lazy loading](https://nextjs.org/docs/app/guides/lazy-loading)
