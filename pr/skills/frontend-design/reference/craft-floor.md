# Craft floor

Load this after the direction is settled, and build to it without announcing the checklist. The user's explicit request and a committed visual world override anything here; your own habit does not.

## Verify

Each item is a check on the built result, not an intention. Run them together in the batched inspection rounds described in SKILL.md; they share one render.

- **Contrast (WCAG 2.2 AA):** body and placeholder text ≥4.5:1; large text (24px, or 18.66px bold) ≥3:1; controls, icons, and focus indicators ≥3:1 against adjacent colors. On colored surfaces, tint secondary text from that hue or the foreground rather than using gray.
- **Depth:** shadows carry an offset and a soft blur. A zero-offset colored halo is decoration.
- **Spacing:** tight groups, generous separation, more space above a heading than below it. Read the computed values.
- **Type:** body measure 65–75ch, display at most 6rem, tracking no tighter than -0.04em, headings balanced (`text-wrap: balance`), obvious scale and weight steps. Run the real copy at every breakpoint and fix what overflows.
- **Motion:** one authored moment, not scattered effects and not one identical entrance on every section. Exponential ease-out from an already-visible default. Transform and opacity are the safe base; blur, clip-path, mask, and shadow are available when they stay smooth on the target device. Avoid animating layout properties (`width`, `height`, `top`, `left`, margins).
- **States:** default, hover, focus, active, disabled, loading, error, empty, success. Real content, working controls, responsive composition, visible keyboard focus. Reduced motion respected.
- **Browser surfaces:** the parts you did not draw still carry the design. Text selection (`::selection`), the caret (`caret-color`), scrollbar colors (`scrollbar-color`), focus rings, underline offset, form-control accents (`accent-color`), and tabular numerals in data all ship with browser defaults that belong to no design system. Theme them from the palette; it is the cheapest signal that a page was built rather than assembled, and the one most often skipped.
- **Copy:** the product's own language. Controls name their action; errors name the problem and the recovery.
- **Coverage:** every brief requirement is present and findable within seconds.

## Refuse

These are the category's defaults, not absolute bans: the brief's own words can earn any of them. Reaching for one when the axis is free means you were not deciding; when you catch one, rewrite the element rather than softening it.

Page scaffolds:

- Same-size cards of icon plus heading plus text as the page structure. Cards are the lazy container; never nest a card inside a card.
- The hero-metric template: big number, small label, supporting stats, accent.
- A kicker or eyebrow label above a heading. The heading carries its own weight; delete the label unless the brief asks for one.
- Section numbers (01 / 02 / 03) unless the sequence itself carries information the reader needs.
- A modal for a task that needs neither interruption nor protected focus.

Surface habits:

- Gradient text. Emphasis comes from weight or size.
- Glass and blur as decoration rather than as a specific effect.
- A colored `border-left` or `border-right` thicker than 1px on cards, list items, callouts, or alerts.
- Hard offset shadows (`box-shadow: 4px 4px 0`) outside a world that is actually neobrutalist. The zero-blur block shadow is a costume, not a depth system. Treat a 4px-or-larger hard offset as advisory rather than a failure: keep it when the world is deliberately neobrutalist and say so.
- Sparklines, progress rings, and soft-shadowed rounded rectangles standing in for content.
- Monospace as a costume for "technical" rather than for code, data, or measurement.
- A system display face (Impact, Arial Black, the platform sans) as the display voice of a brand page. Source and self-host a face whose character matches the direction; the closest installed font is not a fallback for a brand voice. (System stacks are fine for product UI; see [operate.md](operate.md).)
- Unicode glyphs or emoji standing in for an icon system. Use one drawn icon library, or authored SVG, in one consistent stroke and weight.
- Geometric masks standing in for organic contours. A circle, polygon, or radial-gradient cutout approximating a photographic subject's edge reads worse than omitting the effect. Derive an alpha matte from the actual image, or produce a cut-out asset.
- Light or dark picked by category. Pick it from the use scene: who, where, under what ambient light.

Craft details:

- Tracking stops at -0.04em; -0.02 to -0.03em usually reads better on display type.
- Declare elevation once, with a border or a shadow. A 1px border under a wide soft shadow is the ghost card. Vary radii by role (small controls, cards, sheets) rather than one radius everywhere; reserve pill shapes for small controls.
- Real illustration or none. Sketch-style SVG scenes, `loose-sketch` or `doodle` class names, and `feTurbulence` grain read as amateur. This rules out SVG imitating pictures, not SVG doing geometry: crisp vector shapes, diagrams, animated linework, and shader effects remain first-class. A shaded, perspective, or figure-bearing illustration is a picture even in line-art style.
- Backgrounds are surfaces, textured only from the subject's world. `repeating-linear-gradient` stripes and two-axis grid overlays need an actual canvas, map, blueprint, or measuring tool under them.
- Claims and configuration come from supplied facts; label illustrative values as sample data.

The floor holds the mechanics; it never picks the direction. With every check green, spend the page on the committed world, and when torn between refined and committed, commit.
