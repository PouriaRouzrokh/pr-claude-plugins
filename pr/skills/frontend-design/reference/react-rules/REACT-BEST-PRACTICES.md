# React and Next.js Best Practices: Rule Index

An index of the 70 performance and correctness rules in this folder, adapted from Vercel's react-best-practices. Each rule lives in its own file with incorrect and correct examples; this page lists them by category with a one-line summary so you can jump to the one you need. Rules were reviewed against React 19.3.1, React Compiler 1.0, and Next.js 16.4.3 (October 2026).

## Contents

- [How to use](#how-to-use)
- [Categories](#categories)
- [1. Eliminating Waterfalls (async)](#1-eliminating-waterfalls-async)
- [2. Bundle Size Optimization (bundle)](#2-bundle-size-optimization-bundle)
- [3. Server-Side Performance (server)](#3-server-side-performance-server)
- [4. Client-Side Data Fetching (client)](#4-client-side-data-fetching-client)
- [5. Re-render Optimization (rerender)](#5-re-render-optimization-rerender)
- [6. Rendering Performance (rendering)](#6-rendering-performance-rendering)
- [7. JavaScript Performance (js)](#7-javascript-performance-js)
- [8. Advanced Patterns (advanced)](#8-advanced-patterns-advanced)
- [What changed in 2026](#what-changed-in-2026)

## How to use

- **Writing new code:** skim the CRITICAL and HIGH categories first; they cover waterfalls, bundle size, and server rendering, where the largest wins are.
- **Reviewing or optimizing:** measure first, then match the symptom (slow first load, slow navigation, janky input, large payload) to a category below and open the relevant rules.
- **Check the project's setup before applying re-render rules.** If React Compiler is enabled (`reactCompiler: true` in `next.config`, or `babel-plugin-react-compiler` in Vite), most manual `memo`/`useMemo`/`useCallback` advice is handled for you; each affected rule says so in a "Note (2026)".
- **Check the Next.js version and whether Cache Components is enabled** (`cacheComponents: true`, which Next.js 16.4 recommends together with `partialPrefetching: true`). Several server rules have Cache Components-specific guidance. `ensureStatic` (16.4) guarantees that a route's shell, prefetch, or full navigation is static, and `next upgrade --agent` prints version-specific upgrade guidance an agent can follow.
- Rule format: [_template.md](_template.md). Category definitions and impact levels: [_sections.md](_sections.md).

## Categories

| # | Category | Prefix | Impact | Focus |
|---|----------|--------|--------|-------|
| 1 | Eliminating Waterfalls | `async-` | CRITICAL | Sequential awaits each add a full round trip |
| 2 | Bundle Size Optimization | `bundle-` | CRITICAL | Less JavaScript means faster TTI and LCP |
| 3 | Server-Side Performance | `server-` | HIGH | Server waterfalls, caching, RSC payload size, security |
| 4 | Client-Side Data Fetching | `client-` | MEDIUM-HIGH | Deduplication and efficient client fetching |
| 5 | Re-render Optimization | `rerender-` | MEDIUM | Avoid wasted renders and effect re-runs |
| 6 | Rendering Performance | `rendering-` | MEDIUM | Browser rendering, hydration, resource loading |
| 7 | JavaScript Performance | `js-` | LOW-MEDIUM | Hot-path micro-optimizations |
| 8 | Advanced Patterns | `advanced-` | LOW | Effect Events, refs, one-time initialization |

## 1. Eliminating Waterfalls (async)

| Rule | Impact | Summary |
|------|--------|---------|
| [async-parallel](async-parallel.md) | CRITICAL | Run independent async operations with `Promise.all()`. |
| [async-dependencies](async-dependencies.md) | CRITICAL | With partial dependencies, start each task as early as possible (`better-all` or promise chaining). |
| [async-api-routes](async-api-routes.md) | CRITICAL | In Route Handlers and Server Actions, start independent work before awaiting. |
| [async-defer-await](async-defer-await.md) | HIGH | Move `await` into the branch that uses the result. |
| [async-cheap-condition-before-await](async-cheap-condition-before-await.md) | HIGH | Check cheap synchronous conditions before awaiting a flag. |
| [async-suspense-boundaries](async-suspense-boundaries.md) | HIGH | Wrap data-dependent parts in `<Suspense>` so the shell renders first; required for uncached data under Cache Components. |

## 2. Bundle Size Optimization (bundle)

| Rule | Impact | Summary |
|------|--------|---------|
| [bundle-barrel-imports](bundle-barrel-imports.md) | CRITICAL | Avoid barrel imports; Next.js optimizes popular libraries by default, add others via `optimizePackageImports`. |
| [bundle-dynamic-imports](bundle-dynamic-imports.md) | CRITICAL | Lazy-load heavy client components with `next/dynamic` (`ssr: false` only in Client Components). |
| [bundle-analyzable-paths](bundle-analyzable-paths.md) | HIGH | Use explicit import maps and literal file paths so bundlers and file tracing stay narrow. |
| [bundle-conditional](bundle-conditional.md) | HIGH | Import large modules only when the feature is activated. |
| [bundle-defer-third-party](bundle-defer-third-party.md) | MEDIUM | Load analytics, replay, and chat SDKs after hydration from a Client Component wrapper. |
| [bundle-preload](bundle-preload.md) | MEDIUM | Start loading heavy bundles on hover, focus, or when a flag enables them. |

## 3. Server-Side Performance (server)

| Rule | Impact | Summary |
|------|--------|---------|
| [server-auth-actions](server-auth-actions.md) | CRITICAL | Authenticate, validate, and authorize inside every Server Action. |
| [server-parallel-fetching](server-parallel-fetching.md) | CRITICAL | Split fetching into sibling async components so they run in parallel. |
| [server-parallel-nested-fetching](server-parallel-nested-fetching.md) | CRITICAL | Chain each item's dependent fetch inside its own promise. |
| [server-serialization](server-serialization.md) | HIGH | Pass only the fields a Client Component uses across the RSC boundary. |
| [server-cache-lru](server-cache-lru.md) | HIGH | Cache across requests; in Next.js 16 prefer `'use cache'` with `cacheLife`/`cacheTag`. |
| [server-hoist-static-io](server-hoist-static-io.md) | HIGH | Read static files (fonts, templates, config) once at module scope. |
| [server-no-shared-module-state](server-no-shared-module-state.md) | HIGH | Never store request or user data in mutable module-level variables. |
| [server-cache-react](server-cache-react.md) | MEDIUM | Deduplicate non-`fetch` work within one request with `React.cache()`. |
| [server-after-nonblocking](server-after-nonblocking.md) | MEDIUM | Run logging and analytics after the response with `after()`. |
| [server-dedup-props](server-dedup-props.md) | LOW | Don't pass the same data twice under new references; derive it on the client. |

## 4. Client-Side Data Fetching (client)

| Rule | Impact | Summary |
|------|--------|---------|
| [client-swr-dedup](client-swr-dedup.md) | MEDIUM-HIGH | Use SWR or TanStack Query for client fetching; prefer server fetching or `use()` where possible. |
| [client-localstorage-schema](client-localstorage-schema.md) | MEDIUM | Version `localStorage` keys, store minimal fields, wrap access in try/catch. |
| [client-passive-event-listeners](client-passive-event-listeners.md) | MEDIUM | Mark touch and wheel listeners `{ passive: true }` unless they call `preventDefault()`. |
| [client-event-listeners](client-event-listeners.md) | LOW | Share one global listener across many hook instances. |

## 5. Re-render Optimization (rerender)

| Rule | Impact | Summary |
|------|--------|---------|
| [rerender-no-inline-components](rerender-no-inline-components.md) | HIGH | Never define components inside components; it remounts them every render. |
| [rerender-derived-state-no-effect](rerender-derived-state-no-effect.md) | MEDIUM | Compute derived values during render instead of syncing them with effects. |
| [rerender-move-effect-to-event](rerender-move-effect-to-event.md) | MEDIUM | Put user-triggered side effects in event handlers, not state plus effect. |
| [rerender-derived-state](rerender-derived-state.md) | MEDIUM | Subscribe to a derived boolean (media query) instead of a continuous value. |
| [rerender-defer-reads](rerender-defer-reads.md) | MEDIUM | Read search params or storage inside callbacks instead of subscribing. |
| [rerender-functional-setstate](rerender-functional-setstate.md) | MEDIUM | Use functional `setState` updates to avoid stale closures and dependencies. |
| [rerender-lazy-state-init](rerender-lazy-state-init.md) | MEDIUM | Pass a function to `useState` for expensive initial values. |
| [rerender-use-ref-transient-values](rerender-use-ref-transient-values.md) | MEDIUM | Keep high-frequency, non-visual values in refs. |
| [rerender-transitions](rerender-transitions.md) | MEDIUM | Mark frequent non-urgent updates with `startTransition`. |
| [rerender-use-deferred-value](rerender-use-deferred-value.md) | MEDIUM | Keep input responsive with `useDeferredValue` plus a memoized slow child. |
| [rerender-split-combined-hooks](rerender-split-combined-hooks.md) | MEDIUM | Split hooks that mix independent work; the compiler handles values, not effects. |
| [rerender-memo](rerender-memo.md) | MEDIUM | Extract expensive work into components so early returns skip it. |
| [rerender-simple-expression-in-memo](rerender-simple-expression-in-memo.md) | LOW-MEDIUM | Don't wrap cheap primitive expressions in `useMemo`. |
| [rerender-memo-with-default-value](rerender-memo-with-default-value.md) | LOW | Hoist non-primitive default prop values to module constants. |
| [rerender-dependencies](rerender-dependencies.md) | LOW | Depend on primitives (`user.id`, `isMobile`) rather than whole objects. |

## 6. Rendering Performance (rendering)

| Rule | Impact | Summary |
|------|--------|---------|
| [rendering-content-visibility](rendering-content-visibility.md) | HIGH | Apply `content-visibility: auto` to long lists of off-screen items. |
| [rendering-resource-hints](rendering-resource-hints.md) | HIGH | Use `preconnect`, `preload`, and `preinit` from `react-dom` for resources the framework doesn't cover. |
| [rendering-script-defer-async](rendering-script-defer-async.md) | HIGH | Never block parsing with scripts; use `async` in React 19 or a `next/script` strategy. |
| [rendering-activity](rendering-activity.md) | MEDIUM | Use `<Activity>` to hide UI while keeping its state and DOM. |
| [rendering-hydration-no-flicker](rendering-hydration-no-flicker.md) | MEDIUM | Apply client-only values (theme) with an inline script before hydration. |
| [rendering-hydration-suppress-warning](rendering-hydration-suppress-warning.md) | LOW-MEDIUM | Use `suppressHydrationWarning` only for expected, one-level mismatches. |
| [rendering-usetransition-loading](rendering-usetransition-loading.md) | LOW | Use `useTransition`'s `isPending` instead of manual loading flags; rewrap updates after `await`. |
| [rendering-conditional-render](rendering-conditional-render.md) | LOW | Use ternaries when a falsy `0` or `NaN` would render. |
| [rendering-hoist-jsx](rendering-hoist-jsx.md) | LOW | Hoist static JSX out of components (automatic with the compiler). |
| [rendering-animate-svg-wrapper](rendering-animate-svg-wrapper.md) | LOW | Animate a wrapper element around an SVG; mostly relevant to older engines now. |
| [rendering-svg-precision](rendering-svg-precision.md) | LOW | Reduce SVG coordinate precision, for example with SVGO. |

## 7. JavaScript Performance (js)

| Rule | Impact | Summary |
|------|--------|---------|
| [js-tosorted-immutable](js-tosorted-immutable.md) | MEDIUM-HIGH | Use `toSorted()` and friends; never mutate props or state with `sort()`. |
| [js-batch-dom-css](js-batch-dom-css.md) | MEDIUM | Avoid layout thrashing: batch DOM reads and writes, prefer classes. |
| [js-cache-function-results](js-cache-function-results.md) | MEDIUM | Cache repeated pure function results in a module-level Map (bounded on the server). |
| [js-request-idle-callback](js-request-idle-callback.md) | MEDIUM | Defer non-critical work with `requestIdleCallback`, with a fallback. |
| [js-index-maps](js-index-maps.md) | LOW-MEDIUM | Build a Map once instead of repeated `.find()` calls. |
| [js-set-map-lookups](js-set-map-lookups.md) | LOW-MEDIUM | Use a Set or Map for repeated membership checks. |
| [js-combine-iterations](js-combine-iterations.md) | LOW-MEDIUM | Combine several filters over the same array into one loop. |
| [js-flatmap-filter](js-flatmap-filter.md) | LOW-MEDIUM | Use `flatMap` to map and filter in one pass. |
| [js-early-exit](js-early-exit.md) | LOW-MEDIUM | Return as soon as the result is known. |
| [js-length-check-first](js-length-check-first.md) | LOW-MEDIUM | Compare lengths before expensive array comparisons. |
| [js-hoist-regexp](js-hoist-regexp.md) | LOW-MEDIUM | Create regexes at module scope or memoize them; beware `/g` state. |
| [js-cache-property-access](js-cache-property-access.md) | LOW-MEDIUM | Cache deep property lookups in hot loops. |
| [js-cache-storage](js-cache-storage.md) | LOW-MEDIUM | Cache `localStorage` and cookie reads in memory and invalidate on change. |
| [js-min-max-loop](js-min-max-loop.md) | LOW | Find min or max with a loop, not a sort. |

## 8. Advanced Patterns (advanced)

| Rule | Impact | Summary |
|------|--------|---------|
| [advanced-init-once](advanced-init-once.md) | LOW-MEDIUM | Run app-wide initialization once per load, not per mount. |
| [advanced-use-latest](advanced-use-latest.md) | LOW | Read the latest props in effects with `useEffectEvent` (React 19.2+). |
| [advanced-event-handler-refs](advanced-event-handler-refs.md) | LOW | Keep subscriptions stable with `useEffectEvent`, or a ref on older React. |
| [advanced-effect-event-deps](advanced-effect-event-deps.md) | LOW | Never list an Effect Event in a dependency array. |

## What changed in 2026

These rules were reviewed against current releases: React 19.3 (September 2026), React Compiler 1.0 (October 2025), Next.js 16.4 (October 2026), SWR 2.5, TanStack Query 5, and Zod 4. Version-sensitive guidance is marked "Note (2026)" in the rule files.

- **Security floor: Next.js 16.4.1 or later (16.4.3 is current), React 19.3.1.** Next.js 16.4.1 (2026-10-14) fixed two critical unauthenticated remote code execution bugs, one in `use cache` functions that return typed arrays ([GHSA-673q-mjm6-r5xr](https://github.com/vercel/next.js/security/advisories/GHSA-673q-mjm6-r5xr)) and one in the Image Optimization API with SVG files ([GHSA-2464-fhr4-w9xw](https://github.com/vercel/next.js/security/advisories/GHSA-2464-fhr4-w9xw)), plus a high-severity Server Actions denial of service ([GHSA-p3m5-59mp-jv5r](https://github.com/vercel/next.js/security/advisories/GHSA-p3m5-59mp-jv5r)). React 19.3.1 (2026-10-14) improved the Server Components transport protocol. Do not apply the Cache Components or `next/image` guidance below to a project on an older 16.x until it is upgraded.
- **React Compiler is stable.** It memoizes components and values automatically. The memoization rules ([rerender-memo](rerender-memo.md), [rerender-split-combined-hooks](rerender-split-combined-hooks.md), [rerender-use-deferred-value](rerender-use-deferred-value.md), [rerender-simple-expression-in-memo](rerender-simple-expression-in-memo.md), [rendering-hoist-jsx](rendering-hoist-jsx.md), [js-hoist-regexp](js-hoist-regexp.md)) now say what still matters: projects without the compiler, components it skips, and values that must stay stable as effect dependencies. Leave existing manual memoization in place unless you test its removal.
- **`useEffectEvent` and `<Activity>` are stable (React 19.2).** The ref-based handler pattern is now the fallback for older React. Effect Events have no stable identity and must stay out of dependency arrays.
- **Async transitions:** state updates after an `await` inside `startTransition` must be wrapped in another `startTransition`, and async Actions don't guarantee completion order ([rendering-usetransition-loading](rendering-usetransition-loading.md)).
- **React 19 scripts and hydration:** prefer `async` over `defer` in streamed apps; React hoists and de-duplicates async scripts. React 19.3's `use(browser())` inside a `<Suspense>` boundary offers a client-only render path (`onBrowserBailout` on the `react-dom/server` APIs reports when a subtree defers to the browser). React 19.3 also integrates Trusted Types, and transitions now render independently instead of being entangled, so a slow transition no longer holds up an unrelated one. Theme flicker is solved with a `<head>` script plus `suppressHydrationWarning` on `<html>`.
- **Next.js 16 Cache Components** (`'use cache', `cacheLife`, `cacheTag`, `updateTag`, `revalidateTag(tag, profile)`) is the recommended caching model and is on by default in new apps since 16.4. It makes Suspense boundaries around uncached data a requirement and replaces hand-rolled cross-request caches in most cases.
- **Next.js 16 API changes reflected in the rules:** `middleware.ts` is now `proxy.ts`; request APIs (`cookies()`, `headers()`, `params`, `searchParams`) are async only; `next/image` `priority` is deprecated in favor of `preload`; `ssr: false` in `next/dynamic` is allowed only in Client Components; `after()` request-API rules differ between Server Components and Route Handlers.
- **Corrected rules:** [bundle-defer-third-party](bundle-defer-third-party.md) (the upstream example used `ssr: false` in a Server Component layout), [rendering-script-defer-async](rendering-script-defer-async.md) (wrong `next/script` strategy mapping), [client-swr-dedup](client-swr-dedup.md) (wrong SWR imports; now library-neutral), [rerender-memo-with-default-value](rerender-memo-with-default-value.md) (wrong explanation of how `memo()` compares props; impact lowered to LOW), [server-auth-actions](server-auth-actions.md) (Zod 4 syntax and current Next.js guidance), and [js-length-check-first](js-length-check-first.md) (impact lowered to LOW-MEDIUM).
- **Barrel imports:** Next.js optimizes most popular icon and UI libraries by default, so `optimizePackageImports` is for packages outside that list and for internal barrels.
