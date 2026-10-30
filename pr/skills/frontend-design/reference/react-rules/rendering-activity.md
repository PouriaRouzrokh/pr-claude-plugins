---
title: Use Activity Component for Show/Hide
impact: MEDIUM
impactDescription: preserves state/DOM
tags: rendering, activity, visibility, state-preservation
---

## Use Activity Component for Show/Hide

Use React's `<Activity>` (stable since React 19.2) to preserve state and DOM for expensive components that frequently toggle visibility, such as tabs, drawers, and menus.

**Usage:**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

In `hidden` mode, React hides the children with `display: none`, destroys their Effects (cleaning up subscriptions), and keeps their state. Hidden children still re-render on new props, at lower priority. When the boundary becomes visible again, state is restored and Effects re-run. Rendering a boundary as `hidden` from the start pre-renders it in the background without mounting Effects, which makes a likely next tab instant.

**Caveats:**

- Hidden DOM stays in the page, so `<video>`, `<audio>`, and `<iframe>` keep playing. Pause them in a `useLayoutEffect` cleanup.
- A hidden Activity whose child is plain text renders nothing, since there is no element to hide.
- Code that relies on an Effect running once at mount will see it re-run on every reveal. `<StrictMode>` surfaces these bugs early.

Reference: [React `<Activity>`](https://react.dev/reference/react/Activity)
