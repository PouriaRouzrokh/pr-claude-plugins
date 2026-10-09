---
name: frontend-design
description: Creates distinctive, production-grade frontend interfaces with intentional visual design, choosing aesthetic direction, typography, color, layout, motion, and interface copy that avoid templated AI defaults. Use when building or redesigning web components, pages, landing pages, dashboards, artifacts, posters, or applications; when critiquing, auditing, or polishing an existing UI for hierarchy, accessibility, responsiveness, or performance; or when writing React, Next.js, or Tailwind CSS v4 frontend code. Includes reference playbooks for critique, audit, polish, layout, type, color, animation, UX writing, hardening, onboarding, and design-system extraction, plus Vercel's React and Next.js performance rules.
license: Apache-2.0 (Anthropic frontend-design, impeccable); MIT (Vercel react-best-practices, wshobson tailwind-design-system). See NOTICE.md.
---

# Frontend Design

Approach this as the design lead at a studio known for giving every client a distinct visual identity that is never mistaken for anyone else's. This client has already rejected proposals that felt cliché or templated, and is paying for a distinctive point of view: make deliberate, opinionated choices about palette, typography, and layout that are specific to this brief, and take aesthetic risk where it is justified. Then implement real, working, production-grade code.

## Ground designs in the subject matter

If the brief does not identify the product or subject, identify it yourself before designing and confirm it with the user: propose one concrete subject, the design's audience, and its primary job. Use anything you know about the user's preferences or project as a hint, and read the project's design context if one exists (a `## Design Context` section in CLAUDE.md, or DESIGN.md; [init.md](reference/init.md) creates one). The subject's industry, materials, and vernacular are where distinctive choices come from: a toy for girls aged 8–11 looks nothing like a dashboard for financial analysts. Build with the brief's real content and subject matter throughout.

Name the visitor mode of the surface, because it decides how far the design may go ([details](reference/new-work.md#4-visitor-modes)):

- **Persuade** (landing pages, marketing, pricing): the design is the product; earn attention and action.
- **Operate** (app UI, dashboards, settings, tools): scanability, consistency, and familiar affordances outrank expression ([operate.md](reference/operate.md)).
- **Read** (docs, articles, changelogs): structure for comprehension; the world frames a calm reading column.
- **Experience** (portfolios, galleries, showcases): the work leads from the first viewport.

## Design principles

**Hero.** The first viewport opens with the most characteristic thing in the subject's world, in its most fitting form: a headline, an image, an animation, a live demo, an interactive moment. A big number with a small label, supporting stats, and a gradient accent is the default treatment; use it only if it is truly the best option.

**Typography** carries the personality of the page.
- Use one family or two; if two, make them clearly distinct. Choose typefaces deliberately, not the families you would reach for on any other project ([reflex fonts to question](reference/new-work.md#5-commit-the-world)).
- Set a clear type scale following *The Elements of Typographic Style*, with intentional weights, widths, and spacing. When type is a headline or visual element, make the treatment itself an active part of the design.
- Keep line length under 80 characters (65–75ch for body). Serif text can run slightly longer and wants slightly more line-height than sans.
- Avoid the commonest typographic tells: accenting a single word or phrase in a headline (one italic, bold, or colored word), all-caps labels, and unnecessary labels above content.
- Do not use monospace as a costume for "technical"; reserve it for code, data, and measurement.

**Visual structure is information.** Outlines, borders, numbering, eyebrows, dividers, and labels should encode something about the content, not decorate it. Use numbered markers (01 / 02 / 03) only when the content really is a sequence.

**Color.**
- Commit to a color strategy before choosing colors: Restrained, Committed, Full palette, or Drenched ([details](reference/new-work.md#5-commit-the-world)). A dominant color with sharp accents beats a timid, evenly distributed palette.
- Pick light or dark from the use scene (who, where, under what light), never by category habit or because dark-with-glowing-accents looks "cool".
- Use modern CSS color (`oklch()`, `color-mix()`, `light-dark()`) for predictable ramps and themes ([colorize.md](reference/colorize.md)).
- On colored surfaces, derive secondary text from the surface hue; gray text on color looks washed out.
- No gradient text; emphasis comes from weight and size.

**Layout and space.**
- Create rhythm through varied spacing: tight groups, generous separations, more space above a heading than below it. One value repeated everywhere is monotony.
- Not everything needs a container. Never nest cards inside cards, and never build the page from identical icon-heading-text card grids.
- Decide alignment deliberately; centering everything is a default, not a choice. Asymmetry and intentional grid breaks create emphasis when the content earns them.
- Use fluid spacing with `clamp()` on expressive surfaces and container queries for component-level responsiveness ([layout.md](reference/layout.md)).

**Motion.** Use non-user-triggered motion sparingly, only to draw attention. One orchestrated moment (a page-load sequence or a reveal) lands better than scattered effects; fade-and-slide-up on every section and hover transitions on every card read as AI-generated. Motion that answers a person's action (opening, expanding, confirming) is welcome when it shows what changed. Use exponential ease-out, never bounce or elastic; avoid animating layout properties; animate height through `grid-template-rows` ([animate.md](reference/animate.md)).

**Interaction.**
- Make interactions feel fast: optimistic updates for low-stakes actions, skeletons rather than spinners in content.
- Use progressive disclosure: basic options first, advanced behind clear entry points.
- Design empty states that teach the interface and offer the next action.
- Keep hierarchy in actions: one primary, then secondary, ghost, and text styles. Not every button is primary.
- Reach for a modal only when a task needs interruption or protected focus; inline and progressive alternatives come first.
- Adapt layouts across devices rather than amputating features on mobile ([adapt.md](reference/adapt.md)).

**Written content.** Copy can make a design feel as templated as the visuals. When the brief has no real content, write it with the same care (see [Writing in design](#writing-in-design)).

**CSS hygiene.** Watch selector specificity: it is easy to generate classes that cancel each other out (a type selector like `.section` against an element selector like `.cta`), especially for padding and margin between sections.

## Process: plan, review against the brief, build, critique

### AI design clusters

For calibration, AI-generated design currently clusters around these traits:

1. a warm cream background (near `#F4F1EA`) with a high-contrast serif display and a terracotta or warm-clay accent (often near `#D97757`, Anthropic's own Claude accent, so on a user's brief it reads as a tell);
2. a near-black background with a single bright acid-green or vermilion accent;
3. a broadsheet layout with hairline rules, zero border-radius, and dense newspaper-like columns;
4. the SaaS-card kit: content chopped into identical rounded cards, one border-radius on everything, the same soft grey shadow (`rgba(0,0,0,.1)`) under each, and gradient washes (often purple-to-blue) as decoration;
5. template chrome that appears whatever the subject: a tracked-out ALL-CAPS eyebrow above every heading; meta strings joined with middle dots (`A · B · C`); labels built as `WORD — fragment`; tinted near-black (`#0B0B0B`, `#111`) standing in for black; a monospace face for small data labels; a `→` appended to link and button text.

Each is legitimate for some brief, but they are defaults rather than choices, and they appear regardless of subject. Where the brief pins a visual direction, follow it exactly; the brief's own words always win, including when it asks for one of these looks. Where it leaves an axis free, do not spend that freedom on a default.

### Two passes

1. **Plan.** Brainstorm a compact token system from the brief:
   - **Color:** the core palette as 4–6 named hex values.
   - **Type:** the typefaces and their roles.
   - **Layout:** a layout concept in one-sentence descriptions plus ASCII wireframes to compare options, including alignment (left, center, justified).
   - **Principles:** what makes this page unique.
2. **Review the plan against the brief.** If any part reads like the default you would produce for any similar page (work through a similar prompt and see whether you land in the same place), revise it and say what changed and why.
3. **Build** from the revised plan. Read [craft-floor.md](reference/craft-floor.md) immediately before writing UI code.
4. **Critique** the result (see [Restraint and self-critique](#restraint-and-self-critique)).

For a new surface or a replacement identity, [new-work.md](reference/new-work.md) expands this into a full flow: deriving candidate worlds from the audience's culture, offering directions, and recording the chosen one. For planning without code, use [shape.md](reference/shape.md).

## Craft floor

Build to this floor without announcing it. The brief's own words can earn any item in the Refuse list; your habit cannot. Full list with rationale: [craft-floor.md](reference/craft-floor.md). Where references disagree, the user's explicit request wins, then this file.

**Verify on the built result:**
- **Contrast:** body and placeholder text ≥ 4.5:1, large text ≥ 3:1, controls and focus indicators ≥ 3:1.
- **Type:** body measure 65–75ch, display at most 6rem, tracking no tighter than -0.04em, balanced headings, obvious scale and weight steps. Run the real copy at every breakpoint and fix overflow.
- **States:** default, hover, focus, active, disabled, loading, error, empty, success, with real content and visible keyboard focus.
- **Responsive:** composed down to mobile, not merely shrunk. Reduced motion respected.
- **Browser surfaces:** theme text selection, caret, scrollbars, focus rings, underline offset, and tabular numerals from the palette; browser defaults belong to no design system.
- **Copy:** controls name their action; errors name the problem and the recovery.
- **Coverage:** every brief requirement is present and findable within seconds.

**Refuse by default:**
- Identical icon-heading-text card grids as page structure; nested cards; the hero-metric template.
- An eyebrow or kicker above a heading; `01 / 02 / 03` markers on content that is not a sequence.
- Gradient text; glassmorphism as decoration; colored `border-left`/`border-right` stripes over 1px on cards, alerts, or list items.
- Hard offset shadows (`4px 4px 0`) outside a genuinely neobrutalist world; zero-offset colored glows; a 1px border under a wide soft shadow (the ghost card). Declare elevation once.
- Sparklines, progress rings, and soft-shadowed rounded rectangles standing in for content.
- A system display face (Impact, Arial Black, the platform sans) as the voice of a brand page; source and self-host a real face.
- Unicode glyphs or emoji as an icon system; use one drawn icon library in one stroke and weight.
- Sketch-style SVG illustration, stripe and grid-overlay backgrounds with no subject reason, geometric masks faking organic cutouts.
- Invented claims: prices, customers, benchmarks, testimonials. Label illustrative data as sample data.

## Restraint and self-critique

Spend your boldness in one place. Let one element be the memorable thing, keep everything around it quiet and disciplined, and cut any decoration that does not serve the brief. Consider Chanel's advice: before leaving the house, look in the mirror and remove one accessory.

Critique your work as you build, taking screenshots when the environment supports it; a picture is worth a thousand tokens. Inspect in bounded passes: capture desktop and mobile together, fix everything the round shows in one batch, confirm with at most one more round, then stop. Open-ended self-QA costs more and finds less than a fresh review ([critique.md](reference/critique.md), [audit.md](reference/audit.md), [polish.md](reference/polish.md)).

**The AI slop test.** If you showed this interface to someone and said "AI made this," would they believe you immediately? If so, that is the problem. A distinctive interface makes people ask "how was this made?", not "which AI made this?"

Human designers remember what they tried and push for something new. If you have somewhere to jot notes about the directions you have used for this user, keep them and vary your choices across projects: light and dark, different families, different structures.

## Writing in design

Words appear in a design for one reason: to make it easier to understand and use. They are design content, not decoration, and deserve the same intentionality and minimalism as spacing and color. Before writing anything, ask what the design needs to say and how it can best help the person navigate.

- **Write from the user's side.** Name things by what users understand, not by how the system is built: users manage notifications, not webhook config. Describe what something is or does in plain terms rather than selling it. Specific and legible beats clever.
- **Use active voice and exact actions.** A CTA says exactly what happens: "Save changes," not "Submit." An action keeps its name through the whole flow, so the "Publish" button produces a "Published" toast. Consistent vocabulary is how people learn their way around.
- **Treat failure and emptiness as direction, not mood.** Explain what went wrong and how to fix it, in the interface's voice. Errors never apologize and are never vague. An empty screen is an invitation to act.
- **Keep the tone conversational:** plain verbs, sentence case, no filler, matched to the brand and audience. Say each thing once; an intro that restates its heading should go. Each written element does exactly one job.

Detailed patterns, tables, and localization rules: [clarify.md](reference/clarify.md).

## Multi-Agent Strategy for Complex UI Projects

**Use subagents (default)** for independent, parallel work: separate audits (accessibility, performance, responsiveness), code-explorer agents mapping existing UI patterns before new components, the two isolated assessments in [critique.md](reference/critique.md), a fresh-context final review of a finished build, and browser checks at several viewports.

**Consider agent teams** only when agents must negotiate in real time: multi-page builds where page agents share tokens, component APIs, and navigation; design-system extraction across many pages; or full redesigns where visual and interaction owners must resolve conflicts. Teams are experimental and more expensive; for most frontend work, subagents plus your own synthesis are enough.

## Reference Library

Load references only when the task needs them. Starting points:

- **New page or product:** [new-work](reference/new-work.md) + [craft-floor](reference/craft-floor.md), then [typeset](reference/typeset.md), [colorize](reference/colorize.md), [layout](reference/layout.md) as needed
- **Product UI:** add [operate](reference/operate.md)
- **Review an existing UI:** [critique](reference/critique.md) (UX) or [audit](reference/audit.md) (technical), then the suggested references, then [polish](reference/polish.md)

### Plan and set up

| Reference | Use when |
|-----------|----------|
| [init](reference/init.md) | Capturing durable product context (users, purpose, brand commitments) in the project's CLAUDE.md, once per project. |
| [shape](reference/shape.md) | Planning UX and UI through a discovery interview and a confirmed brief, before any code. |
| [new-work](reference/new-work.md) | Building a new surface or replacing a visual identity: visitor modes, candidate worlds, color strategy, typeface choice, direction contract, finish. |
| [craft-floor](reference/craft-floor.md) | Immediately before writing UI code: the quality floor and the ban list. |
| [operate](reference/operate.md) | App UI, dashboards, settings, and tools: product typography, color, component states, and interaction patterns (focus, forms, dialogs, popovers, keyboard). |

### Design foundations

| Reference | Use when |
|-----------|----------|
| [typeset](reference/typeset.md) | Type hierarchy, scale, pairing, font loading, fluid type, OpenType features. |
| [colorize](reference/colorize.md) | Color strategy and roles, OKLCH ramps, contrast, dark themes, tokens. |
| [layout](reference/layout.md) | Reading order, grouping, spacing rhythm, grids, container queries, touch targets. |
| [animate](reference/animate.md) | Motion thesis, timing, easing, reduced motion, perceived performance. |
| [clarify](reference/clarify.md) | Labels, errors, empty and loading states, voice and tone, localization. |
| [adapt](reference/adapt.md) | Responsive and cross-device adaptation, input methods, safe areas, responsive images. |
| [tailwind-design-system](reference/tailwind-design-system.md) | Tailwind CSS v4 (CSS-first `@theme`) tokens, CVA variants, theming, dark mode. Deeper: [tailwind/details](reference/tailwind/details.md), [tailwind/advanced-patterns](reference/tailwind/advanced-patterns.md). |

### Evaluate

| Reference | Use when |
|-----------|----------|
| [critique](reference/critique.md) | Holistic UX review: Nielsen heuristic scores, cognitive load, personas, prioritized issues. |
| [audit](reference/audit.md) | Technical checks scored across accessibility, performance, theming, responsiveness, and implementation integrity. |

### Adjust intensity

| Reference | Use when |
|-----------|----------|
| [bolder](reference/bolder.md) | A section reads safe or flat; raise it within the existing system. |
| [quieter](reference/quieter.md) | A design is loud or overstimulating; refine without going generic. |
| [distill](reference/distill.md) | A design is cluttered; strip it to its essence. |
| [delight](reference/delight.md) | Adding earned moments of personality and joy. |
| [overdrive](reference/overdrive.md) | Pushing past conventional limits: view transitions, WebGL, scroll-driven motion, virtualized data. |

### Harden and ship

| Reference | Use when |
|-----------|----------|
| [harden](reference/harden.md) | Edge cases: errors, long and empty content, i18n, RTL, network failure. |
| [onboard](reference/onboard.md) | First-run flows, empty states, activation. |
| [optimize](reference/optimize.md) | Loading, rendering, animation, and bundle performance. |
| [extract](reference/extract.md) | Consolidating repeated patterns into components and design tokens. |
| [polish](reference/polish.md) | The final pass: system drift, states, alignment, consistency, cleanup. |

## React & Next.js Best Practices

When building React or Next.js applications, apply Vercel's performance rules. The compiled guide is [react-rules/REACT-BEST-PRACTICES.md](reference/react-rules/REACT-BEST-PRACTICES.md) (70 rules with a table of contents); each rule also has its own file in `reference/react-rules/`, named by category prefix (`async-`, `bundle-`, `server-`, `client-`, `rerender-`, `rendering-`, `js-`, `advanced-`).

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

### Key rules

**Eliminating waterfalls (CRITICAL)**
- Run independent operations with `Promise.all()`, and start nested fetches as soon as their parent resolves ([async-parallel](reference/react-rules/async-parallel.md), [server-parallel-nested-fetching](reference/react-rules/server-parallel-nested-fetching.md)).
- Move `await` into the branch that needs it, and check cheap synchronous conditions before awaiting async flags ([async-defer-await](reference/react-rules/async-defer-await.md), [async-cheap-condition-before-await](reference/react-rules/async-cheap-condition-before-await.md)).
- Stream content with Suspense boundaries ([async-suspense-boundaries](reference/react-rules/async-suspense-boundaries.md)).

**Bundle size (CRITICAL)**
- Import from modules directly, not barrel files ([bundle-barrel-imports](reference/react-rules/bundle-barrel-imports.md)), and keep import paths statically analyzable ([bundle-analyzable-paths](reference/react-rules/bundle-analyzable-paths.md)).
- Load heavy components with `next/dynamic` and defer non-critical third-party scripts ([bundle-dynamic-imports](reference/react-rules/bundle-dynamic-imports.md), [bundle-defer-third-party](reference/react-rules/bundle-defer-third-party.md)).

**Server (HIGH)**
- Authenticate Server Actions like API routes ([server-auth-actions](reference/react-rules/server-auth-actions.md)).
- Never keep request data in shared module state; hoist static I/O to module level instead ([server-no-shared-module-state](reference/react-rules/server-no-shared-module-state.md), [server-hoist-static-io](reference/react-rules/server-hoist-static-io.md)).

**Re-renders (MEDIUM)**
- Never define components inside other components ([rerender-no-inline-components](reference/react-rules/rerender-no-inline-components.md)).
- Derive state during render, not in effects; use primitive effect dependencies ([rerender-derived-state-no-effect](reference/react-rules/rerender-derived-state-no-effect.md), [rerender-dependencies](reference/react-rules/rerender-dependencies.md)).
- Keep expensive updates responsive with `useDeferredValue` and transitions ([rerender-use-deferred-value](reference/react-rules/rerender-use-deferred-value.md), [rerender-transitions](reference/react-rules/rerender-transitions.md)).

**Rendering (MEDIUM)**
- Add resource hints for critical assets and load scripts with `defer` or `async` ([rendering-resource-hints](reference/react-rules/rendering-resource-hints.md), [rendering-script-defer-async](reference/react-rules/rendering-script-defer-async.md)).

Consult the rules when writing components, implementing data fetching, reviewing or refactoring React/Next.js code, or optimizing bundle size and load times.

## Related Skills

### Raster vs Vector Decision

| Need | Format | Skill |
|------|--------|-------|
| Photos, textures, backgrounds, product shots | Raster (PNG/JPEG/WebP) | `generate-image` |
| Icons, logos, illustrations, hero graphics | Vector (SVG) | `generate-svg` |
| Animated web elements (spinners, ambient hero motion) | Vector (SVG) | `generate-svg` |
| Diagrams, infographics | Either | `generate-image` with `pro` for text-heavy pieces; `generate-svg` for simple, editable diagrams |

### `generate-image`

Generates and edits raster images with Google's Nano Banana models. Use it for hero photography, blog headers, product mockups, textures, and edits to existing images. Pick the `pro` model when the image contains words that must render accurately.

### `generate-svg`

Generates SVG markup with a Gemini text model. Types: `hero`, `icon`, `illustration`, `logo`, `component`. Use it when the asset must stay crisp at any size, be themable with `currentColor`, or animate with CSS.

### Browser verification: Playwright

Use the Playwright MCP server (or the browser tools available in the session) to screenshot the UI at mobile, tablet, and desktop widths, exercise forms and hover/focus states, and confirm the design renders as intended. Verify before calling a design finished.

### `agentation`

Adds the Agentation annotation toolbar to a React/Next.js app so the user can click elements and send precise, selector-level feedback to the agent. Use it for iterative design review.

### `generate-video`

Generates short clips with Gemini Omni Flash: hero background loops, product demos, animated keyframes made with `generate-image`. Embed with `autoplay muted loop playsinline`, a poster frame, and a reduced-motion fallback.

### `web-quality-audit`

Measures the built page with Lighthouse and axe (Core Web Vitals, WCAG 2.2 AA, SEO). Use it after [audit](reference/audit.md)'s code-level checks, before shipping.
