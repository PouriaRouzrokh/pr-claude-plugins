# Harden

Designs that only work with perfect data are not production-ready. Harden the interface against the inputs, errors, languages, and network conditions real users bring. Empty-state and error copy are covered in [clarify.md](clarify.md) and [onboard.md](onboard.md); this file covers the structural and technical side.

## Contents

- [Assess](#assess)
- [Text overflow and wrapping](#text-overflow-and-wrapping)
- [Internationalization](#internationalization)
- [Errors and failure](#errors-and-failure)
- [Edge cases and boundaries](#edge-cases-and-boundaries)
- [Input validation](#input-validation)
- [Accessibility resilience](#accessibility-resilience)
- [Verify](#verify)

## Assess

List the conditions the target will meet, then check each one:

- **Extreme content:** very long and very short text, empty values, large numbers (millions, billions), 1,000+ list items, 50+ options, no data at all.
- **Failure:** offline, slow, timeouts; API errors (400, 401, 403, 404, 409, 429, 500); validation and permission errors; concurrent edits.
- **Languages:** long translations (German runs about 30% longer than English), RTL scripts (Arabic, Hebrew), CJK, emoji, and locale formats for dates, numbers, and currency.

## Text overflow and wrapping

```css
/* Single line with ellipsis */
.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* Multi-line clamp (the prefixed form is the interoperable one today) */
.clamp-3 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
}

/* Let long words and URLs break instead of overflowing */
.prose { overflow-wrap: break-word; hyphens: auto; } /* hyphens needs a lang attribute */
.user-content { overflow-wrap: anywhere; }

/* Flex and grid children default to min-width: auto and refuse to shrink */
.flex-child, .grid-child { min-width: 0; }
```

- Truncated text needs a way to read the whole value (a tooltip, an expanded view, or a title attribute at minimum).
- Keep body text at 16px or larger on mobile; iOS Safari zooms the page when a focused input's font size is under 16px.
- Check 200% zoom and 400% zoom at a 1280px viewport (WCAG reflow: content must work at 320 CSS px wide without two-dimensional scrolling).
- Let containers grow with their text; avoid fixed heights on anything holding copy.

## Internationalization

- **Expansion:** budget 30–40% extra space, use layouts that size to content, and avoid fixed widths on buttons and labels (`px-4` rather than `w-24`).
- **RTL:** use logical properties (`margin-inline-start`, `padding-inline`, `border-inline-end`, `inset-inline-start`) instead of left/right. Mirror directional icons with `:dir(rtl) .arrow { transform: scaleX(-1); }`; leave non-directional icons (play, check, clock) alone.
- **Arabic-script languages** (Arabic, Persian, Urdu, Pashto, Kurdish):
  - Preserve Zero-Width Non-Joiner (U+200C). Persian and Kurdish use it between compound-word parts to break cursive joining while keeping the word together; a sanitizer or filter that strips it changes meaning.
  - Handle Yeh and Kaf variants. Persian uses ی (U+06CC) and ک (U+06A9); Arabic uses ي (U+064A) and ك (U+0643). Store the original form; for search and validation treat the pairs as equivalent so an Arabic keyboard matches Persian text.
  - Use locale-aware digits through `Intl.NumberFormat` (`new Intl.NumberFormat('fa-IR').format(1234)` gives ۱٬۲۳۴) instead of hardcoding Western digits.
  - Respect calendars: Persian users expect Solar Hijri, many Arabic-speaking users expect Hijri. Use `Intl.DateTimeFormat` with the locale or `-u-ca-` extension (`'ar-SA-u-ca-islamic'`).
- **Scripts:** serve UTF-8 everywhere and choose fonts (or fallbacks) that cover the target scripts; CJK text needs line-breaking rules (`word-break: keep-all` for Korean, `line-break: strict` where appropriate).
- **Formats:** use the `Intl` APIs instead of hand-built strings:

```js
new Intl.DateTimeFormat('de-DE').format(date);                                // 15.1.2026
new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(1234.56); // $1,234.56
new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(-1, 'day');     // yesterday
```

- **Plurals:** never build plurals with `count !== 1 ? 's' : ''`. Use the project's i18n library or `Intl.PluralRules`, which handles languages with several plural forms.

## Errors and failure

- **Network:** say what failed, keep the user's input, offer a retry, and handle timeouts. Cancel stale requests (`AbortController`) when the user navigates or retypes.
- **Forms:** show errors inline next to the field, keep everything the user entered, and do not block submission on rules the server will check anyway.
- **By status:** 400 → field-level validation messages; 401 → re-authenticate and return the user to where they were; 403 → explain the missing permission and who can grant it; 404 → a not-found state with a way forward; 409 → show the conflict and let the user choose; 429 → say when to retry; 5xx → a plain explanation that the problem is on the server, plus a retry or support path.
- **Containment:** one failing widget should not blank the page. Use error boundaries (or equivalent) around independent regions.
- **Progressive enhancement:** server-rendered content and native links and forms keep working when JavaScript is slow or fails; feature-detect (`@supports`, `'x' in window`) rather than browser-sniff.

## Edge cases and boundaries

- **Empty:** first use, no results, filtered to nothing, no permission, and failed-to-load each need their own state and next action.
- **Loading:** initial load, pagination, and refresh; name what is loading and reserve its space so nothing shifts.
- **Large datasets:** paginate or virtualize; never render 10,000 rows at once.
- **Concurrency:** disable or debounce submit while a request is in flight, make writes idempotent where possible, roll back optimistic updates on failure, and surface conflicts instead of silently overwriting.
- **Permissions:** read-only and no-access states explain why and how to get access.
- **Interrupted gestures** (custom sliders, drag surfaces, scrollable control strips): when a second pointer lands mid-drag, the browser cancels the gesture to scroll (`pointercancel`), capture is lost (`lostpointercapture`), the pointer is released outside the control, or the window blurs, clear the dragging state and release capture. Set `touch-action` on drag surfaces so the browser knows which axis it owns. After each interruption, the next drag must work without a reload.

## Input validation

- Use native constraints first (`required`, `type="email"`, `maxlength`, `pattern`, `inputmode`, `autocomplete`) and connect hints with `aria-describedby`.
- Style errors with `:user-invalid` so fields don't turn red before the user has interacted with them.
- Validate again on the server, always; client-side checks are for convenience, not security.

```html
<label for="username">Username</label>
<input id="username" name="username" required maxlength="30"
       pattern="[A-Za-z0-9_]+" autocomplete="username" aria-describedby="username-hint">
<p id="username-hint">Letters, numbers, and underscores, up to 30 characters.</p>
```

## Accessibility resilience

- **Keyboard:** everything reachable and operable, logical order, focus moved into and restored out of dialogs, skip link on long pages.
- **Screen readers:** semantic HTML first, accessible names on every control, live regions (`aria-live="polite"`) for async results and errors.
- **Forced colors:** test with Windows contrast themes (`@media (forced-colors: active)`); borders and focus outlines must survive when backgrounds and shadows are stripped, and meaning must not rely on color alone.
- **Resources:** clean up listeners, timers, subscriptions, and pending requests when components unmount.

## Verify

Exercise each case, preferably in the browser:

- 100+ character names, emoji in every text field, an RTL language, CJK text.
- Offline and throttled network; forced API errors for each status the UI handles.
- 0, 1, and 1,000+ items; empty and filtered-to-nothing states.
- Submit clicked ten times quickly; two tabs editing the same record.
- Interrupted gestures: second finger mid-drag, scroll across the control, release outside it, switch windows; then drag again.
- Keyboard-only pass, a screen-reader spot check, forced-colors mode, 200% zoom.

Say what produced the evidence (emulated viewport, synthesized touch, which engine, physical device) and name what stayed untested; Chromium emulation does not prove Safari behavior. Add automated coverage where the project's runner allows: unit tests for edge-case formatting, end-to-end tests for error paths, and axe checks.

When edge cases are covered, finish with a polish pass ([polish.md](polish.md)).
