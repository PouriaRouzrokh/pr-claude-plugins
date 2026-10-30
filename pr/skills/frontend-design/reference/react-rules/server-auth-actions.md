---
title: Authenticate Server Actions Like API Routes
impact: CRITICAL
impactDescription: prevents unauthorized access to server mutations
tags: server, server-actions, server-functions, authentication, security, authorization
---

## Authenticate Server Actions Like API Routes

**Impact: CRITICAL (prevents unauthorized access to server mutations)**

Server Actions (functions marked `'use server'`, also called Server Functions) are reachable by direct POST requests, just like API routes. Verify authentication and authorization **inside** each action. Do not rely on Proxy (formerly middleware), layout guards, or page-level checks: a page-level check controls which UI renders, but the action is a separate entry point.

The Next.js data security guide puts it this way: "you should still treat Server Actions as reachable via direct POST requests and verify authentication and authorization inside each one."

**Incorrect (no authentication check):**

```typescript
'use server'

export async function deleteUser(userId: string) {
  // Anyone can call this! No auth check
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**Correct (authentication and authorization inside the action):**

```typescript
'use server'

import { verifySession } from '@/lib/auth'

export async function deleteUser(userId: string) {
  const session = await verifySession()
  if (!session) {
    throw new Error('Unauthorized')
  }

  // Authorization: can this user act on this resource?
  if (session.user.role !== 'admin' && session.user.id !== userId) {
    throw new Error('Forbidden')
  }

  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**With input validation (Zod 4):**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { z } from 'zod'

const updateProfileSchema = z.object({
  userId: z.uuid(),
  name: z.string().min(1).max(100),
  email: z.email(),
})

export async function updateProfile(data: unknown) {
  // 1. Authenticate
  const session = await verifySession()
  if (!session) {
    throw new Error('Unauthorized')
  }

  // 2. Validate untrusted input
  const validated = updateProfileSchema.parse(data)

  // 3. Authorize against the validated input
  if (session.user.id !== validated.userId) {
    throw new Error('Can only update own profile')
  }

  await db.user.update({
    where: { id: validated.userId },
    data: { name: validated.name, email: validated.email },
  })

  // Return only what the UI needs, never the raw database record
  return { success: true }
}
```

For larger apps, move auth checks and queries into a `server-only` Data Access Layer and keep `'use server'` files thin, so every entry point shares the same checks.

Reference: [Next.js data security guide](https://nextjs.org/docs/app/guides/data-security), [Next.js authentication guide](https://nextjs.org/docs/app/guides/authentication)
