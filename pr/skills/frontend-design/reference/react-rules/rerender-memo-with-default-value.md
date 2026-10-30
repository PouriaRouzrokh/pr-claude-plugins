---
title: Hoist Non-Primitive Default Prop Values to Constants
impact: LOW
impactDescription: keeps default values referentially stable for hooks and memoized children
tags: rerender, memo, default-props, optimization
---

## Hoist Non-Primitive Default Prop Values to Constants

A non-primitive default in a destructured prop (`onClick = () => {}`, `items = []`, `style = {}`) creates a new value every time the component renders. `memo()` itself is not affected: it compares the props the parent passed, and an omitted prop is `undefined` on every render. The problem is everything downstream of the default. When the defaulted value goes into a `useEffect`, `useMemo`, or `useCallback` dependency array, or is passed to a memoized child, it changes on every render and defeats that memoization.

Extract the default to a module-level constant.

**Incorrect (`onClick` is a new function on every render of `UserAvatar`):**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // Re-runs on every render because the default is new each time
  useEffect(() => {
    registerShortcut('a', onClick)
    return () => unregisterShortcut('a')
  }, [onClick])
  // ...
})

// Used without optional onClick
<UserAvatar />
```

**Correct (stable default value):**

```tsx
const NOOP = () => {}

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  useEffect(() => {
    registerShortcut('a', onClick)
    return () => unregisterShortcut('a')
  }, [onClick])
  // ...
})

// Used without optional onClick
<UserAvatar />
```

A module-level constant is stable whether or not React Compiler is enabled, so it is the safe default for any non-primitive fallback.
