---
title: Extract to Memoized Components
impact: MEDIUM
impactDescription: enables early returns
tags: rerender, memo, useMemo, optimization
---

## Extract to Memoized Components

Extract expensive work into memoized components to enable early returns before computation.

**Incorrect (computes avatar even when loading):**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user)
    return <Avatar id={id} />
  }, [user])

  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}
```

**Correct (skips computation when loading):**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  )
}
```

The structural point holds with or without memoization: an early return placed before expensive work skips it entirely.

> **Note (2026):** React Compiler 1.0 (stable since October 2025; `reactCompiler: true` in Next.js 16, off by default) memoizes components and values automatically, so in compiled code you don't need `memo()` or `useMemo()` for this. Manual memoization still matters when the compiler is not enabled, when it skips a component that breaks the Rules of React (no ✨ badge in React DevTools), or when you need a guaranteed-stable value, for example as an effect dependency. React's guidance for existing code is to leave current `useMemo`/`useCallback`/`memo` in place, or test carefully before removing them.
