# Notices

This skill combines and modifies material from four upstream projects. Each portion remains under its original license. The Apache License 2.0 text is in [LICENSE-APACHE-2.0.txt](LICENSE-APACHE-2.0.txt); the MIT notices are reproduced below.

Upstream snapshots were taken on 2026-10-09.

## Anthropic: frontend-design

- **Source:** https://github.com/anthropics/skills/tree/main/skills/frontend-design (commit `9d630808e4add0a7146de4af9384155d5dee350a`)
- **License:** Apache License 2.0
- **Used in:** `SKILL.md`, whose core design guidance (subject grounding, design principles, AI design clusters, the two-pass process, restraint and self-critique, writing in design) is Anthropic's text.
- **Changes:** reorganized into new sections; merged with impeccable's craft floor and earlier local guidance; added visitor modes, a multi-agent section, a reference index, a React/Next.js summary, and related-skill links; light copy edits.

## Paul Bakaus: impeccable

- **Source:** https://github.com/pbakaus/impeccable, `skill/` directory, tag `skill-v4.5.2` (commit `d631a8827f99414d2b6daba4ef08b7f8701751d7`)
- **License:** Apache License 2.0. Copyright 2025 Paul Bakaus.
- **Used in:** `reference/` files `adapt.md`, `animate.md`, `audit.md`, `bolder.md`, `clarify.md`, `colorize.md`, `craft-floor.md`, `critique.md`, `delight.md`, `distill.md`, `extract.md`, `harden.md`, `init.md`, `layout.md`, `onboard.md`, `operate.md`, `optimize.md`, `overdrive.md`, `polish.md`, `quieter.md`, `shape.md`, `typeset.md`, and `new-work.md`; the craft-floor ban list summarized in `SKILL.md`.
- **Changes:**
  - Removed every dependency on impeccable's tooling: the `impeccable` CLI launcher and its detector, critique storage, concept seeding, build-phase gates, live mode, hooks, `/impeccable` slash commands, PRODUCT.md/DESIGN.md generation, and `.impeccable/` config files. Those steps are rewritten as plain instructions (manual code scans against the craft floor, browser screenshots, subagent reviews, and questions through the AskUserQuestion tool).
  - Rewrote `init.md` to record design context in the project's CLAUDE.md, and `critique.md`'s workflow section; condensed upstream `new-work.md` and the `mode-*.md` files into a new plain-Markdown `new-work.md`.
  - Removed detector rule-anchor comments, template placeholders, harness-specific blocks, and live-mode parameter sections; added titles and tables of contents.
  - Appended "Technical reference" sections to `typeset.md`, `colorize.md`, `layout.md`, `animate.md`, and `clarify.md`, and an "Interaction patterns" section to `operate.md`, carrying forward concrete guidance from the earlier impeccable reference files this skill vendored in January 2026 (`typography.md`, `color-and-contrast.md`, `spatial-design.md`, `motion-design.md`, `ux-writing.md`, `interaction-design.md`), minus advice upstream has since reversed.
  - Not vendored: native platform files (`ios.md`, `android.md`, `*.native.md`, which upstream credits to ehmo's MIT-licensed platform-design-skills), and tooling-only files (`live*.md`, `generate.md`, `hooks.md`, `doctor.md`, `document.md`, `routing.md`, `region-map.md`, `visualize.md`, `component-review.md`, `craft.md`, `degraded/`).

## Vercel: react-best-practices

- **Source:** https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices (commit `063bee94c3f4df8453406c830b0a7df0f2860278`)
- **License:** MIT, as declared in the upstream skill's frontmatter (`license: MIT`). The upstream repository ships no LICENSE file, so the copyright holder below is taken from the upstream metadata (author and organization: Vercel).
- **Used in:** `reference/react-rules/` (70 rule files, `_sections.md`, `_template.md`) and `reference/react-rules/REACT-BEST-PRACTICES.md`, which is upstream's compiled `AGENTS.md` under a stable local filename.
- **Changes:** none to the rule files; `AGENTS.md` renamed to `REACT-BEST-PRACTICES.md`.

```text
MIT License

Copyright (c) 2026 Vercel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Seth Hobson: wshobson/agents, tailwind-design-system

- **Source:** https://github.com/wshobson/agents/tree/main/plugins/frontend-mobile-development/skills/tailwind-design-system (commit `46891e7e60da0e52baf1050b7b6391b64e84c6d9`)
- **License:** MIT
- **Used in:** `reference/tailwind-design-system.md` (upstream `SKILL.md`), `reference/tailwind/details.md`, and `reference/tailwind/advanced-patterns.md` (upstream `references/`).
- **Changes:** removed the frontmatter; rewrote the pointer to the detailed references and fixed relative links for the new paths; renamed one heading; added tables of contents.

```text
MIT License

Copyright (c) 2024 Seth Hobson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
