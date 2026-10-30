# Audit

Run systematic technical quality checks and write a report. Do not fix issues during the audit; document them so the other references can address them.

This is a code-level audit, not a design critique. Check what's measurable and verifiable in the implementation.

**Web only** (mobile web included). For native apps, audit against the platform's own guidelines instead.

## Contents

- [Diagnostic Scan](#diagnostic-scan)
- [Generate Report](#generate-report)
- [Recommended Actions](#recommended-actions)

## Diagnostic Scan

Run comprehensive checks across 5 dimensions. Score each dimension 0-4 using the criteria below.

### 1. Accessibility (A11y)

**Check for**:
- **Contrast issues**: Text below 4.5:1, large text (24px, or 18.66px bold) below 3:1, and controls, icons, and focus indicators below 3:1 against adjacent colors (WCAG 2.2 AA)
- **Motion sensitivity**: `prefers-reduced-motion` needs an intentional alternative that preserves state change and hierarchy; flag a global `0.01ms` kill that destroys useful feedback, flashing above threshold, and motion that blocks focus, reading, or task completion
- **Missing ARIA**: Interactive elements without proper roles, labels, or states
- **Keyboard navigation**: Missing focus indicators, illogical tab order, keyboard traps
- **Semantic HTML**: Improper heading hierarchy, missing landmarks, divs instead of buttons
- **Alt text**: Missing or poor image descriptions
- **Form issues**: Inputs without labels, poor error messaging, missing required indicators, missing `autocomplete` tokens
- **WCAG 2.2 additions**: Focus hidden behind sticky headers (2.4.11), targets smaller than 24×24 CSS px without spacing (2.5.8), drag-only interactions without a pointer alternative (2.5.7), and re-asking for information already entered (3.3.7)

**Score 0-4**: 0=Inaccessible (fails WCAG A), 1=Major gaps (few ARIA labels, no keyboard nav), 2=Partial (some a11y effort, significant gaps), 3=Good (WCAG AA mostly met, minor gaps), 4=Excellent (WCAG AA fully met, approaches AAA)

### 2. Performance

**Check for**:
- **Layout thrashing**: Reading/writing layout properties in loops
- **Expensive animations**: Casual layout-property animation, unbounded blur/filter/shadow effects, or effects that visibly drop frames
- **Missing optimization**: Below-the-fold images without lazy loading, a lazy-loaded or low-priority LCP image, media without dimensions (layout shift), unoptimized assets
- **will-change overuse**: `will-change` applied broadly or left on at rest (it is a targeted hint for known expensive animations, not a baseline requirement)
- **Bundle size**: Unnecessary imports, unused dependencies
- **Render performance**: Unnecessary re-renders, long tasks during interaction (INP above 200ms); for React, check against [react-rules](react-rules/REACT-BEST-PRACTICES.md)

**Score 0-4**: 0=Severe issues (layout thrash, unoptimized everything), 1=Major problems (no lazy loading, expensive animations), 2=Partial (some optimization, gaps remain), 3=Good (mostly optimized, minor improvements possible), 4=Excellent (fast, lean, well-optimized)

### 3. Theming

**Check for**:
- **Hard-coded colors**: Colors not using design tokens
- **Broken dark mode**: Missing dark mode variants, poor contrast in dark theme
- **Inconsistent tokens**: Using wrong tokens, mixing token types
- **Theme switching issues**: Values that don't update on theme change

**Score 0-4**: 0=No theming (hard-coded everything), 1=Minimal tokens (mostly hard-coded), 2=Partial (tokens exist but inconsistently used), 3=Good (tokens used, minor hard-coded values), 4=Excellent (full token system, dark mode works perfectly)

### 4. Responsive Design

**Check for**:
- **Fixed widths**: Hard-coded widths that break on mobile
- **Touch targets**: Interactive elements below 24×24 CSS px (the WCAG 2.2 AA floor), and primary touch controls below the recommended 44×44px. SC 2.5.8 has exceptions: spacing (a 24 CSS px circle centered on the target's bounding box overlaps no other target or undersized target's circle), an equivalent control elsewhere, inline text links, user-agent-styled controls, and an essential size
- **Broken touch interaction**: Custom sliders, drag surfaces, and scrollable control strips whose primary gesture fails under touch, that swallow page scroll or lose the drag to it, or that stay stuck after an interrupted gesture. Code tells: mouse-only handlers, no `touch-action` on a pointer-event drag surface, drag state that nothing clears on cancel, lost capture, or blur. Exercise the gesture when a browser tool can synthesize touch (a rendered viewport proves layout, not the gesture), then say what produced the evidence (emulated viewport, synthesized touch, which engine, physical device) and what stayed untested
- **Horizontal scroll**: Content overflow on narrow viewports
- **Text scaling**: Layouts that break when text size increases
- **Missing breakpoints**: No mobile/tablet variants

**Score 0-4**: 0=Desktop-only (breaks on mobile), 1=Major issues (some breakpoints, many failures), 2=Partial (works on mobile, rough edges), 3=Good (responsive, minor touch target or overflow issues), 4=Excellent (fluid, all viewports, proper touch targets, gestures work under touch)

### 5. Implementation Integrity

This dimension decides whether the build expresses a real design system or a pile of defaults, so weigh it heavily. Search the target's markup and styles for the bans in [craft-floor.md](craft-floor.md) (gradient text, side-stripe borders, identical card grids, eyebrow labels, decorative glass, hard offset shadows, glyph icons) and for arbitrary values outside the project's scale. Verify each finding in context. Look for repeated implementation shortcuts, design-system drift, misleading or decorative content, and structure that is interchangeable with an unrelated product. Keep deterministic findings separate from visual judgment and call out false positives.

**Score 0-4**: 0=systemic drift, 1=major repeated failures, 2=several verified issues, 3=minor isolated issues, 4=coherent and intentional

## Generate Report

### Audit Health Score

| # | Dimension | Score | Key Finding |
|---|-----------|-------|-------------|
| 1 | Accessibility | ? | [most critical a11y issue or "--"] |
| 2 | Performance | ? | |
| 3 | Theming | ? | |
| 4 | Responsive Design | ? | |
| 5 | Implementation Integrity | ? | |
| **Total** | | **??/20** | **[Rating band]** |

**Rating bands**: 18-20 Excellent (minor polish), 14-17 Good (address weak dimensions), 10-13 Acceptable (significant work needed), 6-9 Poor (major overhaul), 0-5 Critical (fundamental issues)

### Implementation Integrity Verdict
**Start here.** Pass/fail: does the implementation express a coherent product-specific system? Cite verified evidence and scan findings.

### Executive Summary
- Audit Health Score: **??/20** ([rating band])
- Total issues found (count by severity: P0/P1/P2/P3)
- Top 3-5 critical issues
- Recommended next steps

### Detailed Findings by Severity

Tag every issue with **P0-P3 severity**:
- **P0 Blocking**: Prevents task completion. Fix immediately
- **P1 Major**: Significant difficulty or WCAG AA violation. Fix before release
- **P2 Minor**: Annoyance, workaround exists. Fix in next pass
- **P3 Polish**: Nice-to-fix, no real user impact. Fix if time permits

For each issue, document:
- **[P?] Issue name**
- **Location**: Component, file, line
- **Category**: Accessibility / Performance / Theming / Responsive / Implementation Integrity
- **Impact**: How it affects users
- **WCAG/Standard**: Which standard it violates (if applicable)
- **Recommendation**: How to fix it
- **Suggested reference**: Which reference to apply next (see the list under [Recommended Actions](#recommended-actions))

### Patterns & Systemic Issues

Identify recurring problems that indicate systemic gaps rather than one-off mistakes:
- "Hard-coded colors appear in 15+ components, should use design tokens"
- "Touch targets consistently under 24px throughout the mobile experience"

### Positive Findings

Note what's working well: good practices to maintain and replicate.

## Recommended Actions

List recommended passes in priority order (P0 first, then P1, then P2):

1. **[P?] `reference-name`**: Brief description (specific context from audit findings)
2. **[P?] `reference-name`**: Brief description (specific context)

**Rules**: Only recommend references from: adapt, animate, bolder, clarify, colorize, delight, distill, extract, harden, layout, onboard, optimize, overdrive, polish, quieter, typeset. Map findings to the most appropriate reference. End with a polish pass ([polish.md](polish.md)) if any fixes were recommended.

After the summary, offer to run these one at a time or together, and to re-run the audit afterwards to show the score change. For measured Lighthouse and axe results (Core Web Vitals, WCAG 2.2 AA), follow up with the `web-quality-audit` skill.

Keep the report actionable: explain each issue's impact, make recommendations specific, include what works, prioritize honestly (not everything is P0), verify findings before reporting them, and keep P3 noise to a minimum.
