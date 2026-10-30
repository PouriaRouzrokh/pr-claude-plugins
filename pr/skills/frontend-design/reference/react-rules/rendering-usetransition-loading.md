---
title: Use useTransition Over Manual Loading States
impact: LOW
impactDescription: reduces re-renders and improves code clarity
tags: rendering, transitions, useTransition, loading, state
---

## Use useTransition Over Manual Loading States

Use `useTransition` instead of manual `useState` for loading states. This provides built-in `isPending` state and automatically manages transitions.

**Incorrect (manual loading state):**

```tsx
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async (value: string) => {
    setIsLoading(true)
    setQuery(value)
    const data = await fetchResults(value)
    setResults(data)
    setIsLoading(false)
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isLoading && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**Correct (useTransition with built-in pending state):**

```tsx
import { useTransition, useState } from 'react'

function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  const handleSearch = (value: string) => {
    setQuery(value) // Update input immediately
    
    startTransition(async () => {
      const data = await fetchResults(value)
      // State updates after an await must be wrapped again to count as a transition
      startTransition(() => {
        setResults(data)
      })
    })
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**Benefits:**

- **Automatic pending state**: `isPending` stays true until the whole async Action, including awaited work, finishes
- **Error resilience**: An error thrown inside the Action resets the pending state and reaches the nearest error boundary
- **Better responsiveness**: The input update stays urgent while the results update renders at lower priority

**Caveats:**

- React loses the transition context after `await`, so state updates that follow an `await` need their own `startTransition` (shown above). React plans to remove this limitation once `AsyncContext` is available.
- Transitions do not cancel earlier ones, and async Actions don't guarantee completion order: a slow earlier search can finish after a newer one and overwrite its results. Use `useActionState` or form actions, which order updates for you, or track the latest request and ignore stale responses (an `AbortController` also saves the wasted fetch).

Reference: [useTransition](https://react.dev/reference/react/useTransition)
