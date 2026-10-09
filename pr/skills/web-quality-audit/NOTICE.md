# Notice

This skill is adapted from [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) (commit `afa8da9`, retrieved 2026-10-09), which is distributed under the MIT License reproduced below.

## What was adapted

| File | Origin |
|------|--------|
| `SKILL.md` | Rewritten from upstream `skills/web-quality-audit/SKILL.md` around a Lighthouse and axe CLI workflow, with severity, evidence, fix, and owner-skill reporting |
| `references/core-web-vitals.md` | Condensed from upstream `skills/core-web-vitals/` (SKILL.md and the LCP, INP, and CLS references) and `skills/performance/references/MEASUREMENT.md`; Lighthouse 13 insight ids and Next.js fixes added |
| `references/accessibility.md` | Condensed from upstream `skills/accessibility/` (SKILL.md, `WCAG.md`, `A11Y-PATTERNS.md`) into a WCAG 2.2 AA checklist with a manual test protocol |
| `references/seo.md` | Condensed from upstream `skills/seo/` (SKILL.md and `STRUCTURED-DATA.md`); HTTP-level checks and the Next.js Metadata API added |
| `scripts/analyze.sh` | Copied from upstream `skills/web-quality-audit/scripts/analyze.sh`; only an attribution comment was added |
| `scripts/summarize.mjs` | Written for this plugin; not from upstream |

Upstream's `best-practices` security material and `performance` skill were not carried over.

## Upstream license

```
MIT License

Copyright (c) 2026 Addy Osmani

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
