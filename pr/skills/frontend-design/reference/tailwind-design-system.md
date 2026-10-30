# Tailwind Design System (v4)

Build production-ready design systems with Tailwind CSS v4, including CSS-first configuration, design tokens, component variants, responsive patterns, and accessibility.

> **Note**: This reference targets Tailwind CSS v4 (v4.0 shipped January 2025; v4.3 is current as of October 2026). For v3 projects, run the upgrade tool (`npx @tailwindcss/upgrade`, Node.js 20+) and read the [upgrade guide](https://tailwindcss.com/docs/upgrade-guide).

## Contents

- [When to Use](#when-to-use)
- [Setup](#setup)
- [Key v4 Changes](#key-v4-changes)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [shadcn/ui without the default look](#shadcnui-without-the-default-look)
- [Detailed patterns and worked examples](#detailed-patterns-and-worked-examples)

## When to Use

- Creating a component library with Tailwind v4
- Implementing design tokens and theming with CSS-first configuration
- Building responsive and accessible components
- Standardizing UI patterns across a codebase
- Migrating from Tailwind v3 to v4
- Setting up dark mode with native CSS features

## Setup

v4 needs no `tailwind.config.js` and no `content` array: sources are detected automatically (use `@source "../path"` for anything outside the project, such as a package in `node_modules`).

```ts
// vite.config.ts (Vite, React Router, Astro, SvelteKit)
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss()],
})
```

```js
// postcss.config.mjs (Next.js and other PostCSS setups)
// npm install tailwindcss @tailwindcss/postcss postcss
export default {
  plugins: { '@tailwindcss/postcss': {} },
}
```

```css
/* app/globals.css */
@import "tailwindcss";
```

v4.2 added `@tailwindcss/webpack` for plain webpack builds. Sass, Less, and Stylus are not supported alongside v4.

## Key v4 Changes

| v3 Pattern                                    | v4 Pattern                                                                       |
| --------------------------------------------- | -------------------------------------------------------------------------------- |
| `tailwind.config.ts`                          | `@theme` in CSS (a legacy JS config still loads with `@config "./tailwind.config.js"`) |
| `@tailwind base/components/utilities`         | `@import "tailwindcss"`                                                          |
| `darkMode: "class"`                           | `@custom-variant dark (&:where(.dark, .dark *))`                                 |
| `theme.extend.colors`                         | `@theme { --color-*: value }`                                                    |
| `plugins: [require("@tailwindcss/typography")]` | `@plugin "@tailwindcss/typography"`                                            |
| Custom JS plugin utilities                    | `@utility name { ... }`                                                          |
| `safelist`                                    | `@source inline("...")`                                                          |
| `theme(colors.red.500)` in CSS                | `var(--color-red-500)` (`theme()` is deprecated)                                 |
| `bg-[--brand]`                                | `bg-(--brand)`                                                                   |
| `!flex` (important prefix)                    | `flex!` (important suffix)                                                       |
| `shadow-sm` / `shadow`                        | `shadow-xs` / `shadow-sm` (same shift for `rounded`, `blur`, `drop-shadow`)      |
| `outline-none` (invisible outline)            | `outline-hidden` (`outline-none` now sets `outline-style: none`)                 |
| `ring` (3px, blue)                            | `ring-3`; bare `ring` is 1px and `currentColor`                                  |
| `bg-gradient-to-r`                            | `bg-linear-to-r` (old name still works)                                          |
| `bg-opacity-50`, `flex-shrink-0`              | `bg-black/50`, `shrink-0`                                                        |
| `require("tailwindcss-animate")`              | `@import "tw-animate-css"`, or CSS `@keyframes` in `@theme` + `@starting-style`  |

Other default changes: borders and rings default to `currentColor` (always set a color), `space-*` and `divide-*` now use a `:not(:last-child)` selector (prefer `flex` + `gap`), buttons get `cursor: default`, and `hover:` only applies on devices that support hover.

## Quick Start

```css
/* app.css - Tailwind v4 CSS-first configuration */
@import "tailwindcss";

/* Define your theme with @theme */
@theme {
  /* Semantic color tokens using OKLCH for better color perception */
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);

  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);

  --color-secondary: oklch(96% 0.01 264);
  --color-secondary-foreground: oklch(14.5% 0.025 264);

  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);

  --color-accent: oklch(96% 0.01 264);
  --color-accent-foreground: oklch(14.5% 0.025 264);

  --color-destructive: oklch(53% 0.22 27);
  --color-destructive-foreground: oklch(98% 0.01 264);

  --color-border: oklch(91% 0.01 264);
  --color-ring: oklch(14.5% 0.025 264);

  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(14.5% 0.025 264);

  /* Ring offset for focus states */
  --color-ring-offset: oklch(100% 0 0);

  /* Radius tokens */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;

  /* Animation tokens - keyframes inside @theme are output when referenced by --animate-* variables */
  --animate-fade-in: fade-in 0.2s ease-out;
  --animate-fade-out: fade-out 0.2s ease-in;
  --animate-slide-in: slide-in 0.3s ease-out;
  --animate-slide-out: slide-out 0.3s ease-in;

  @keyframes fade-in {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes fade-out {
    from {
      opacity: 1;
    }
    to {
      opacity: 0;
    }
  }

  @keyframes slide-in {
    from {
      transform: translateY(-0.5rem);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  @keyframes slide-out {
    from {
      transform: translateY(0);
      opacity: 1;
    }
    to {
      transform: translateY(-0.5rem);
      opacity: 0;
    }
  }
}

/* Dark mode variant - use @custom-variant for class-based dark mode */
@custom-variant dark (&:where(.dark, .dark *));

/* Dark mode theme overrides */
.dark {
  --color-background: oklch(14.5% 0.025 264);
  --color-foreground: oklch(98% 0.01 264);

  --color-primary: oklch(98% 0.01 264);
  --color-primary-foreground: oklch(14.5% 0.025 264);

  --color-secondary: oklch(22% 0.02 264);
  --color-secondary-foreground: oklch(98% 0.01 264);

  --color-muted: oklch(22% 0.02 264);
  --color-muted-foreground: oklch(65% 0.02 264);

  --color-accent: oklch(22% 0.02 264);
  --color-accent-foreground: oklch(98% 0.01 264);

  --color-destructive: oklch(42% 0.15 27);
  --color-destructive-foreground: oklch(98% 0.01 264);

  --color-border: oklch(22% 0.02 264);
  --color-ring: oklch(83% 0.02 264);

  --color-card: oklch(14.5% 0.025 264);
  --color-card-foreground: oklch(98% 0.01 264);

  --color-ring-offset: oklch(14.5% 0.025 264);
}

/* Base styles */
@layer base {
  * {
    @apply border-border;
  }

  body {
    @apply bg-background text-foreground antialiased;
  }
}
```

How the theming works: `@theme` variables are emitted as CSS variables on `:root` (the ones in use, unless you write `@theme static`), and utilities such as `bg-background` compile to `var(--color-background)`, so redefining the variable under `.dark` re-themes every utility without a `dark:` prefix. An equivalent pattern (used by shadcn/ui) keeps raw values in `:root` and `.dark` and maps them with `@theme inline { --color-background: var(--background); }`; use `inline` whenever a theme variable references another variable. Set the `.dark` class on `<html>` before first paint to avoid a flash (see [advanced-patterns.md](tailwind/advanced-patterns.md#pattern-6-dark-mode-with-css-v4)).

## Core Concepts

### 1. Design Token Hierarchy

```
Brand Tokens (abstract)
    └── Semantic Tokens (purpose)
        └── Component Tokens (specific)

Example:
    oklch(45% 0.2 260) → --color-primary → bg-primary
```

### 2. Component Architecture

```
Base styles → Variants → Sizes → States → Overrides
```

## shadcn/ui without the default look

shadcn/ui (CLI 4.x) copies component source into your repo, so the code is yours to change. Its stock theme, however, is the template look this skill refuses: neutral gray, one radius, soft shadows. Use it for behavior and accessibility, then restyle.

1. **Set up:** `npx shadcn@latest init` in a new or existing project (`--template next|vite|start`, `--base radix|base|aria`, `--preset <name>`). `npx shadcn@latest info` shows the detected setup; `npx shadcn@latest docs <component>` prints current usage.
2. **Add only what the surface needs:** `npx shadcn@latest add dialog dropdown-menu`. Review each added file before use; it is now your code.
3. **Restyle through tokens, not per-component overrides:** edit the semantic variables in `globals.css` (`--background`, `--foreground`, `--primary`, `--accent`, `--border`, `--ring`, `--radius`, and the chart and sidebar sets) to the palette chosen for the brief. Write them in `oklch()`, define the dark theme in the same file, and keep the two-layer primitives-and-roles structure above.
4. **Then change what tokens cannot reach:** the type scale and font families (set the font variables in the root layout), the radius scale (one radius everywhere is the tell), shadows, density, and the component variants in the `cva` definitions. A design built only from stock components with new colors still reads as the default kit.
5. **Keep what works:** the focus management, keyboard behavior, and ARIA in the Radix or Base UI primitives. Restyle around them rather than rebuilding dialogs, menus, and comboboxes.

## Detailed patterns and worked examples

Detailed pattern documentation lives in [tailwind/details.md](tailwind/details.md) (CVA components, compound components, form components, grid and container utilities). Advanced v4 patterns (native CSS animations, dark mode theming, custom utilities, theme modifiers, namespace overrides, and the v3-to-v4 migration checklist) live in [tailwind/advanced-patterns.md](tailwind/advanced-patterns.md). Read them when the summary above is insufficient.

