# Critique

Run a holistic UX design review of one target: two independent assessments, one synthesized report, then a few targeted questions about what to improve next. The chat response is the deliverable; do not edit code during a critique.

## Contents

- [Workflow](#workflow): setup, the two assessments, report structure, questions, and recommended actions
- [Reference material](#reference-material): [cognitive load](#cognitive-load-assessment), [heuristics scoring](#heuristics-scoring-guide), [issue severity](#issue-severity-p0p3), and [personas](#persona-based-testing)

## Workflow

### Ground rules

- Run two assessments: **A** (design review) and **B** (mechanical and browser evidence). When the Agent tool is available, run them as two parallel subagents so neither sees the other's output; deterministic scan findings anchor judgment, and isolation keeps the design read honest. Without subagents, finish and write down A before starting B, and say so in the method line.
- Inspect viewable targets in a browser (Playwright MCP or the session's browser tools) when one is available. Stop any local server you started for the review before reporting, unless the user asks to keep it.
- Write the full report first, then ask the questions last.

### Setup

1. **Resolve the target** to a concrete file path or URL. Prefer a source path over a dev-server URL when both identify the same surface; ports drift, paths do not.
   - "the homepage" → `app/page.tsx`, `src/pages/index.astro`, or `index.html`
   - "the settings modal" → the primary component file
   - "this page" → the current URL or source file
2. **Read the design context** if the project records one (a `## Design Context` section in CLAUDE.md, or DESIGN.md). It feeds the design-intent judgment and project-specific personas.

### Assessment A: design review

Read the relevant source files and, when a browser is available, inspect the live page. Think like a design director.

Evaluate:
- **Design specificity:** is the composition, interaction, and visual language grounded in this product, or could an unrelated product use it unchanged? Judge this before seeing any scan output.
- **Holistic design:** hierarchy, information architecture, emotional fit, discoverability, composition, typography, color, accessibility, states, copy, and edge cases.
- **Cognitive load:** apply the [cognitive load checklist](#cognitive-load-assessment); report failures and decision points with more than four visible options.
- **Emotional journey:** peak-end rule, emotional valleys, reassurance at high-stakes moments.
- **Nielsen heuristics:** score all ten with the [scoring guide](#heuristics-scoring-guide), using `n/a` only where [mode applicability](#mode-applicability) allows.

Return: specificity verdict, heuristic scores, cognitive load, emotional journey, 2–3 strengths, 3–5 priority issues, persona red flags, minor observations, and provocative questions.

### Assessment B: mechanical and browser evidence

1. **Code scan.** Search the target's markup and styles (`rg` through Bash works well) for the refusals in [craft-floor.md](craft-floor.md): gradient text, colored side-stripe borders, identical icon-heading-text card grids, eyebrow labels above headings, `01 / 02 / 03` section markers, decorative glassmorphism, hard offset shadows, glyph or emoji icons, gray text on colored surfaces, and arbitrary values outside the project's spacing, type, and color scales. Record counts and file locations.
2. **Browser pass** (viewable targets, when a browser tool exists). Capture desktop (1440px) and mobile (390px) screenshots, check the console for errors, tab through the primary flow to confirm visible focus, and measure the contrast of body text, placeholders, and text on colored or image backgrounds. For multi-view targets, cover 3–5 representative pages.
3. Report false positives and any step you skipped, with the reason.

### Report

Synthesize both assessments into one report rather than concatenating them: note where they agree, what the scan caught that the review missed, and which scan hits are false positives.

1. **Method line.** First line: `Method: dual-agent` or `Method: single-context (<reason>)`.
2. **Design specificity verdict.** Does the result feel authored for this product, or category-interchangeable? Give the unanchored assessment (coherence, structural sameness, interchangeable choices, missed opportunities for product character), then summarize the code scan with counts and locations.
3. **Design health score.** Nielsen's ten heuristics as a table, one row each:

   | # | Heuristic | Score | Key issue |
   |---|-----------|-------|-----------|
   | 1 | Visibility of system status | ? | specific finding, or "—" if solid |
   | … | … | … | … |
   | **Total** | | **??/[applicable max]** | **[rating band]** |

   The applicable maximum is 4 × the number of heuristics scored: /40 when all ten apply, /32 when two are `n/a`. Be honest: a 4 means genuinely excellent, and most real interfaces score 20–32 out of 40.
4. **Overall impression.** A brief gut reaction: what works, what doesn't, and the single biggest opportunity.
5. **What's working.** 2–3 things done well, and specifically why they work.
6. **Priority issues.** The 3–5 most impactful problems, in order. For each: **[P?] what** (with a [severity](#issue-severity-p0p3)), **why it matters** to users, a concrete **fix**, and the **reference** that addresses it (adapt, animate, bolder, clarify, colorize, delight, distill, extract, harden, layout, onboard, optimize, overdrive, polish, quieter, typeset).
7. **Persona red flags.** Pick 2–3 [personas](#persona-based-testing) that fit the interface, plus 1–2 [project-specific personas](#project-specific-personas) when a design context exists. Walk the primary action as each and name the exact elements that fail them, for example: *Alex (power user): no keyboard shortcuts; the primary action takes 8 clicks; onboarding is a forced modal.*
8. **Minor observations.** Quick notes on smaller issues.
9. **Questions to consider.** Provocative questions that might unlock better solutions ("What would a confident version of this look like?").

Be direct and specific ("the submit button," not "some elements"), say why each problem matters to users, give concrete fixes instead of "consider exploring," and prioritize: if everything is important, nothing is.

### Ask the user

After the report, ask 2–3 targeted questions with the AskUserQuestion tool, each offering 2–3 concrete options tied to the findings:

1. **Priority direction:** which issue category to tackle first (offer the top 2–3 found).
2. **Design intent:** if the critique found a tonal mismatch, whether it was intentional, with 2–3 tonal directions that would fix it.
3. **Scope:** "Top 3 only", "All issues", or "Critical issues only". Ask about off-limits areas only when findings span many areas.

Skip generic questions such as "who is your audience?". When the report has fewer than three priority issues, skip the questions and say why in one line.

### Recommended actions

After the user answers, present a prioritized action list, one line per reference:

1. **`reference-name`**: what to fix, with specific context from the critique

Order by the user's stated priorities, then by impact; map each priority issue to a reference; skip references that address nothing; respect the chosen scope and off-limits areas; end with a [polish](polish.md) pass if any fixes were recommended. Offer to run them one at a time or together, and to re-run the critique afterwards to show the score change.

---

## Reference material

### Cognitive load assessment

Cognitive load is the mental effort an interface demands. There are three kinds:

- **Intrinsic** (the task itself): cannot be removed, only structured. Break complex tasks into steps, provide templates and defaults, group related decisions, disclose progressively.
- **Extraneous** (bad design): pure waste; eliminate it. Sources: navigation that requires a mental map, labels that force guessing, visual clutter, inconsistent patterns, unnecessary steps.
- **Germane** (learning): good load that builds mastery. Support it with consistent patterns, confirming feedback, and onboarding that teaches through action.

#### Checklist

- [ ] **Single focus:** the primary task can be completed without distraction from competing elements.
- [ ] **Chunking:** information comes in digestible groups (about four items per group).
- [ ] **Grouping:** related items are visually grouped (proximity, borders, shared background).
- [ ] **Visual hierarchy:** it is immediately clear what matters most.
- [ ] **One thing at a time:** the user can settle one decision before the next.
- [ ] **Minimal choices:** about four visible options at any decision point.
- [ ] **Working memory:** nothing from a previous screen must be remembered to act on this one.
- [ ] **Progressive disclosure:** complexity appears only when needed.

Count failures: 0–1 is low load, 2–3 moderate (address soon), 4+ high (critical).

#### Working memory

People hold about four chunks in working memory at once (Cowan, 2001). At each decision point, count the options, actions, or facts the user must weigh together: up to four is comfortable, 5–7 calls for grouping or disclosure, 8+ means users skip, misclick, or abandon. In practice: one primary action with 1–2 secondary and the rest in a menu; about five top-level navigation items; one reading path in long-form content, with related links gathered at the end.

#### Common violations

| Violation | Problem | Fix |
|-----------|---------|-----|
| Wall of options | 10+ choices with no hierarchy | Group, highlight a recommendation, disclose progressively |
| Memory bridge | Step 3 needs information from step 1 | Keep the context visible where it is needed |
| Hidden navigation | User must build a mental map | Show current location: breadcrumbs, active states, progress |
| Jargon barrier | Domain language forces translation | Plain language; define unavoidable terms inline |
| Visual noise floor | Everything has equal weight | One primary element, 2–3 secondary, the rest muted |
| Inconsistent pattern | Similar actions behave differently | Same kind of action, same kind of UI |
| Multi-task demand | Read, decide, and navigate at once | Sequence the steps |
| Context switch | Jumping between screens to make one decision | Co-locate the information each decision needs |

### Heuristics scoring guide

Score each of Nielsen's ten usability heuristics from 0 to 4 on this shared scale, using the per-heuristic checks below:

| Score | Meaning |
|-------|---------|
| 0 | Absent or hostile: the heuristic is violated throughout |
| 1 | Major gaps: most of the interface fails it |
| 2 | Partial: main flows handled, significant gaps remain |
| 3 | Good: minor gaps only |
| 4 | Excellent: consistently met, including edge cases |

| # | Heuristic | Check for | A 4 looks like |
|---|-----------|-----------|----------------|
| 1 | Visibility of system status | Loading indicators, confirmation of actions, progress in multi-step flows, current location, inline validation | Every action confirms; progress is always visible |
| 2 | Match between system and real world | Familiar terminology, logical order, recognizable icons and metaphors, domain-appropriate language | Speaks the user's language throughout |
| 3 | User control and freedom | Undo/redo, cancel on forms and dialogs, a way back to safety, easy clearing of filters and selections, escape from long flows | Undo, cancel, back, and escape everywhere |
| 4 | Consistency and standards | Consistent terms, same action → same result, platform conventions, visual and interaction consistency | A cohesive, predictable system |
| 5 | Error prevention | Confirmation or undo for destructive actions, input constraints, smart defaults, clear labels, autosave | Errors are hard to make |
| 6 | Recognition rather than recall | Visible options, contextual hints, recent items, autocomplete, labels on icons | Nothing needs memorizing |
| 7 | Flexibility and efficiency | Keyboard shortcuts, customization, favorites, bulk actions, expert paths that don't burden novices | Multiple paths and real power features |
| 8 | Aesthetic and minimalist design | Only necessary information per step, clear hierarchy, purposeful emphasis, no competing decoration | Every element earns its place |
| 9 | Help users recover from errors | Plain-language messages, specific problem, recovery suggestion, error near its source, input preserved | Pinpoints the issue, suggests the fix, keeps the user's work |
| 10 | Help and documentation | Findable, contextual, task-focused, concise help reachable without leaving context | The right help at the right moment |

#### Mode applicability

Heuristics 7 (flexibility) and 10 (help) may be scored `n/a` on persuasive and showcase surfaces (landing pages, campaigns, portfolios), as may any heuristic that genuinely cannot apply. Write `n/a` with a one-line reason and lower the maximum accordingly.

#### Rating bands

| Score (of 40) | Percentage | Rating | Meaning |
|---------------|------------|--------|---------|
| 36–40 | 90%+ | Excellent | Minor polish only |
| 28–35 | 70%+ | Good | Solid foundation; address weak areas |
| 20–27 | 50%+ | Acceptable | Significant improvements needed |
| 12–19 | 30%+ | Poor | Core experience needs an overhaul |
| 0–11 | below 30% | Critical | Redesign needed |

With `n/a` heuristics, read the band off the percentage: 24/32 is 75%, so Good.

### Issue severity (P0–P3)

| Priority | Name | Description | Action |
|----------|------|-------------|--------|
| **P0** | Blocking | Prevents task completion | Fix immediately |
| **P1** | Major | Significant difficulty or confusion, or a WCAG AA failure | Fix before release |
| **P2** | Minor | Annoyance with a workaround | Fix in the next pass |
| **P3** | Polish | No real user impact | Fix if time permits |

When unsure between two levels, ask whether a user would contact support about it; if yes, it is at least P1.

### Persona-based testing

Each persona exposes failure modes a single design-director view misses. Pick 2–3 that fit the interface, walk the primary action as each, and report specific red flags rather than generic concerns.

| Persona | Profile | Test questions | Red flags |
|---------|---------|----------------|-----------|
| **Alex, impatient power user** | Expert in the category; skips onboarding, hunts for shortcuts, batch-edits, leaves if patronized | Core task in under 60 seconds? Keyboard shortcuts? Skippable onboarding? Esc closes dialogs? Bulk actions? | Forced tutorials; no keyboard path; slow, unskippable animation; one-at-a-time work where batch is natural; confirmations on low-risk actions |
| **Jordan, confused first-timer** | New to the category; reads everything, hesitates, takes labels literally | First action obvious within 5 seconds? Icons labeled? Help at decision points? Undo at every step? | Icon-only navigation; unexplained jargon; no visible help; unclear next step; no confirmation of success |
| **Sam, assistive-technology user** | Screen reader (VoiceOver, NVDA), keyboard only, possibly low vision or zoom to 200–400% | Whole flow keyboard-only? Visible focus? Meaningful alt text? Contrast meets AA? State changes announced? Reflows at 320px-wide zoom? | Click-only interactions; missing focus indicators; meaning by color alone; unlabeled fields or buttons; time limits without extension; custom widgets that break screen-reader flow |
| **Riley, deliberate stress tester** | Pushes past the happy path: edge cases, odd input, back/refresh mid-flow, multiple tabs | 0, 1, and 1,000 items? Very long text, emoji, RTL, pasted spreadsheet data? Refresh mid-workflow? Errors leave the UI usable? | Silent failures; technical error details; useless empty states; data lost on refresh; similar interactions behaving differently |
| **Casey, distracted mobile user** | One-handed, interrupted, possibly on a slow connection; types as little as possible | Primary actions within thumb reach? State kept after leaving and returning? Usable on a throttled connection? Autocomplete and defaults? Targets at least 44×44px? | Key actions at the top of the screen; progress lost on interruption; typing where selection would do; heavy assets everywhere; small or crowded targets |

| Interface type | Personas |
|----------------|----------|
| Landing page / marketing | Jordan, Riley, Casey |
| Dashboard / admin | Alex, Sam |
| E-commerce / checkout | Casey, Riley, Jordan |
| Onboarding flow | Jordan, Casey |
| Data-heavy / analytics | Alex, Sam |
| Form-heavy / wizard | Jordan, Sam, Casey |

#### Project-specific personas

When the project records a design context ([init.md](init.md)), derive 1–2 extra personas from its audience: identify the primary archetype the five above do not cover, then write a short profile, 3–4 behaviors, and 3–4 red flags drawn from that audience. Do not invent audience details; without a design context, use the five predefined personas.
