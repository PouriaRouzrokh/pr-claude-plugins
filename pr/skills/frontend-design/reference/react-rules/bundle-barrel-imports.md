---
title: Avoid Barrel File Imports
impact: CRITICAL
impactDescription: 200-800ms import cost, slow builds
tags: bundle, imports, tree-shaking, barrel-files, performance
---

## Avoid Barrel File Imports

Import directly from source files instead of barrel files to avoid loading thousands of unused modules. **Barrel files** are entry points that re-export multiple modules (e.g., `index.js` that does `export * from './module'`).

Popular icon and component libraries can have **up to 10,000 re-exports** in their entry file. For many React packages, **it takes 200-800ms just to import them**, affecting both development speed and production cold starts.

**Why tree-shaking doesn't help:** When a library is marked as external (not bundled), the bundler can't optimize it. If you bundle it to enable tree-shaking, builds become substantially slower analyzing the entire module graph.

**Incorrect (imports entire library):**

```tsx
import { Check, X, Menu } from 'lucide-react'
// Loads 1,583 modules, takes ~2.8s extra in dev
// Runtime cost: 200-800ms on every cold start

import { Button, TextField } from '@mui/material'
// Loads 2,225 modules, takes ~4.2s extra in dev
```

**Correct - Next.js (recommended):**

Next.js already rewrites barrel imports for a built-in list of popular packages, including `lucide-react`, `@mui/material`, `@mui/icons-material`, `date-fns`, `lodash-es`, `react-icons/*`, `@headlessui/react`, `@tabler/icons-react`, `@heroicons/react/*`, `recharts`, `rxjs`, `ramda`, `antd`, and `react-use`. Keep standard imports for those:

```tsx
// No config needed for packages on the default list
import { Check, X, Menu } from 'lucide-react'
```

Add packages that are not on the list, such as your own design-system package or an internal barrel-heavy library:

```ts
// next.config.ts
const nextConfig = {
  experimental: {
    optimizePackageImports: ['@acme/ui', 'some-icon-library'],
  },
}

export default nextConfig
```

This preserves TypeScript types and editor autocompletion while still eliminating the barrel import cost.

> **Note (2026):** `optimizePackageImports` is still under `experimental` in Next.js 16.4. Because the common UI and icon libraries are optimized by default, this rule mostly matters for packages outside the default list, for your own internal `index.ts` barrels, and for non-Next.js bundlers.

**Correct - Direct imports (non-Next.js projects):**

```tsx
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
// Loads only what you use
```

> **TypeScript warning:** Some libraries (notably `lucide-react`) don't ship `.d.ts` files for their deep import paths. Importing from `lucide-react/dist/esm/icons/check` resolves to an implicit `any` type, causing errors under `strict` or `noImplicitAny`. Prefer `optimizePackageImports` when available, or verify the library exports types for its subpaths before using direct imports.

These optimizations provide 15-70% faster dev boot, 28% faster builds, 40% faster cold starts, and significantly faster HMR.

Libraries commonly affected: `lucide-react`, `@mui/material`, `@mui/icons-material`, `@tabler/icons-react`, `react-icons`, `@headlessui/react`, `@radix-ui/react-*`, `lodash`, `ramda`, `date-fns`, `rxjs`, `react-use`.

Reference: [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js), [`optimizePackageImports`](https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports)
