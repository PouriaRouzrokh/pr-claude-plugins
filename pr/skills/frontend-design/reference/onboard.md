# Onboard

Get people to first value as fast as possible. Onboarding's job is not to teach the whole product; it is to reach the moment that proves the product is worth their time. Before designing, know that moment (the first project created, the first report run) and the users' experience level; infer them from the design context and product, and ask only if they remain unclear.

## Contents

- [Assess](#assess)
- [Principles](#principles)
- [Patterns](#patterns)
- [Empty states](#empty-states)
- [Implementation](#implementation)
- [Verify](#verify)

## Assess

1. **The job:** what users are trying to accomplish, where they get stuck or drop off, and what the first-value moment is.
2. **The users:** experience level (new to the category, switching from a competitor, expert), motivation (exploring vs. required by work), and the time they will give it.
3. **Success:** the minimum they must learn, the one key action, and how you would know it worked (completion rate, time to first value).

## Principles

- **Show, don't tell.** Use real functionality with working examples rather than a separate tutorial mode.
- **Make it skippable.** Experienced users can skip or dismiss everything, and nothing blocks access to the product.
- **Time to value.** Front-load the few concepts that deliver most of the value; save advanced features for discovery in context.
- **Context over ceremony.** Teach a feature when the user reaches it; empty states and point-of-use hints beat upfront tours.
- **Respect intelligence.** Don't explain standard patterns; be brief.

## Patterns

**First run**
- **Welcome:** what the product does for this user and, if there is a setup flow, how long it takes, with a visible way to skip.
- **Account setup:** ask for the minimum now and the rest later; explain non-obvious requests; prefill sensible defaults.
- **Core concepts:** introduce one to three, interactively where possible, with progress shown ("Step 1 of 3").
- **First success:** guide the user to something real, offer templates or sample data so actions work immediately, acknowledge completion in proportion to the effort ([delight.md](delight.md)), and point to the next step.

**Ongoing discovery**
- **Contextual hints:** appear the first time a user reaches a feature, point at the relevant control, explain the benefit in a line, and dismiss permanently.
- **Feature announcements:** say what changed and why it matters, let users try it immediately, and stay dismissible.
- **Progressive unlocking:** reveal advanced options as users show they need them.

**Guided tours** suit complex tools, major redesigns, and domain-heavy products. Keep them to 3–7 steps, focused on a workflow ("Create a project") rather than a feature inventory ("This is the project button"); let users click the real interface during the tour; offer "Skip tour"; and make the tour replayable from help.

**Interactive tutorials** suit high-stakes or unfamiliar work: a sandbox with sample data, a clear objective ("Create a chart of sales by region"), validation that the user did it, and a clear finish.

**In-product help:** contextual help links, a searchable help center, and visible keyboard shortcut hints (for example, `⌘K` shown in the search field).

## Empty states

Every empty state answers three questions and offers an action:

- **What will be here:** "Your projects will appear here."
- **Why it matters:** "Projects keep your files and your team's work in one place."
- **How to start:** [Create project] or [Start from a template]

Add an image only if it comes from the product's own visual world ([craft-floor.md](craft-floor.md) refuses generic illustration). Distinguish the kinds of emptiness, because each needs a different response:

| Type | Response |
|------|----------|
| First use | Emphasize value; offer a template or sample data |
| User cleared everything | Light touch; easy to start again |
| No results | Suggest a different query; offer to clear filters |
| No permission | Explain why and how to get access |
| Failed to load | Say what happened; offer a retry |

Copy patterns for these states are in [clarify.md](clarify.md#loading-empty-and-success-states).

## Implementation

- **Hints and popovers:** the Popover API with CSS anchor positioning covers most tooltip and coach-mark needs natively ([operate.md](operate.md#overlays)); Floating UI is the library fallback.
- **Tours:** use the project's existing tour library if it has one (for example Shepherd.js or React Joyride); otherwise popovers plus a small state machine are often enough.
- **Dialogs:** native `<dialog>` with `showModal()` for anything modal.
- **Remembering progress:** store completed steps and dismissed hints server-side for signed-in users, so they follow the user across devices; `localStorage` is fine for anonymous visitors. Never show the same onboarding twice.
- **Measurement:** instrument completion, skip, and drop-off per step so the flow can be tuned.

Avoid: long mandatory onboarding before first use; tours that block the whole UI; tutorial modes disconnected from the real product; hidden or hard-to-find "Skip"; information dumps up front; re-running first-run onboarding for returning users.

## Verify

- Walk the flow as a new user in a fresh profile (cleared storage), then as a returning user: first value should arrive in minutes, and nothing should repeat.
- Every step can be skipped or dismissed, works by keyboard, and announces itself to screen readers.
- Each empty-state type above renders with its own message and action.
- Note which success metrics are instrumented; real-user completion and time-to-value numbers come later, so say what to watch.

When users reach first value quickly, finish with a polish pass ([polish.md](polish.md)).
