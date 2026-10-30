# Accessibility (WCAG 2.2 AA)

Read this reference when axe or Lighthouse reports accessibility violations, and before signing off any UI as accessible.

## Contents

- [What automation covers](#what-automation-covers)
- [Severity from axe impact](#severity-from-axe-impact)
- [WCAG 2.2 AA checklist](#wcag-22-aa-checklist)
- [Manual test protocol](#manual-test-protocol)
- [Fix patterns](#fix-patterns)
- [React and Next.js notes](#react-and-nextjs-notes)
- [Sources](#sources)

## What automation covers

axe-core and Lighthouse (which runs axe internally) catch only part of accessibility barriers; published estimates range from about a third to just over half. A score of 100 does not mean WCAG conformance. Treat axe violations as confirmed defects, axe `incomplete` results as items needing manual review, and every criterion marked **manual** below as untested until someone checks it.

## Severity from axe impact

| axe impact | Report severity | Examples |
|------------|-----------------|----------|
| `critical` | Critical | Unnamed buttons or form fields, images without alt, keyboard traps |
| `serious` | High | Insufficient contrast, missing `lang`, links without discernible text |
| `moderate` | Medium | Missing landmarks, heading order, missing `<h1>` |
| `minor` | Low | Redundant roles, minor ARIA misuse |

Raise the severity when the failure sits on a primary flow (sign-up, checkout, navigation).

## WCAG 2.2 AA checklist

Level AA conformance requires every Level A and Level AA criterion. **Auto** means axe or Lighthouse checks part of it; **manual** means a person must verify it.

### Perceivable

- [ ] **1.1.1 Non-text content (A, auto):** Meaningful images have descriptive `alt`; decorative images use `alt=""`; icon-only controls have accessible names.
- [ ] **1.2.1–1.2.5 Media (A/AA, manual):** Prerecorded video has captions and audio description; audio has a transcript; live video has captions.
- [ ] **1.3.1 Info and relationships (A, auto + manual):** Headings, lists, tables, labels, and landmarks are real markup, not styling.
- [ ] **1.3.2 Meaningful sequence (A, manual):** DOM order matches reading order.
- [ ] **1.3.3 Sensory characteristics (A, manual):** Instructions do not rely only on shape, position, or sound.
- [ ] **1.3.4 Orientation (AA, manual):** Content works in portrait and landscape.
- [ ] **1.3.5 Identify input purpose (AA, auto + manual):** Personal-data fields have correct `autocomplete` values. axe flags invalid values but not missing ones.
- [ ] **1.4.1 Use of color (A, manual):** Color is never the only signal (errors, links, status).
- [ ] **1.4.2 Audio control (A, manual):** Auto-playing audio can be paused or muted.
- [ ] **1.4.3 Contrast (AA, auto):** Text contrast is at least 4.5:1; large text (24 px, or 18.66 px bold) at least 3:1.
- [ ] **1.4.4 Resize text (AA, manual):** Content works at 200% zoom.
- [ ] **1.4.5 Images of text (AA, manual):** Real text instead of text baked into images.
- [ ] **1.4.10 Reflow (AA, manual):** No horizontal scrolling at 320 CSS px width.
- [ ] **1.4.11 Non-text contrast (AA, manual):** Control borders, focus indicators, and meaningful graphics reach 3:1.
- [ ] **1.4.12 Text spacing (AA, manual):** No clipping when line, letter, and word spacing increase.
- [ ] **1.4.13 Content on hover or focus (AA, manual):** Tooltips and popovers are dismissible, hoverable, and persistent.

### Operable

- [ ] **2.1.1 Keyboard (A, manual):** Every action works with the keyboard alone.
- [ ] **2.1.2 No keyboard trap (A, manual):** Focus can always leave a component.
- [ ] **2.1.4 Character key shortcuts (A, manual):** Single-key shortcuts can be turned off or remapped.
- [ ] **2.2.1 Timing adjustable (A, manual):** Time limits can be extended.
- [ ] **2.2.2 Pause, stop, hide (A, manual):** Carousels and moving content can be paused.
- [ ] **2.3.1 Three flashes (A, manual):** Nothing flashes more than three times per second.
- [ ] **2.4.1 Bypass blocks (A, auto + manual):** A skip link or landmarks let users skip repeated navigation.
- [ ] **2.4.2 Page titled (A, auto):** Each page has a descriptive, unique `<title>`.
- [ ] **2.4.3 Focus order (A, manual):** Tab order follows the visual and logical order.
- [ ] **2.4.4 Link purpose (A, auto + manual):** Link text makes sense in context; no bare "click here".
- [ ] **2.4.5 Multiple ways (AA, manual):** Pages are reachable by navigation plus search or a sitemap.
- [ ] **2.4.6 Headings and labels (AA, manual):** Headings and labels describe their content.
- [ ] **2.4.7 Focus visible (AA, manual):** Every focusable element shows a visible focus indicator.
- [ ] **2.4.11 Focus not obscured (AA, manual, new in 2.2):** Sticky headers, footers, and banners never fully hide the focused element.
- [ ] **2.5.1 Pointer gestures (A, manual):** Multi-finger or path gestures have single-pointer alternatives.
- [ ] **2.5.2 Pointer cancellation (A, manual):** Actions fire on release, not press.
- [ ] **2.5.3 Label in name (A, auto + manual):** The accessible name contains the visible label text.
- [ ] **2.5.4 Motion actuation (A, manual):** Shake or tilt features have UI alternatives.
- [ ] **2.5.7 Dragging movements (AA, manual, new in 2.2):** Drag interactions (sorting, sliders, maps) have a click or keyboard alternative.
- [ ] **2.5.8 Target size (AA, auto + manual, new in 2.2):** Targets are at least 24×24 CSS px or adequately spaced.

### Understandable

- [ ] **3.1.1 Language of page (A, auto):** `<html lang="…">` is set.
- [ ] **3.1.2 Language of parts (AA, manual):** Passages in another language carry their own `lang`.
- [ ] **3.2.1 On focus / 3.2.2 On input (A, manual):** Focusing or changing a field never triggers unexpected navigation or submission.
- [ ] **3.2.3 Consistent navigation / 3.2.4 Consistent identification (AA, manual):** Shared navigation and controls keep the same order and names.
- [ ] **3.2.6 Consistent help (A, manual, new in 2.2):** Help links, chat, or contact details appear in the same relative place on every page.
- [ ] **3.3.1 Error identification (A, manual):** Errors are described in text and tied to the field.
- [ ] **3.3.2 Labels or instructions (A, auto):** Every input has a visible, programmatic label.
- [ ] **3.3.3 Error suggestion (AA, manual):** Error messages say how to fix the problem.
- [ ] **3.3.4 Error prevention (AA, manual):** Legal, financial, and data-deleting actions can be reviewed, confirmed, or undone.
- [ ] **3.3.7 Redundant entry (A, manual, new in 2.2):** Users are not asked to re-enter data they already gave in the same flow.
- [ ] **3.3.8 Accessible authentication (AA, manual, new in 2.2):** Login allows paste and password managers, or offers passkeys, magic links, or SSO. No step requires a cognitive test such as transcribing distorted text or solving a puzzle unless an alternative exists (object-recognition CAPTCHAs are allowed at AA).

### Robust

- [ ] **4.1.2 Name, role, value (A, auto + manual):** Custom widgets expose correct roles, names, and states; prefer native elements.
- [ ] **4.1.3 Status messages (AA, manual):** Toasts, form results, and loading states are announced through live regions without moving focus.

WCAG 2.2 removed 4.1.1 Parsing; do not report it.

## Manual test protocol

Run these on each audited route after the automated pass:

1. **Keyboard:** Unplug the mouse. Tab through the page, open and close every menu and dialog, submit every form. Watch for lost focus, traps, and hidden focus indicators.
2. **Screen reader:** Use VoiceOver (macOS: Cmd+F5) or NVDA (Windows). List headings and landmarks, then complete the primary flow by ear.
3. **Zoom and reflow:** Zoom to 200%, then set the viewport to 320 px wide. Nothing should clip, overlap, or need horizontal scrolling.
4. **Reduced motion:** Enable the OS reduced-motion setting and confirm large animations stop or simplify.
5. **Target size and contrast spot checks:** Inspect small icon buttons and custom focus rings that automation cannot measure.

When browser automation is available (Playwright MCP or Claude in Chrome), use it for the keyboard pass and accessibility-tree snapshots, and capture screenshots as evidence.

## Fix patterns

**Icon-only button:**

```html
<button type="button" aria-label="Open menu">
  <svg aria-hidden="true" focusable="false"><!-- icon --></svg>
</button>
```

**Visually hidden text** (keeps text available to screen readers):

```css
.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;
}
```

**Visible focus.** Browsers already skip focus rings on mouse clicks for buttons and links, so style `:focus-visible` and never remove outlines with a bare `:focus { outline: none }`:

```css
:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; }
html { scroll-padding-top: 5rem; } /* keeps focused items clear of a sticky header (2.4.11) */
```

**Skip link:**

```html
<a href="#main" class="skip-link">Skip to main content</a>
<main id="main" tabindex="-1">…</main>
```

```css
.skip-link { position: absolute; left: 0; top: -40px; padding: 8px 16px; }
.skip-link:focus { top: 0; }
```

**Labeled field with an associated error:**

```html
<label for="email">Email</label>
<input id="email" type="email" autocomplete="email"
       aria-invalid="true" aria-describedby="email-error">
<p id="email-error">Enter an email address like name@example.com.</p>
```

On submit, move focus to the first invalid field or to an error summary.

**Status announcements:** Render an empty `<div role="status">` once, then change its text content. Use `role="alert"` only for urgent errors.

**Dialogs:** Prefer native `<dialog>` opened with `showModal()`, which traps focus and closes on Escape. For custom dialogs, use `role="dialog"`, `aria-modal="true"`, and `aria-labelledby`, trap focus while open, and return focus to the trigger on close.

**Reduced motion:**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## React and Next.js notes

- Set `lang` on `<html>` in the root `app/layout.tsx`.
- Next.js's ESLint config includes `eslint-plugin-jsx-a11y`; run the project's lint script to catch issues before runtime.
- The App Router announces client-side route changes using the page title, so give every route a distinct `title` through the Metadata API.
- Headless component libraries (Radix UI, React Aria, Headless UI) supply tested keyboard and ARIA behavior; prefer them over hand-built menus, comboboxes, and tabs.
- Do not attach `onClick` to `div` or `span`. Use `<button>` for actions and `<Link>` for navigation.

For qualitative accessibility and design review that tools cannot measure, use the `frontend-design` skill's `reference/audit.md`; for edge cases such as long text, RTL, and error states, use its `reference/harden.md`.

## Sources

- [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/) and [Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [What's new in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [axe-core rule descriptions](https://dequeuniversity.com/rules/axe/)
