# Init: capture design context

`init` captures durable product truth and records it where every later session will read it: a `## Design Context` section in the project's CLAUDE.md. It does not invent a visual world; [new-work.md](new-work.md) creates or expands one.

Run it once per project, or when the product's audience, purpose, or brand commitments change.

## Contents

- [Step 1: Load current state](#step-1-load-current-state)
- [Step 2: Explore the project](#step-2-explore-the-project)
- [Step 3: Interview for product truth](#step-3-interview-for-product-truth)
- [Step 4: Write the design context](#step-4-write-the-design-context)
- [Step 5: Wrap up or resume](#step-5-wrap-up-or-resume)

## Step 1: Load current state

- **No design context yet:** explore, interview, and write it.
- **A `## Design Context` section exists:** ask what product knowledge is stale or missing; do not reopen confirmed fields without a reason.
- **The project keeps PRODUCT.md or DESIGN.md:** treat them as existing context. Update the file the project already uses instead of creating a competing authority, and leave a DESIGN.md's visual decisions untouched.
- **Redesign or rebrand request:** preserve confirmed product truth unless the user changes it. Visual replacement happens later in new-work, not here.

Never silently overwrite existing context. If another request invoked init, finish the context and resume that request.

## Step 2: Explore the project

Before asking, scan enough to avoid making the user repeat known facts: README and product docs; package and config files; features, workflows, routes, and roles; names, logos, legal and proof assets, and brand commitments; existing design tokens and CSS variables; accessibility signals.

Treat repository evidence as a hypothesis, not user approval. Note how mature the visual system is without documenting, extending, or replacing it.

Form a platform hypothesis: `web`, `ios`, `android`, or `adaptive` (one product that genuinely adapts its design language per OS). Mobile web remains `web`; a native wrapper around a website does not make its design language native.

## Step 3: Interview for product truth

Ask the user with the AskUserQuestion tool. Ask only about material gaps the repository and the original request do not answer with strong evidence. Keep rounds to at most three focused questions, and require one real answer or approval round before writing new context. Confirm inferences instead of asserting them. If no one can answer (an unattended run), infer from the explicit brief, label every inferred fact, and say so in your first reply.

Start with the unknowns that most change future product decisions:

1. Who is the primary user, in what situation, and what job are they doing?
2. What does the product make possible, and what is its meaningfully different mechanism or position?
3. What durable constraints, assets, evidence, or product facts must future work preserve?

Confirm an ambiguous platform separately. When the project has no framework or scaffold and the request implies building, the stack is a user decision: ask once whether they want plain static HTML/CSS, a specific framework, or your recommendation, plus any deploy target that constrains the answer. Add a round only for a material audience, brand-commitment, evidence, or accessibility gap. Record undecided facts instead of inventing them.

Do not ask for an aesthetic direction, emotional feel, visual references, colors, typography, or style during init. If the user volunteers a binding visual constraint, record it without expanding it.

### What belongs here

- users, jobs, workflows, purpose, success, positioning, and operating context;
- capabilities, constraints, terminology, evidence, platform, and accessibility;
- confirmed voice, assets, and brand commitments.

### What does not belong here

- visual worlds, palettes, typography, components, or page concepts;
- invented testimonials, customers, benchmarks, pricing, licensing, or deployment claims;
- a requirement to decide every optional field.

## Step 4: Write the design context

Write only confirmed facts and explicitly marked open decisions. Omit irrelevant subsections rather than filling them with generic prose. Append the section to CLAUDE.md in the project root (create the file if needed), or update the existing section in place.

```markdown
## Design Context

### Platform
web

### Stack
[Greenfield only: the user's answer, e.g. "static HTML/CSS", "Next.js", or "delegated: <what you chose and why>". Omit when the codebase already answers it.]

### Users
[Primary users, their situation, and job. Add other audiences only when confirmed.]

### Product Purpose
[What the product does, why it exists, and what success means.]

### Positioning
[The product mechanism or claim a neighboring product could not truthfully copy.]

### Operating Context
[Workflows, environments, tools, documents, materials, and rituals that are factual parts of using or evaluating the product.]

### Capabilities and Constraints
[Confirmed functionality, technical constraints, terminology, and explicitly undecided product facts.]

### Brand Commitments
[Existing name, voice, assets, personality, identity constraints, and references the user made binding. Omit when none exist.]

### Evidence on Hand
[Real content, data, demonstrations, testimonials, case studies, press, or assets, with paths where applicable. State absences that future work must not fabricate.]

### Product Principles
[Three to five durable strategic principles derived from confirmed answers; no visual recipes.]

### Accessibility & Inclusion
[Known user needs or required standard. Omit when no product-specific requirement was established.]
```

Platform is the bare value `web`, `ios`, `android`, or `adaptive`. For a native platform, follow the platform's own guidelines (Apple Human Interface Guidelines, Material Design) in later design work.

Before resuming any build, verify the section exists and contains the confirmed record. Interview notes held only in the conversation do not count.

## Step 5: Wrap up or resume

Summarize the captured and deliberately undecided facts, then recommend the next step from the actual project state:

- **Empty or early project:** ask for the surface to build, or run [shape.md](shape.md) when the user wants a confirmed brief before implementation. [new-work.md](new-work.md) establishes a visual world only when the requested work needs one.
- **Existing coherent interface:** offer to record its visual system (tokens, type, components) in a DESIGN.md file, or as a `### Visual System` subsection of the design context, if the user wants it captured independently of a build.
- **Existing surface needing work:** name the most relevant reference, such as [critique.md](critique.md), [audit.md](audit.md), or [polish.md](polish.md).

If init was invoked by another request, resume that request now.
