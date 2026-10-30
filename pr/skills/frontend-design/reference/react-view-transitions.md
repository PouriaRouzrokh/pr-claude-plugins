# React view transitions

Animate between UI states in React 19.3 and later with the `<ViewTransition>` component, which wraps the browser's View Transition API. Use it when continuity is the point (a list item becoming its detail page, content arriving, a reordered list). For when motion is warranted at all, see [animate.md](animate.md); for browser support, see the table in [overdrive.md](overdrive.md#browser-support-snapshot).

## Contents

- [Availability](#availability)
- [Rules that decide whether it works](#rules-that-decide-whether-it-works)
- [Props and types](#props-and-types)
- [Next.js](#nextjs)
- [Patterns worth the effort](#patterns-worth-the-effort)

## Availability

- `ViewTransition` and `addTransitionType` are stable in React 19.3 (2026-09-09). Earlier stable React has neither.
- Next.js App Router needs no configuration and no `react@canary`: its bundled React channel includes them, and navigations already run as transitions. Do not add the old `experimental.viewTransition` flag.
- Browsers: Chromium 125+, Firefox 144+, Safari 18.2+. Elsewhere the update still happens, without the animation.
- Never call `document.startViewTransition` yourself in a React tree; React does it.

## Rules that decide whether it works

- Only `startTransition`, `useDeferredValue`, and `Suspense` reveals animate. A plain `setState` does not.
- `<ViewTransition>` must sit above any DOM node in its subtree. A `<div>` around it suppresses enter and exit.
- Triggers: `enter` (inserted), `exit` (removed), `update` (content or size changed inside it), `share` (a named boundary unmounts while another with the same `name` mounts).
- Do not wrap `{children}` of a layout in `<ViewTransition>` when pages declare their own; layouts persist across navigations and the pair cancels out.
- Every link click in Next.js is a transition, so a boundary left at `default="auto"` animates on every navigation. Set `default="none"` and opt in.

## Props and types

```tsx
import { ViewTransition, startTransition, addTransitionType } from "react";

<ViewTransition
  default="none"
  enter={{ "nav-forward": "slide-from-right", "nav-back": "slide-from-left", default: "none" }}
  exit={{ "nav-forward": "slide-to-left", "nav-back": "slide-to-right", default: "none" }}
  share="morph"
  name={`product-${id}`}
>
  <Card />
</ViewTransition>;

startTransition(() => {
  addTransitionType("nav-forward");
  router.push(`/products/${id}`);
});
```

Prop values are `"auto"` (browser cross-fade), `"none"`, a CSS class name, or an object mapping transition types to those. Style the class with `::view-transition-old(.slide-to-left)`, `::view-transition-new(...)`, and `::view-transition-group(...)`; wrap the keyframes in `@media (prefers-reduced-motion: no-preference)` and fall back to a crossfade or nothing.

## Next.js

On Next.js 16.2 and later, put types on the link instead of wiring `onNavigate`: `<Link href="/products/1" transitionTypes={["nav-forward"]}>`. Keep manual `startTransition` for buttons and forms. A shared-element morph only works when the incoming content is ready as the navigation commits, so prefetch the destination (`prefetch={true}`) or cache it. Check the installed version's docs under `node_modules/next/dist/docs/` before relying on a flag.

## Patterns worth the effort

Add each only when it says something, in this priority order:

1. **Shared element** (`name` plus `share`): "the same thing, going deeper".
2. **Suspense reveal** (`enter`/`exit` on the fallback and content): "data arrived".
3. **List identity** (a `<ViewTransition key={id}>` per item): "same items, new arrangement".
4. **State change** (`enter`/`exit`): "something appeared or went away".
5. **Route change**: "a new place". Reserve directional slides for hierarchical navigation and ordered sequences; tabs and background refreshes get a fade or `default="none"`.
