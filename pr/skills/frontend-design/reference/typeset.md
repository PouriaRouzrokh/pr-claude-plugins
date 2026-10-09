# Typeset

Typography carries information, hierarchy, and voice. Improve it inside the established visual world; do not replace the identity unless the user asked to.

---

## Contents

- [Visitor mode](#visitor-mode)
- [Two isolated assessments](#two-isolated-assessments)
- [Set the system](#set-the-system)
- [Apply](#apply)
- [Verify](#verify)
- [Technical reference](#technical-reference)

## Visitor mode

- **Persuade + Experience:** display type may carry the voice. Use decisive contrast and responsive scale when the composition benefits.
- **Operate + Read:** stability, scanability, and measure come first. A single well-tuned family and fixed role scale are often right.

If typography replacement would create a new identity, route through [new-work.md](new-work.md) and update the recorded design context. Otherwise preserve confirmed families and improve their use.

## Two isolated assessments

When a sub-agent tool is available and permitted, run these independently; otherwise run them yourself in this order. Do not let scan findings anchor the design assessment.

1. **Typographic assessment:** inspect representative pages and styles. Answer every question below with a file, selector, or computed value:
   - **Authority and fit:** Which faces, weights, and roles are established? Do they fit the product and selected world, or are they unexamined defaults? Is every family necessary?
   - **Hierarchy:** Can heading, body, label, metadata, and data roles be distinguished at a glance? Are adjacent sizes or weights too close to carry different jobs?
   - **Scale and consistency:** Is there a deliberate role scale, or a collection of arbitrary values? Do repeated roles stay identical across screens and states?
   - **Reading:** Does body copy stay within a comfortable 45–75 character measure? Are line height, paragraph rhythm, contrast, and tracking tuned to the actual face, width, language, and surface?
   - **Stress:** What happens with long headings, localization expansion, zoom, narrow containers, missing weights, and font fallback?
   - **Delivery:** Are only used assets loaded? Do fallback metrics, loading strategy, and variable-font settings avoid invisible text and disruptive reflow?
2. **Mechanical scan:** Search the target's markup and styles for the bans in [craft-floor.md](craft-floor.md) (gradient text, side-stripe borders, identical card grids, eyebrow labels, decorative glass, hard offset shadows, glyph icons) and for arbitrary values outside the project's scale. Also list every font family, size, weight, and line-height value in use, including dynamic ones. Synthesize both assessments before editing, noting what each caught alone. A clean scan is a floor, not proof of good typography.

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
- Keep prose in the 45–75ch range. Tune line height inversely with measure: wider lines generally need more leading.
- Compensate light text on dark surfaces on all three perceptual axes: slightly more line height, a touch more tracking, and one step more weight when the face needs it.
- Tune line height to the face, width, language, and contrast, not a universal ratio.
- Keep repeated roles consistent across screens and states.
- Use numeric, tabular, code, and label features when their content benefits.
- Load only used font assets and weights. Provide metric-compatible fallbacks and avoid blocking text.
- Let marketing display type respond to available space when useful; keep dense product and reading surfaces spatially predictable.
- Preserve browser zoom, user font settings, Dynamic Type, and platform text scaling.
- Use paragraph spacing or first-line indentation as the primary paragraph rhythm; combining both usually double-marks the boundary.

Do not make type decorative at the expense of comprehension, or introduce a second family without a clear role it alone can perform.

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

Set measure with `ch` units (`max-width: 65ch`). On light-on-dark text, add 0.05-0.1 to the usual line-height.

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
- Give text links enough padding or line-height for a 44px tap target.
