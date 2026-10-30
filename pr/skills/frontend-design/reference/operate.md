# Operate mode depth (and Read notes)

When design serves the product: app UIs, admin dashboards, settings panels, data tables, tools, authenticated surfaces, anything where the user is in a task. The essentials live in the visitor modes of [new-work.md](new-work.md#4-visitor-modes) and in [craft-floor.md](craft-floor.md); this file is extended depth, written for Operate surfaces. Read surfaces (docs, guides, long-form) take the Read mode plus this file's typography and consistency rules; their prose measure and navigation matter more than component density.

## Contents

- [The product slop test](#the-product-slop-test)
- [Typography](#typography)
- [Color](#color)
- [Layout](#layout)
- [Components](#components)
- [Motion](#motion)
- [What to avoid](#what-to-avoid)
- [Product permissions](#product-permissions)
- [Interaction patterns](#interaction-patterns)

## The product slop test

Familiarity is often a feature here. The test is whether a category-fluent user can trust the interface immediately or must pause at every subtly-off component.

Product UI's failure mode isn't flatness, it's strangeness without purpose: over-decorated buttons, mismatched form controls, gratuitous motion, display fonts where labels should be, invented affordances for standard tasks. The bar is earned familiarity. The tool should disappear into the task.

## Typography

- **One family is often right.** Product UIs don't need display/body pairing. A well-tuned sans carries headings, buttons, labels, body, data.
- **Fixed rem scale, not fluid.** Clamp-sized headings don't serve product UI: users work at a consistent size, and a fluid heading that shrinks in a narrow pane looks worse, not better.
- **Tighter scale ratio.** 1.125–1.2 between steps is typical. More type elements here than on brand surfaces; exaggerated contrast creates noise.
- **Line length still applies for prose** (65–75ch). Data and compact UI can run denser; tables at 120ch+ are fine.

## Color

Product defaults to Restrained. A single surface can earn Committed (a dashboard where one category color carries a report, an onboarding flow with a drenched welcome screen), but Restrained is the floor.

- State-rich semantic vocabulary: hover, focus, active, disabled, selected, loading, error, warning, success, info. Standardize these.
- Accent color used for primary actions, current selection, and state indicators only, not decoration.
- A second neutral layer for sidebars, toolbars, and panels (slightly cooler or warmer than the content surface).

## Layout

- Responsive behavior is structural (collapse sidebar, responsive table, breakpoint-driven columns), not fluid typography.

## Components

Every interactive component has default, hover, focus, active, disabled, loading, and error states; shipping half of them is the most common product-UI gap.

- Skeleton states for loading, not spinners in the middle of content.
- Empty states that teach the interface, not "nothing here."
- Consistent affordances across the surface. Same button shape. Same form-control vocabulary. Same icon style.
- Overlays escape their container. An absolutely positioned dropdown inside an `overflow: hidden` or `overflow: auto` ancestor gets clipped; use `<dialog>` or the Popover API (both render in the top layer), or a portal.

## Motion

- 150–250 ms on most transitions. Users are in flow; don't make them wait for choreography.
- Motion conveys state, not decoration. State change, feedback, loading, reveal: nothing else.
- No orchestrated page-load sequences. Product loads into a task; users don't want to watch it load.

## What to avoid

- Decorative motion that doesn't convey state.
- Inconsistent component vocabulary across screens. If the "save" button looks different in two places, one is wrong.
- Display fonts in UI labels, buttons, data.
- Reinventing standard affordances for flavor (scrollbars that behave differently, unusual form controls, non-standard dialogs). Theming them from the palette (`scrollbar-color`, `accent-color`) is welcome; changing how they work is not.
- Heavy color or full-saturation accents on inactive states.
- A modal as the first thought. Modals interrupt and hide context; try inline and progressive alternatives first.

## Product permissions

Product can afford things brand surfaces can't.

- System fonts and familiar sans defaults.
- Standard navigation patterns: top bar + side nav, breadcrumbs, tabs, command palettes.
- Density. Tables with many rows, panels with many labels, dense information when users need it.
- Consistency over surprise. The same visual vocabulary screen to screen is a virtue; delight is saved for moments, not pages.

## Interaction patterns

### Interactive states

| State | When | Treatment |
|-------|------|-----------|
| Default | At rest | Base styling |
| Hover | Pointer over (not touch) | Subtle color or elevation shift |
| Focus | Keyboard or programmatic focus | Visible ring |
| Active | Being pressed | Pressed in, darker |
| Disabled | Not interactive | Reduced emphasis, no pointer |
| Loading | Processing | Inline spinner or skeleton |
| Error | Invalid | Border, icon, and message |
| Success | Completed | Confirmation |

Hover and focus are different states; keyboard users never see hover.

### Focus rings

Never remove an outline without a replacement. Show rings for keyboard focus with `:focus-visible`:

```css
button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

Rings need 3:1 contrast against adjacent colors, 2-3px thickness, an offset from the element, and the same treatment on every interactive element.

### Forms

Placeholders are not labels; always render a visible `<label>`. Validate on blur, not on every keystroke (password strength is the exception), and style invalid fields with `:user-invalid` so they don't turn red before the user has interacted. Place errors below their field and connect them with `aria-describedby`. `field-sizing: content` (Baseline 2026) lets textareas and inputs grow with their content.

### Overlays

- **Modal dialogs:** use the native `<dialog>` element. `showModal()` puts it in the top layer, makes the page behind it inert, moves focus into it, and closes on Escape. For custom overlays, set `inert` on the content behind.
- **Non-modal overlays** (menus, pickers, disclosures): use the Popover API (Baseline 2025) for light dismiss and top-layer stacking without z-index wars.
- **Declarative wiring:** invoker commands (`commandfor` and `command`, Baseline since December 2025) open dialogs and popovers without JavaScript.
- **Positioning:** CSS anchor positioning (`anchor-name`, `position-anchor`, `position-area`, `position-try-fallbacks`) tethers a popover to its trigger and flips it at viewport edges. The core shipped in every engine by January 2026 (Chrome 125, Safari 26, Firefox 147), but Baseline data still lists the full feature as pending Safari 27; keep a simple fallback position for older browsers, or use Floating UI where broad legacy support matters.

```html
<button commandfor="confirm" command="show-modal">Delete project</button>
<dialog id="confirm">…</dialog>

<button popovertarget="menu" class="menu-trigger">Options</button>
<div id="menu" popover class="menu">
  <button>Rename</button>
  <button>Duplicate</button>
</div>
```

```css
.menu-trigger { anchor-name: --menu-trigger; }
.menu {
  position-anchor: --menu-trigger;
  position-area: block-end span-inline-end;
  position-try-fallbacks: flip-block;
  inset: auto;      /* clear the popover UA centering */
  margin: 4px 0 0;
}
```

- **Custom selects:** prefer the native `<select>`. Customizable select (`appearance: base-select`) ships in Chrome 135+ and Safari 27 but not yet in stable Firefox; opt in with `@supports (appearance: base-select)` so other browsers keep the native control.

### Destructive actions

Prefer undo to confirmation; users click through confirmations without reading. Remove the item immediately, show an undo toast, and delete for real when the toast expires. Reserve confirmation for irreversible, high-cost, or batch actions.

### Keyboard navigation

- **Roving tabindex:** in composite widgets (tabs, menus, radio groups), one item has `tabindex="0"` and the rest `-1`; arrow keys move focus within the group and Tab leaves it.
- **Skip links:** provide `<a href="#main-content">Skip to main content</a>`, visually hidden until focused.

### Gestures

Swipe and long-press gestures are invisible. Hint at them (a partially revealed action, a first-use coach mark) and always provide a visible alternative, such as a menu with the same action.
