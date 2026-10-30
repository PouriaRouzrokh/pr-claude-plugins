---
title: Use a Data-Fetching Library for Client-Side Deduplication
impact: MEDIUM-HIGH
impactDescription: automatic deduplication
tags: client, swr, tanstack-query, react-query, deduplication, data-fetching
---

## Use a Data-Fetching Library for Client-Side Deduplication

When Client Components fetch data, use a data-fetching library such as SWR or TanStack Query. Both deduplicate identical requests across component instances and add caching, revalidation, and mutation helpers. Pick one per app and use it consistently.

**Incorrect (no deduplication, each instance fetches):**

```tsx
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users')
      .then(r => r.json())
      .then(setUsers)
  }, [])
}
```

**Correct with SWR (multiple instances share one request):**

```tsx
import useSWR from 'swr'
import useSWRImmutable from 'swr/immutable'
import useSWRMutation from 'swr/mutation'

function UserList() {
  const { data: users } = useSWR('/api/users', fetcher)
}

// Data that never changes: no revalidation on focus or reconnect
function StaticContent() {
  const { data } = useSWRImmutable('/api/config', fetcher)
}

// Mutations: the fetcher receives (key, { arg })
function UpdateButton() {
  const { trigger } = useSWRMutation('/api/user', updateUser)
  return <button onClick={() => trigger({ name: 'New name' })}>Update</button>
}
```

**Correct with TanStack Query (v5):**

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

function UserList() {
  const { data: users } = useQuery({ queryKey: ['users'], queryFn: fetchUsers })
}

function UpdateButton() {
  const queryClient = useQueryClient()
  const { mutate } = useMutation({
    mutationFn: updateUser,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['user'] }),
  })
  return <button onClick={() => mutate({ name: 'New name' })}>Update</button>
}
```

TanStack Query requires a `QueryClientProvider` near the root; SWR works without a provider.

> **Note (2026):** In the Next.js App Router, first ask whether the data needs client fetching at all. Fetching in a Server Component (deduplicated per request by `fetch` memoization or `React.cache()`), or starting the fetch on the server and passing the promise to a Client Component that reads it with `use()`, avoids a client round trip. Reach for SWR or TanStack Query for client-driven data: polling, infinite lists, optimistic updates, or data that depends on client-only state.

Reference: [SWR](https://swr.vercel.app), [TanStack Query](https://tanstack.com/query/latest), [Next.js data fetching](https://nextjs.org/docs/app/getting-started/fetching-data#client-components)
