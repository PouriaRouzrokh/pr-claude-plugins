# Tailwind Design System: Advanced Patterns

Advanced Tailwind CSS v4 patterns including animations, dark mode theming, custom utilities, theme modifiers, namespace overrides, and the v3-to-v4 migration checklist.

## Contents

- [Pattern 5: Native CSS Animations (v4)](#pattern-5-native-css-animations-v4)
- [Pattern 6: Dark Mode with CSS (v4)](#pattern-6-dark-mode-with-css-v4)
- [Advanced v4 Patterns](#advanced-v4-patterns)
- [v3 to v4 Migration Checklist](#v3-to-v4-migration-checklist)
- [Best Practices](#best-practices)

## Pattern 5: Native CSS Animations (v4)

```css
/* In your CSS file. Keyframes outside @theme are always emitted;
   inside @theme they are emitted only when an --animate-* variable uses them. */
@theme {
  --animate-dialog-in: dialog-fade-in 0.2s ease-out;
  --animate-dialog-out: dialog-fade-out 0.15s ease-in;
}

@keyframes dialog-fade-in {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-0.5rem);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes dialog-fade-out {
  from {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: scale(0.95) translateY(-0.5rem);
  }
}

/* Native popover animations using @starting-style */
[popover] {
  transition:
    opacity 0.2s,
    transform 0.2s,
    display 0.2s allow-discrete;
  opacity: 0;
  transform: scale(0.95);
}

[popover]:popover-open {
  opacity: 1;
  transform: scale(1);
}

@starting-style {
  [popover]:popover-open {
    opacity: 0;
    transform: scale(0.95);
  }
}
```

The same popover transition with utilities: `transition-discrete` adds `allow-discrete`, and the `starting:` variant writes the `@starting-style` block.

```html
<div popover class="opacity-0 scale-95 transition-all transition-discrete duration-200
                    open:opacity-100 open:scale-100 starting:open:opacity-0 starting:open:scale-95">
```

```typescript
// components/ui/dialog.tsx - Radix Dialog animated with the keyframes above via data-state
import * as DialogPrimitive from '@radix-ui/react-dialog'
import { cn } from '@/lib/utils'

const DialogPortal = DialogPrimitive.Portal

// React 19: React.ComponentProps includes ref, so it passes through with ...props
export function DialogOverlay({
  className,
  ...props
}: React.ComponentProps<typeof DialogPrimitive.Overlay>) {
  return (
    <DialogPrimitive.Overlay
      className={cn(
        'fixed inset-0 z-50 bg-black/80',
        'data-[state=open]:animate-fade-in data-[state=closed]:animate-fade-out',
        className
      )}
      {...props}
    />
  )
}

export function DialogContent({
  className,
  children,
  ...props
}: React.ComponentProps<typeof DialogPrimitive.Content>) {
  return (
    <DialogPortal>
      <DialogOverlay />
      <DialogPrimitive.Content
        className={cn(
          'fixed left-1/2 top-1/2 z-50 grid w-full max-w-lg -translate-x-1/2 -translate-y-1/2 gap-4 border border-border bg-background p-6 shadow-lg sm:rounded-lg',
          'data-[state=open]:animate-dialog-in data-[state=closed]:animate-dialog-out',
          className
        )}
        {...props}
      >
        {children}
      </DialogPrimitive.Content>
    </DialogPortal>
  )
}
```

## Pattern 6: Dark Mode with CSS (v4)

By default, `dark:` follows `prefers-color-scheme`. For a user toggle, override the variant (`@custom-variant dark (&:where(.dark, .dark *));`, or `[data-theme=dark]` for an attribute) and set the class on `<html>` **before first paint**: an inline script in `<head>` plus `suppressHydrationWarning` on `<html>`. The provider below only manages the toggle; on its own it applies the class after hydration, which flashes the wrong theme. In Next.js, the `next-themes` package implements both halves.

```tsx
// app/layout.tsx - runs before paint (script from the Tailwind dark mode docs;
// the 'theme' key must match the provider's storageKey)
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `try{document.documentElement.classList.toggle('dark',localStorage.theme==='dark'||(!('theme' in localStorage)&&matchMedia('(prefers-color-scheme: dark)').matches))}catch(e){}`,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

```typescript
// providers/ThemeProvider.tsx - Simplified for v4
'use client'

import { createContext, useContext, useEffect, useState } from 'react'

type Theme = 'dark' | 'light' | 'system'

interface ThemeContextType {
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: 'dark' | 'light'
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({
  children,
  defaultTheme = 'system',
  storageKey = 'theme',
}: {
  children: React.ReactNode
  defaultTheme?: Theme
  storageKey?: string
}) {
  // Read the stored choice on the first client render so the effect below never
  // re-applies the default over the class the <head> script already set.
  // Don't render `theme` as text before mount: the server always sees the default.
  const [theme, setTheme] = useState<Theme>(() =>
    typeof window === 'undefined'
      ? defaultTheme
      : ((localStorage.getItem(storageKey) as Theme | null) ?? defaultTheme)
  )
  const [resolvedTheme, setResolvedTheme] = useState<'dark' | 'light'>('light')

  useEffect(() => {
    const root = document.documentElement
    root.classList.remove('light', 'dark')

    const resolved = theme === 'system'
      ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
      : theme

    root.classList.add(resolved)
    setResolvedTheme(resolved)

    // Update meta theme-color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]')
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', resolved === 'dark' ? '#09090b' : '#ffffff')
    }
  }, [theme])

  return (
    <ThemeContext.Provider value={{
      theme,
      setTheme: (newTheme) => {
        // Match the <head> script: no stored key means "follow the system"
        if (newTheme === 'system') localStorage.removeItem(storageKey)
        else localStorage.setItem(storageKey, newTheme)
        setTheme(newTheme)
      },
      resolvedTheme,
    }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  return context
}

// components/ThemeToggle.tsx
'use client'

import { Moon, Sun } from 'lucide-react'
import { useTheme } from '@/providers/ThemeProvider'

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme()

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
    >
      <Sun className="size-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute size-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
```

## Advanced v4 Patterns

### Custom Utilities with `@utility`

Define reusable custom utilities. Unlike plain classes, `@utility` classes work with every variant (`hover:`, `md:`, `dark:`) and sort correctly against other utilities:

```css
/* Custom utility for decorative lines */
@utility line-t {
  @apply relative before:absolute before:top-0 before:-left-[100vw] before:h-px before:w-[200vw] before:bg-gray-950/5 dark:before:bg-white/10;
}

/* Custom utility for text gradients */
@utility text-gradient {
  @apply bg-linear-to-r from-primary to-accent bg-clip-text text-transparent;
}
```

`@apply` works in the main stylesheet. In a separately processed stylesheet (CSS modules, Vue or Svelte `<style>` blocks), add `@reference "../app.css";` first so it can see your theme and custom utilities without duplicating CSS.

### Theme Modifiers

```css
/* Use @theme inline when referencing other CSS variables */
@theme inline {
  --font-sans: var(--font-inter), system-ui;
}

/* Use @theme static to always generate CSS variables (even when unused) */
@theme static {
  --color-brand: oklch(65% 0.15 240);
}

/* Or apply an option to the whole default theme. This replaces the plain
   @import "tailwindcss" and, like any @import, must come first in the file. */
@import "tailwindcss" theme(static);
```

### Namespace Overrides

```css
@theme {
  /* Clear all default colors and define your own */
  --color-*: initial;
  --color-white: #fff;
  --color-black: #000;
  --color-primary: oklch(45% 0.2 260);
  --color-secondary: oklch(65% 0.15 200);

  /* Clear ALL defaults for a minimal setup */
  /* --*: initial; */
}
```

### Semi-transparent Color Variants

Usually unnecessary: opacity modifiers such as `bg-primary/10` already compile to `color-mix()`, and the `--alpha(var(--color-primary) / 10%)` function does the same inside custom CSS. Define named alpha tokens only when you want them as part of the design system:

```css
/* inline: utilities evaluate the expression where they are used, so the
   tokens follow a --color-primary redefined under .dark */
@theme inline {
  --color-primary-50: color-mix(in oklab, var(--color-primary) 5%, transparent);
  --color-primary-100: color-mix(
    in oklab,
    var(--color-primary) 10%,
    transparent
  );
  --color-primary-200: color-mix(
    in oklab,
    var(--color-primary) 20%,
    transparent
  );
}
```

### Container Queries

Container queries are built into v4; no plugin is needed. Mark a parent with `@container` and style children with `@sm:`, `@md:`, and so on (sizes `@3xs` at 16rem through `@7xl` at 80rem), `@max-md:` for below a size, `@container/name` with `@md/name:` for named containers, and `@min-[475px]:` for one-off sizes. v4.3 adds `@container-size` for block-size units like `cqb`.

```html
<div class="@container">
  <div class="flex flex-col @md:flex-row @max-xs:text-sm">...</div>
</div>
```

`--container-*` theme variables drive both these variants and the `max-w-*` scale, so add new sizes rather than redefining the defaults:

```css
@theme {
  --container-8xl: 96rem; /* adds @8xl: and max-w-8xl */
}
```

## v3 to v4 Migration Checklist

- [ ] Run `npx @tailwindcss/upgrade` (Node.js 20+) on a new branch and review the diff
- [ ] Replace `@tailwind base/components/utilities` with `@import "tailwindcss"`
- [ ] Move `tailwind.config.ts` theme values into `@theme`; until then, load the old file with `@config` (`corePlugins`, `safelist`, and `separator` are not supported)
- [ ] Load plugins with `@plugin`, or rewrite simple ones as `@utility`; replace `safelist` with `@source inline()`
- [ ] Replace `darkMode: "class"` with `@custom-variant dark (&:where(.dark, .dark *))`
- [ ] Rename shifted utilities: `shadow-sm` to `shadow-xs`, `shadow` to `shadow-sm` (same for `rounded`, `blur`, `drop-shadow`), `outline-none` to `outline-hidden`, `ring` to `ring-3`
- [ ] Replace removed utilities: `bg-opacity-*` with `/50` modifiers, `flex-shrink-*` with `shrink-*`, `flex-grow-*` with `grow-*`, `overflow-ellipsis` with `text-ellipsis`
- [ ] Add explicit colors to `border`, `divide`, and `ring` (they now default to `currentColor`)
- [ ] Update arbitrary variables (`bg-[--x]` to `bg-(--x)`) and important (`!flex` to `flex!`)
- [ ] Replace `theme()` in CSS with `var(--...)`; add `@reference` to CSS modules and component `<style>` blocks that use `@apply`
- [ ] Replace `tailwindcss-animate` with `tw-animate-css` or native `@keyframes`
- [ ] Prefer `size-*`, `bg-linear-*`, and OKLCH colors in new code
- [ ] Remove `forwardRef` (React 19 passes `ref` as a prop)

## Best Practices

### Do's

- **Use `@theme` blocks** - CSS-first configuration is v4's core pattern
- **Use OKLCH colors** - Better perceptual uniformity than HSL
- **Compose with CVA** - Type-safe variants
- **Use semantic tokens** - `bg-primary` not `bg-blue-500`
- **Use `size-*`** - Shorthand for `w-* h-*`
- **Use `gap` over `space-*`** - Flex and grid gaps avoid the v4 `space-*` selector edge cases
- **Add accessibility** - ARIA attributes, focus states

### Don'ts

- **Don't start new projects with `tailwind.config.ts`** - Use CSS `@theme`; keep `@config` for legacy migration only
- **Don't use `@tailwind` directives** - Use `@import "tailwindcss"`
- **Don't use `forwardRef`** - React 19 passes ref as prop
- **Don't repeat arbitrary values** - Promote a value used more than once into `@theme`
- **Don't hardcode colors** - Use semantic tokens
- **Don't forget dark mode** - Test both themes
