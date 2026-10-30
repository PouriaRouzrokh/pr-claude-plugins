# New visual work

Use this flow for a new surface or a replacement visual identity. Product truth lives in the project's design context (see [init.md](init.md)); durable visual decisions live in DESIGN.md or a `### Visual System` subsection of that context, when the project keeps one.

## Contents

- [1. Decide what is already true](#1-decide-what-is-already-true)
- [2. Ask what will change the work](#2-ask-what-will-change-the-work)
- [3. Choose the right amount of invention](#3-choose-the-right-amount-of-invention)
- [4. Visitor modes](#4-visitor-modes)
- [5. Commit the world](#5-commit-the-world)
- [6. Record the direction](#6-record-the-direction)
- [7. Build with full commitment](#7-build-with-full-commitment)
- [8. Inspect and finish](#8-inspect-and-finish)

## 1. Decide what is already true

Read the design context, representative code, tokens, components, and assets.

- **Redesign:** preserve product truth, content, function, constraints, and explicit brand commitments; replace the old visual world rather than polishing it. The old look is evidence of what the subject is, not authority over what it becomes.
- **Established world:** inherit it. A missing DESIGN.md does not erase a coherent identity already in code.
- **Incomplete brand:** preserve confirmed assets and recognizable traits, then expand the system with the user for this surface.
- **No visual authority:** create a new world with the user.

A section, component, feature, or state inside an established surface inherits that surface. Never turn a local addition into a new identity exercise.

## 2. Ask what will change the work

Before implementation, ask the user with the AskUserQuestion tool: two or three related questions, or a compact confirmation when the request is precise. Skip settled facts, not the confirmation. When you will also offer directions (section 3), keep the total to two rounds.

- **Persuade:** who must act, what they should believe, which real proof, content, or assets earn that belief.
- **Operate:** the task, information, important states, frequency, constraints.
- **Read:** the reader's question, source material, structure, wayfinding.
- **Experience:** what leads, how exploration unfolds, which interaction or transition matters.

Across modes, ask what success looks like, what must remain untouched, and what would make a polished result feel wrong. Never ask for CSS values or canned aesthetic lanes.

## 3. Choose the right amount of invention

**Extend an existing surface.** Inherit its world and composition. Resolve only the new purpose, content, hierarchy, states, interaction, and how the addition joins the surrounding experience.

**Create a whole surface inside an established world.** Keep the visual system fixed. Derive three to five materially different structures from the content, task, and user behavior, and offer the strongest two or three to the user. Each option varies composition, never identity.

**Create or replace the visual world.**

1. Name the product's unique mechanism in one sentence, the audience's real scene, its cultural home, and what this first surface must prove. Name the page this category always ships and its predictable opposite: both are the rut.
2. From the audience's world, list seven concrete visual systems, artifacts, places, or rituals they know by heart. For each, note why it resonates and how it looks (ground and main colors, type voices, the one signature that makes it recognizable). Include the audience's graphic and screen traditions: notation, publications, identity programs, data graphics. On an Operate or Read surface, never take the tools the audience operates (a terminal, a scope, a control panel) as the world; they come back as costumes. When more than three candidates share one material family, keep digging until the list spans at least three.
3. Turn the strongest candidates into complete directions, each joining a reusable visual world to a concrete first-surface experience: world, first viewport, visitor path, signature interaction, honest risk.
4. Present two or three directions with the AskUserQuestion tool (skip this when the user already named a direction), the most resonant first, with each option's description carrying its world and its risk. Always include one quiet alternative: the category standard, played straight. Never recommend it; if the user picks it, ask for two or three products it should sit alongside and execute it at their craft level, without irony.

Every direction must be viable: every claim it visualizes true, a real palette and component family, workable within the available assets and performance budget. Demonstration data is design material: author it at full fidelity and label it as sample data. Commercial and factual claims (prices, customers, benchmarks, capabilities) are never invented.

## 4. Visitor modes

The mode names what the visitor's success looks like on this surface. Choose it from the requested surface, not the product: a tool's landing page is Persuade; a fashion house's documentation is Read.

- **Persuade** (landing pages, marketing, pricing): the opening makes the offer intelligible and desirable, exposes the action visitors came to take in its working form (a search, a booking slot, add to cart), and demonstrates something only this product can prove. The world may carry the page, but it never becomes a picture of the page: navigation still reads as links, copy as text, the primary action as plainly clickable.
- **Experience** (portfolios, galleries, showcases): the work itself leads from the first viewport; the interface recedes.
- **Operate** (app UI, dashboards, admin, settings): someone who uses tools like this should know where everything is before they notice the world. The world lends type, palette, density, and one signature move, never the layout, navigation model, or controls. See [operate.md](operate.md).
- **Read** (docs, articles, guides, changelogs): the reader's question leads. The world owns the frame (masthead, rail, section openers, how code and tables are set); the reading column stays calm, in a reading face at a real measure.

## 5. Commit the world

**Color strategy.** Pick a strategy before picking colors: Restrained (tinted neutrals plus one accent; common on Operate and Read surfaces), Committed (one saturated color carries 30-60% of the surface), Full palette (3-4 named roles), or Drenched (the surface is the color). Persuade and Experience surfaces have permission for the bolder strategies. Color commits at page scale: fields that own whole regions, not accents scattered over a neutral ground. Light or dark is never a default: write one sentence describing the physical scene (who uses this, where, under what light) and let it force the answer.

**Typefaces.** Choose faces like objects from the subject's world, in the mode's register. Operate and Read surfaces are well served by system stacks and workhorse UI faces. Persuade and Experience surfaces want faces with a point of view, and these training-data defaults mean you stopped looking: Fraunces, Playfair Display, Cormorant, Lora, Crimson, Newsreader, Syne, Space Grotesk, Space Mono, IBM Plex, Inter as display, DM Sans, DM Serif, Outfit, Plus Jakarta Sans, Instrument Sans. Use one only for a reason no other face could satisfy; a subject association (books want a serif, tech wants a mono) is never that reason.

**Calibration.** Generated interfaces cluster around a few looks regardless of subject (the "AI design clusters" in SKILL.md list them). Where the brief leaves the aesthetic free, landing in one means the self-check failed: if someone could guess your aesthetic from the category alone, rework it. A brief's negative constraints (no gamification, no hype) rule out those devices, not energy. A bookish, warm, or child-facing subject does not license cream paper and a serif: book cloth, thread, jackets, and endpapers span the whole saturated spectrum.

## 6. Record the direction

Before code, write the chosen direction as a short contract (about 150 words) in the design context, under a `### Direction: <surface>` heading:

- **Thesis:** the one idea this surface owns, and the category-default arrangement it refuses.
- **Own world:** the palette and component language, specific enough to recognize with all content removed.
- **Story:** what the visitor understands, believes, and does.
- **First viewport:** the exact composition, what is where and at what scale, and where the primary action sits.
- **Signature:** the one interaction or motion moment this surface is remembered for.

If a block reads like a mood, the direction is not decided yet. Never copy the contract into implementation source or anything shipped to the browser (comments, hidden DOM, `data-*` attributes, metadata).

## 7. Build with full commitment

Build the chosen direction, not a safer interpretation of it. Rebuild every atom (nav, buttons, inputs, links) in the world's vocabulary; a stock component inside a committed world is a lapse. Land the first build fully committed; later passes make it clear and effective, never diluted.

- **The first viewport is a thesis, not a header.** Demonstrate the mechanism immediately, at the scale it has in life. Memory test: if someone left after one viewport, what would they describe an hour later? If the honest answer is a mood, the concept has not committed.
- **Prove, don't claim.** Show the subject doing its job: the interface at work, specifics a competitor could not copy-paste.
- **Author the assets; never substitute chrome.** Great surfaces live on carefully made content: names, entries, copy, covers, thumbnails. Gradients, glass, generic icon tiles, and polygon `clip-path` shapes where an authored asset belongs are the gap wearing chrome. Use `generate-image` or `generate-svg` when an asset must be made.
- **Build the world's web leverage.** When the world names a technique (canvas, WebGL, view transitions, generative motion), build the technique itself, not a static imitation. See [overdrive.md](overdrive.md).
- **Pace the scroll.** Vary density, scale, image, motion, and quiet inside one grammar; a dense passage earns a quiet one, and the page ends on a real close. One spacing rhythm throughout, with more space above a heading than below it.
- **Use real, verified imagery when the brief implies it.** One decisive photo beats five mediocre ones. Verify that every image URL resolves.
- **Author motion as material.** One orchestrated moment, not scattered hover effects. Keep content visible by default. See [animate.md](animate.md).

Read [craft-floor.md](craft-floor.md) immediately before writing UI code. Preserve semantics, accessibility, performance, responsiveness, project conventions, and working behavior.

## 8. Inspect and finish

Inspect in bounded passes. Capture desktop (1440px) and mobile (390px) screenshots in one batched round, adding the user's actual viewport when you know it. Critique the render against the request and the direction contract, fix everything material in one batch, and confirm with at most one more round.

A capture is evidence only when it is valid: settle or disable entrance motion first, capture full-page shots from the document top, and open every file to confirm it shows what its name claims (no blank regions, no half-loaded state).

For substantial work, hand the final review to a fresh subagent with no access to the build conversation: pass it the original request, the direction contract, the screenshot paths, and [craft-floor.md](craft-floor.md), and ask for a ship-or-fix verdict with specific findings. Apply its fixes in one batch, recapture once to confirm, and stop; report anything left unresolved instead of starting another loop.

After a new or replacement world ships, record its visual system (color tokens, type roles, spacing scale, component language) in DESIGN.md or the design context, written from the built result rather than from the plan.
