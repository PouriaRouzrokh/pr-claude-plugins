# Typeset

Typography carries information, hierarchy, and voice. Improve it inside the established visual world; do not replace the identity unless the user asked to.

## Contents

- [Visitor mode](#visitor-mode)
- [Assess](#assess)
- [Set the system](#set-the-system)
- [Apply](#apply)
- [Line breaks](#line-breaks)
- [Verify](#verify)
- [Technical reference](#technical-reference)

## Visitor mode

- **Persuade + Experience:** display type may carry the voice. Use decisive contrast and responsive scale when the composition benefits.
- **Operate + Read:** stability, scanability, and measure come first. A single well-tuned family and fixed role scale are often right.

If typography replacement would create a new identity, route through [new-work.md](new-work.md) and update the recorded design context. Otherwise preserve confirmed families and improve their use.

## Assess

Do the typographic read first and the mechanical scan second, so scan output doesn't anchor your judgment. For a large surface, the two can run as parallel subagents.

1. **Typographic assessment:** inspect representative pages and styles. Answer every question below with a file, selector, or computed value:
   - **Authority and fit:** Which faces, weights, and roles are established? Do they fit the product and selected world, or are they unexamined defaults? Is every family necessary?
   - **Hierarchy:** Can heading, body, label, metadata, and data roles be distinguished at a glance? Are adjacent sizes or weights too close to carry different jobs?
   - **Scale and consistency:** Is there a deliberate role scale, or a collection of arbitrary values? Do repeated roles stay identical across screens and states?
   - **Reading:** Does body prose sit at a 65–75 character measure (narrow columns down to about 45ch are acceptable)? Are line height, paragraph rhythm, contrast, and tracking tuned to the actual face, width, language, and surface?
   - **Stress:** What happens with long headings, localization expansion, zoom, narrow containers, missing weights, and font fallback?
   - **Delivery:** Are only used assets loaded? Do fallback metrics, loading strategy, and variable-font settings avoid invisible text and disruptive reflow?
2. **Mechanical scan:** List every font family, size, weight, line-height, and letter-spacing value in use, including dynamic ones, and flag values outside the project's scale. Check the typographic refusals in [craft-floor.md](craft-floor.md): gradient text, monospace as costume, tracking tighter than -0.04em, eyebrow labels, single accented words in headlines, and a system display face on a brand page. Synthesize both assessments before editing, noting what each caught alone. A clean scan is a floor, not proof of good typography.

## Set the system

Before editing, state:

- the roles the interface needs;
- the intended contrast between those roles;
- the reading measure and density;
- which existing faces and weights are authoritative;
- any performance, localization, or accessibility constraints.

Use the fewest roles and families that make the hierarchy unmistakable. Combine size, weight, space, and tone deliberately instead of asking size alone to do all the work. Role names and tokens should describe purpose rather than values.

## Apply

- Keep body copy comfortably readable and zoomable. Use 1rem / 16px as the ordinary web body floor unless a dense role, platform convention, or user setting justifies otherwise.
- Keep body prose at 65–75ch; narrower columns (sidebars, multi-column layouts) can go down to about 45ch. Wider lines need more leading.
- Compensate light text on dark surfaces: slightly more line height and a touch more tracking, then judge weight on the render. Light-on-dark can bloom and look heavier, or thin out under grayscale antialiasing; adjust weight one step in whichever direction the screenshot needs, and avoid hairline weights.
- Tune line height to the face, width, language, and contrast, not a universal ratio.
- Keep repeated roles consistent across screens and states.
- Use numeric, tabular, code, and label features when their content benefits.
- Load only used font assets and weights. Provide metric-compatible fallbacks and avoid blocking text.
- Let marketing display type respond to available space when useful; keep dense product and reading surfaces spatially predictable.
- Preserve browser zoom, user font settings, Dynamic Type, and platform text scaling.
- Use paragraph spacing or first-line indentation as the primary paragraph rhythm; combining both usually double-marks the boundary.
- Balance headings with `text-wrap: balance` (Baseline 2024) and reduce orphans in prose with `text-wrap: pretty` (Chromium and Safari; Firefox falls back to normal wrapping, which is harmless).

Line breaks are part of the typography ([Line breaks](#line-breaks)).

Do not make type decorative at the expense of comprehension, or introduce a second family without a clear role it alone can perform.

## Line breaks

After Matthew Butterick's *Practical Typography*, paraphrased.

- Set `text-wrap: balance` on headings and short centered blocks, and `text-wrap: pretty` on body copy. Both are progressive: a browser that ignores them keeps its default wrap.
- `pretty` pulls a word down beside a lone last word. It does not fill the last line, and a two-word tail is fine.
- In a column too narrow for either to help, edit the copy or widen the column.
- Break a heading by hand only between phrases, and check the break at every width the heading renders at. A hard break that lands mid-line on a phone is worse than the default wrap.
- An uneven break can carry meaning (a headline landing on one word for weight, a poster line, a pull quote). Make it deliberate with a hard break or a wrap set on that element, and keep it rare. Automated checks for a lone last word (a straggler) or a stub on a heading's last line are advisory for this reason.

## Verify

- Primary, secondary, body, and metadata roles are recognizable without reading the copy.
- Long text remains comfortable across relevant widths and languages.
- The typography belongs to the product and its established world.
- Loading does not create disruptive reflow or invisible text.
- Zoom, text scaling, focus, contrast, and reduced viewport paths remain usable.
- A final mechanical scan has no unexplained findings.

Answer each item with rendered or source evidence, then repeat the scan. Do not substitute a bare “yes” for verification.

When the hierarchy holds, finish with a polish pass ([polish.md](polish.md)).

## Technical reference

Concrete values and patterns for applying the guidance above.

### Scale and rhythm

Use fewer sizes with more contrast. Many sizes that sit close together (14, 15, 16, 18px) produce muddy hierarchy. A five-step role scale covers most interfaces:

| Role | Typical size | Use |
|------|--------------|-----|
| xs | 0.75rem | Captions, legal |
| sm | 0.875rem | Secondary UI, metadata |
| base | 1rem | Body text |
| lg | 1.25-1.5rem | Subheadings, lead text |
| xl+ | 2-4rem | Headlines, display |

Common ratios: 1.125-1.2 for dense product UI, 1.25 (major third), 1.333 (perfect fourth), or 1.5 (perfect fifth) for expressive surfaces. Pick one and commit.

For vertical rhythm, derive spacing from the body line-height: with `line-height: 1.5` on 16px type (24px), vertical spacing in multiples of 24px makes text and space share one foundation.

Set measure with `ch` units (`max-width: 65ch`). On light-on-dark text, add 0.05–0.1 to the usual line-height.

`text-box: trim-both cap alphabetic` trims the space above cap height and below the baseline so text aligns optically with icons and box edges (Chromium and Safari; harmless where unsupported).

### Families and pairing

One well-chosen family in several weights often builds cleaner hierarchy than two competing typefaces. Add a second family only for genuine contrast, and contrast on more than one axis: serif against sans (structure), geometric against humanist (personality), condensed display against wide body (proportion). Never pair two faces that are similar but not identical, such as two geometric sans-serifs.

The system stack (`system-ui, -apple-system, "Segoe UI", sans-serif`) looks native, loads instantly, and suits product UI where performance outranks personality.

### Font loading

Late-loading fonts reflow text. Show text immediately and match fallback metrics so the swap does not shift layout:

```css
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;
}

/* Fallback tuned to the custom face's metrics */
@font-face {
  font-family: 'CustomFont-Fallback';
  src: local('Arial');
  size-adjust: 105%;
  ascent-override: 90%;
  descent-override: 20%;
  line-gap-override: 10%;
}

body {
  font-family: 'CustomFont', 'CustomFont-Fallback', sans-serif;
}
```

Tools such as [Fontaine](https://github.com/unjs/fontaine) or `next/font` calculate these overrides automatically.

### Fluid type

`clamp(min, preferred, max)` scales display type with the viewport. The middle value (for example `5vw + 1rem`) sets the scaling rate; the rem offset keeps it from collapsing on small screens. Do not use fluid sizing for button text, labels, dense product UI, or anywhere you need exact control at a breakpoint.

### OpenType features

```css
.data-table { font-variant-numeric: tabular-nums; }      /* aligned figures */
.recipe-amount { font-variant-numeric: diagonal-fractions; }
abbr { font-variant-caps: all-small-caps; }
code { font-variant-ligatures: none; }
body { font-kerning: normal; }
```

Check which features a font supports with [Wakamai Fondue](https://wakamaifondue.com/).

### Tokens and accessibility

- Name type tokens by role (`--text-body`, `--text-heading`), not value (`--font-size-16`). Include stacks, sizes, weights, line-heights, and tracking.
- Never disable zoom (`user-scalable=no`). If the layout breaks at 200% zoom, fix the layout.
- Use `rem` or `em` for font sizes so user settings apply; keep body text at 16px or larger.
- Give standalone text links (navigation, buttons styled as links) at least a 24×24px target, 44px for primary touch controls. Links inside a sentence are exempt from WCAG's target-size rule.
