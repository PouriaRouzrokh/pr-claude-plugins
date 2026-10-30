---
title: Conditional Module Loading
impact: HIGH
impactDescription: loads large data only when needed
tags: bundle, conditional-loading, lazy-loading
---

## Conditional Module Loading

Load large data or modules only when a feature is activated.

**Example (lazy-load animation frames):**

```tsx
function AnimationPlayer({ enabled, setEnabled }: { enabled: boolean; setEnabled: React.Dispatch<React.SetStateAction<boolean>> }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js')
        .then(mod => setFrames(mod.frames))
        .catch(() => setEnabled(false))
    }
  }, [enabled, frames, setEnabled])

  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

Effects never run on the server, so the `typeof window !== 'undefined'` check does nothing at runtime here. Its value is at build time: Next.js replaces `typeof window` with a constant in each bundle, so the server build drops the `import()` as dead code and never bundles the module.

> **Note (2026):** To skip server rendering for a whole component instead of one module, use `next/dynamic` with `ssr: false` from a Client Component (see [Dynamic Imports for Heavy Components](./bundle-dynamic-imports.md)), or, on React 19.3+, call `use(browser())` from `react-dom` inside the component so the server renders the nearest Suspense fallback.
