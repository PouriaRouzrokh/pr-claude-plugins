---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Apache 2.0. Based on Anthropic's frontend-design skill. See NOTICE.md for attribution.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Design Direction

Commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work—the key is intentionality, not intensity.

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

### Typography
→ *Consult [typography reference](reference/typography.md) for scales, pairing, and loading strategies.*

Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font.

**DO**: Use a modular type scale with fluid sizing (clamp)
**DO**: Vary font weights and sizes to create clear visual hierarchy
**DON'T**: Use overused fonts—Inter, Roboto, Arial, Open Sans, system defaults
**DON'T**: Use monospace typography as lazy shorthand for "technical/developer" vibes
**DON'T**: Put large icons with rounded corners above every heading—they rarely add value and make sites look templated

### Color & Theme
→ *Consult [color reference](reference/color-and-contrast.md) for OKLCH, palettes, and dark mode.*

Commit to a cohesive palette. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

**DO**: Use modern CSS color functions (oklch, color-mix, light-dark) for perceptually uniform, maintainable palettes
**DO**: Tint your neutrals toward your brand hue—even a subtle hint creates subconscious cohesion
**DON'T**: Use gray text on colored backgrounds—it looks washed out; use a shade of the background color instead
**DON'T**: Use pure black (#000) or pure white (#fff)—always tint; pure black/white never appears in nature
**DON'T**: Use the AI color palette: cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds
**DON'T**: Use gradient text for "impact"—especially on metrics or headings; it's decorative rather than meaningful
**DON'T**: Default to dark mode with glowing accents—it looks "cool" without requiring actual design decisions

### Layout & Space
→ *Consult [spatial reference](reference/spatial-design.md) for grids, rhythm, and container queries.*

Create visual rhythm through varied spacing—not the same padding everywhere. Embrace asymmetry and unexpected compositions. Break the grid intentionally for emphasis.

**DO**: Create visual rhythm through varied spacing—tight groupings, generous separations
**DO**: Use fluid spacing with clamp() that breathes on larger screens
**DO**: Use asymmetry and unexpected compositions; break the grid intentionally for emphasis
**DON'T**: Wrap everything in cards—not everything needs a container
**DON'T**: Nest cards inside cards—visual noise, flatten the hierarchy
**DON'T**: Use identical card grids—same-sized cards with icon + heading + text, repeated endlessly
**DON'T**: Use the hero metric layout template—big number, small label, supporting stats, gradient accent
**DON'T**: Center everything—left-aligned text with asymmetric layouts feels more designed
**DON'T**: Use the same spacing everywhere—without rhythm, layouts feel monotonous

### Visual Details
**DO**: Use intentional, purposeful decorative elements that reinforce brand
**DON'T**: Use glassmorphism everywhere—blur effects, glass cards, glow borders used decoratively rather than purposefully
**DON'T**: Use rounded elements with thick colored border on one side—a lazy accent that almost never looks intentional
**DON'T**: Use sparklines as decoration—tiny charts that look sophisticated but convey nothing meaningful
**DON'T**: Use rounded rectangles with generic drop shadows—safe, forgettable, could be any AI output
**DON'T**: Use modals unless there's truly no better alternative—modals are lazy

### Motion
→ *Consult [motion reference](reference/motion-design.md) for timing, easing, and reduced motion.*

Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions.

**DO**: Use motion to convey state changes—entrances, exits, feedback
**DO**: Use exponential easing (ease-out-quart/quint/expo) for natural deceleration
**DO**: For height animations, use grid-template-rows transitions instead of animating height directly
**DON'T**: Animate layout properties (width, height, padding, margin)—use transform and opacity only
**DON'T**: Use bounce or elastic easing—they feel dated and tacky; real objects decelerate smoothly

### Interaction
→ *Consult [interaction reference](reference/interaction-design.md) for forms, focus, and loading patterns.*

Make interactions feel fast. Use optimistic UI—update immediately, sync later.

**DO**: Use progressive disclosure—start simple, reveal sophistication through interaction (basic options first, advanced behind expandable sections; hover states that reveal secondary actions)
**DO**: Design empty states that teach the interface, not just say "nothing here"
**DO**: Make every interactive surface feel intentional and responsive
**DON'T**: Repeat the same information—redundant headers, intros that restate the heading
**DON'T**: Make every button primary—use ghost buttons, text links, secondary styles; hierarchy matters

### Responsive
→ *Consult [responsive reference](reference/responsive-design.md) for mobile-first, fluid design, and container queries.*

**DO**: Use container queries (@container) for component-level responsiveness
**DO**: Adapt the interface for different contexts—don't just shrink it
**DON'T**: Hide critical functionality on mobile—adapt the interface, don't amputate it

### UX Writing
→ *Consult [ux-writing reference](reference/ux-writing.md) for labels, errors, and empty states.*

**DO**: Make every word earn its place
**DON'T**: Repeat information users can already see

---

## The AI Slop Test

**Critical quality check**: If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem.

A distinctive interface should make someone ask "how was this made?" not "which AI made this?"

Review the DON'T guidelines above—they are the fingerprints of AI-generated work from 2024-2025.

---

## Implementation Principles

Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices across generations.

Remember: Claude is capable of extraordinary creative work. Don't hold back—show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

---

## Reference Library

This skill includes extensive reference documentation for specialized tasks. Use these references as needed throughout your design process.

### Design Foundations
These references provide core design knowledge. Consult them when building any frontend:

| Reference | Purpose |
|-----------|---------|
| [typography](reference/typography.md) | Type scales, font pairing, web font loading |
| [color-and-contrast](reference/color-and-contrast.md) | OKLCH, palettes, dark mode, accessibility |
| [spatial-design](reference/spatial-design.md) | Grids, rhythm, container queries |
| [motion-design](reference/motion-design.md) | Timing, easing, reduced motion |
| [interaction-design](reference/interaction-design.md) | Forms, focus, loading patterns |
| [responsive-design](reference/responsive-design.md) | Mobile-first, fluid design |
| [ux-writing](reference/ux-writing.md) | Labels, errors, empty states |
| [tailwind-design-system](reference/tailwind-design-system.md) | Tailwind CSS design tokens, CVA components, theming, dark mode |

### Quality Assessment
Use these references to evaluate and critique your work:

| Reference | When to Use |
|-----------|-------------|
| [audit](reference/audit.md) | Run systematic checks across accessibility, performance, theming, and responsive design. Generates a comprehensive report with severity ratings. |
| [critique](reference/critique.md) | Conduct a holistic design critique evaluating visual hierarchy, information architecture, and emotional resonance. |

**When to apply**: After completing a design checkpoint or before final delivery. Use **audit** for comprehensive technical checks; use **critique** for UX-focused design review.

### Visual Adjustments
Use these references to tune the visual intensity of your designs:

| Reference | When to Use |
|-----------|-------------|
| [bolder](reference/bolder.md) | Amplify designs that are too safe, generic, or underwhelming. |
| [quieter](reference/quieter.md) | Tone down overly bold or aggressive designs for refinement. |
| [colorize](reference/colorize.md) | Add strategic color to monochromatic or bland interfaces. |
| [simplify](reference/simplify.md) | Strip designs to their essence by removing unnecessary complexity. |

**When to apply**: When the design feels off in terms of visual intensity—too bland, too loud, too gray, or too cluttered.

### Specialized Transformations
Use these references for specific enhancement tasks:

| Reference | When to Use |
|-----------|-------------|
| [animate](reference/animate.md) | Add purposeful animations and micro-interactions. |
| [delight](reference/delight.md) | Add moments of joy and personality that make interfaces memorable. |
| [clarify](reference/clarify.md) | Improve unclear UX copy, error messages, and labels. |
| [adapt](reference/adapt.md) | Adapt designs for different screen sizes, devices, or platforms. |
| [onboard](reference/onboard.md) | Design onboarding flows, empty states, and first-time experiences. |
| [harden](reference/harden.md) | Improve resilience: error handling, i18n, text overflow, edge cases. |
| [normalize](reference/normalize.md) | Align designs to match a design system's standards and patterns. |
| [extract](reference/extract.md) | Extract reusable components and design tokens into a design system. |

**When to apply**: When a specific aspect of the design needs focused improvement.

### Final Polish
Use these references before shipping:

| Reference | When to Use |
|-----------|-------------|
| [polish](reference/polish.md) | Final quality pass fixing alignment, spacing, consistency, and details. |
| [optimize](reference/optimize.md) | Improve performance across loading, rendering, animations, and bundle size. |

**When to apply**: After the design is functionally complete, before delivery.

### Setup
| Reference | When to Use |
|-----------|-------------|
| [teach-impeccable](reference/teach-impeccable.md) | One-time setup to gather design context for a project and save to CLAUDE.md. |

---

## React & Next.js Best Practices

When building React or Next.js applications, apply these performance optimization patterns. Detailed rules with code examples are in `reference/react-rules/`.

→ *For the complete guide, consult [react-rules/REACT-BEST-PRACTICES.md](reference/react-rules/REACT-BEST-PRACTICES.md)*

### Priority Categories

| Priority | Category | Impact | When to Apply |
|----------|----------|--------|---------------|
| 1 | Eliminating Waterfalls | CRITICAL | Data fetching, API routes, async operations |
| 2 | Bundle Size Optimization | CRITICAL | Imports, dynamic loading, third-party libraries |
| 3 | Server-Side Performance | HIGH | Server components, caching, serialization |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | SWR, event listeners, localStorage |
| 5 | Re-render Optimization | MEDIUM | State management, memoization, effects |
| 6 | Rendering Performance | MEDIUM | Hydration, SVGs, content-visibility |
| 7 | JavaScript Performance | LOW-MEDIUM | DOM batching, lookups, iterations |
| 8 | Advanced Patterns | LOW | Refs, initialization, stable callbacks |

### Key Rules to Remember

**Eliminating Waterfalls (CRITICAL)**:
- Use `Promise.all()` for independent operations
- Move `await` into branches where actually needed
- Use Suspense boundaries to stream content

**Bundle Size (CRITICAL)**:
- Import directly from modules, not barrel files
- Use `next/dynamic` for heavy components
- Defer non-critical third-party scripts

**Re-renders (MEDIUM)**:
- Extract expensive work into memoized components
- Use primitive dependencies in effects
- Derive state during render, not in effects

**When to consult detailed rules**: When writing new components, implementing data fetching, reviewing code for performance, refactoring existing React/Next.js code, or optimizing bundle size and load times.

---

## Related Skills

These complementary skills extend frontend-design capabilities. Use them when you need specialized functionality beyond core design and implementation.

### Image Generation: `generate-image-nb`

Generate custom images, logos, icons, illustrations, and visual assets using the Nano Banana model (via Gemini CLI).

**When to use**:
- Creating blog featured images, thumbnails, or banners
- Generating app icons, favicons, or UI illustrations
- Designing diagrams, flowcharts, or architecture visuals
- Creating patterns, textures, or decorative graphics
- When the user needs a custom image that can't be found online

**How to invoke**: Use the `generate-image-nb` skill. It provides commands like `/generate`, `/icon`, `/diagram`, `/pattern` for different image types.

**Example scenarios**:
- "Create a hero image for my landing page" → Use generate-image-nb
- "Design an app icon for my productivity tool" → Use generate-image-nb with `/icon`
- "Make a flowchart showing the user auth flow" → Use generate-image-nb with `/diagram`

### Browser Testing: `agent-browser`

Automate browser interactions for testing, screenshots, form filling, and visual verification of your frontend work.

**When to use**:
- Testing the UI after implementation
- Taking screenshots to verify visual changes
- Testing user flows and form interactions
- Verifying responsive design at different viewports
- Debugging layout or interaction issues

**How to invoke**: Use the `agent-browser` skill. Core workflow: `open` → `snapshot -i` → interact using refs → re-snapshot.

**Example scenarios**:
- "Test the login form I just built" → Use agent-browser to fill and submit the form
- "Take screenshots at mobile and desktop sizes" → Use agent-browser with viewport changes
- "Check if the button hover states work" → Use agent-browser to hover and capture

### Visual Feedback: `agentation`

Add a visual feedback/annotation toolbar to Next.js projects for development-time design iteration.

**When to use**:
- Setting up a new Next.js project that needs design feedback tools
- When the user wants to annotate and mark up the UI during development
- For collaborative design review workflows

**How to invoke**: Use the `agentation` skill. It adds a floating toolbar component that only loads in development mode.

**Example scenarios**:
- "Set up design feedback tools for this Next.js app" → Use agentation
- "I want to annotate the UI while developing" → Use agentation