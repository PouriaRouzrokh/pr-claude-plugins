# Layout

Layout turns product priority into reading order, grouping, rhythm, and usable space. Diagnose the structural problem before moving boxes.

---

## Contents

- [Visitor mode](#visitor-mode)
- [Two isolated assessments](#two-isolated-assessments)
- [Set the spatial thesis](#set-the-spatial-thesis)
- [Apply](#apply)
- [Verify](#verify)
- [Technical reference](#technical-reference)

## Visitor mode

- **Persuade + Experience:** composition may be asymmetric, fluid, or intentionally disruptive when the selected world earns it.
- **Operate + Read:** predictable structure, stable density, and navigable linearity are affordances.

Preserve the established visual world. A layout pass changes structure inside it; identity replacement belongs to [new-work.md](new-work.md).

## Two isolated assessments

When a sub-agent tool is available and permitted, run these independently; otherwise run them yourself in this order.

1. **Layout assessment:** inspect representative states and viewports. Answer every question below with rendered or source evidence:
   - **Reading order:** Apply the squint test. With detail blurred, can you still identify the primary element, the secondary element, and the major groups in order?
   - **Grouping:** Are related items close and distinct groups separated, or are containers compensating for weak proximity?
   - **Rhythm:** Do tight and generous intervals create a deliberate cadence, or is one spacing value repeated until everything has equal weight?
   - **Structure:** Does the topology match the content and task? Are repeated cards, columns, or sections genuinely equivalent, or merely a framework default?
   - **Density:** Does the amount of information per region fit use frequency, decision complexity, and visitor mode?
   - **Adaptation:** At narrow, intermediate, wide, zoomed, and localized states, what reorders, collapses, wraps, scrolls, or remains fixed? Does DOM and focus order still agree with the visual order?
   - **Extremes:** Do long content, empty states, overlays, sticky elements, safe areas, and small touch targets expose structural failures?
2. **Mechanical scan:** Search the target's markup and styles for the bans in [craft-floor.md](craft-floor.md) (gradient text, side-stripe borders, identical card grids, eyebrow labels, decorative glass, hard offset shadows, glyph icons) and for arbitrary values outside the project's scale. Also inspect arbitrary spacing, overflow, stacking, and container behavior. Keep mechanical evidence out of the first assessment, then synthesize both passes before editing. A clean scan cannot prove hierarchy or rhythm.

## Set the spatial thesis

Before editing, name:

- the primary reading or task path;
- what belongs together and what must separate;
- which element leads and which supports;
- the intended density and spacing rhythm;
- how the structure changes across containers, viewports, input modes, and content extremes.

Choose the simplest structural model that expresses those relationships. Use layout primitives according to the relationships they control, and name reusable spacing and container roles semantically.

## Apply

- Group by meaning. Use proximity before adding containers or decoration.
- Create rhythm through deliberate contrast between tight and generous intervals.
- Use a documented spacing scale rather than one-off values. A 4-unit base usually provides the useful middle steps that an 8-only scale misses.
- Let hierarchy follow product priority, not framework defaults.
- Keep distinct content visually distinct without turning every group into an isolated component.
- Make responsive behavior structural: reorder, collapse, reflow, or reveal based on what remains important.
- Prefer container-aware components when the same component appears in different contexts.
- Use `gap` for sibling rhythm when it expresses the relationship more directly than child margins.
- Keep touch targets usable even when their visible marks are small.
- Use depth only when it clarifies state or hierarchy.
- Make optical corrections only after inspecting the rendered result.

Variation is not a goal by itself. Repetition should support recognition; break it only when content or priority changes.

## Verify

- The squint test still reveals the primary, secondary, and major groups in order.
- The reading and task path remains clear at every supported size.
- Related content groups naturally; unrelated content does not blur together.
- Tight and generous spacing create intentional rhythm instead of monotonous repetition.
- Density matches use frequency and content complexity.
- Long text, empty states, localization, zoom, and dynamic content do not break the structure.
- Keyboard, touch, and assistive-technology order agree with the visual order.
- A final mechanical scan has no unexplained findings.

Answer each item with rendered or source evidence, then repeat the scan. Do not substitute a bare “yes” for verification.

When the structure holds, finish with a polish pass ([polish.md](polish.md)).

## Technical reference

Concrete values and patterns for applying the guidance above.

### Spacing scale

A 4px base gives the useful middle steps an 8-only scale lacks: 4, 8, 12, 16, 24, 32, 48, 64, 96px. Name tokens by relationship (`--space-sm`, `--space-lg`), not value (`--spacing-8`). Use `gap` for sibling spacing; it avoids margin collapse and cleanup hacks.

### Grids

`grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` gives a responsive grid without breakpoints: columns of at least 280px, as many as fit, leftovers stretched. For complex page layouts, use named `grid-template-areas` and redefine them at breakpoints.

### Hierarchy dimensions

Size alone makes weak hierarchy. Combine two or three of these:

| Tool | Strong | Weak |
|------|--------|------|
| Size | 3:1 ratio or more | under 2:1 |
| Weight | Bold against regular | Medium against regular |
| Color | High contrast | Similar tones |
| Position | Top or leading edge | Bottom or trailing edge |
| Space | Surrounded by space | Crowded |

### Container queries

Viewport queries are for page layout; container queries are for components.

```css
.card-container { container-type: inline-size; }

.card { display: grid; gap: var(--space-md); }

@container (min-width: 400px) {
  .card { grid-template-columns: 120px 1fr; }
}
```

The same card stays compact in a sidebar and expands in the main column without viewport hacks.

### Optical adjustments

- Text set at `margin-left: 0` can look indented because of side bearings; a small negative margin (around `-0.05em`) aligns it optically.
- Geometrically centered icons often look off-center: shift play icons right and arrows toward their direction.

### Touch targets

Keep interactive targets at least 44x44px even when the visible mark is smaller:

```css
.icon-button { position: relative; width: 24px; height: 24px; }
.icon-button::before { content: ''; position: absolute; inset: -10px; }
```

### Depth and stacking

Define a semantic z-index scale (dropdown, sticky, modal backdrop, modal, toast, tooltip) instead of arbitrary numbers, and a consistent elevation scale for shadows. Keep shadows subtle: if you notice the shadow before the object, it is too strong.
