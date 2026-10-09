---
name: systematic-debugging
description: Enforces root-cause debugging before any fix - reproduce, gather evidence at component boundaries, trace bad values to their source, test one hypothesis at a time, then fix with a failing regression test first. Use when encountering any bug, test failure, build failure, flaky test, performance regression, or unexpected behavior, before proposing a fix, and especially after a first fix attempt has failed.
license: MIT. Adapted from obra/superpowers. See NOTICE.md.
---

# Systematic Debugging

Random fixes waste time and create new bugs. Quick patches mask the underlying issue.

**Core principle:** find the root cause before attempting any fix. A symptom fix is a failure.

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If Phase 1 is not complete, do not propose a fix.

## When to Use

Any technical issue: test failures, production bugs, unexpected behavior, performance problems, build failures, integration issues, flaky tests.

Use it **especially** when:
- Time pressure makes guessing tempting
- "One quick fix" seems obvious
- A previous fix did not work
- You do not fully understand the issue

Simple bugs have root causes too, and for them the process is fast.

## The Four Phases

Complete each phase before moving to the next.

### Phase 1: Root Cause Investigation

1. **Read the error completely.** Stack traces, line numbers, error codes, warnings above the failure. They often contain the answer.
2. **Reproduce consistently.** Find the exact steps. If it is not reproducible, gather more data instead of guessing.
3. **Check recent changes.** `git log -p`, `git diff`, dependency bumps (lockfile diff), config and environment differences. `git bisect run <test>` finds the breaking commit mechanically.
4. **Gather evidence at component boundaries.** In multi-component systems (UI → API → service → database, CI → build → deploy), log what enters and exits each boundary, run once, and let the evidence show which layer breaks. Then investigate that layer.
5. **Trace data flow backward.** When a bad value surfaces deep in a call stack, ask what called this with that value, and keep going up until you find where it originated. Fix at the source. Technique: [references/root-cause-tracing.md](references/root-cause-tracing.md).

### Phase 2: Pattern Analysis

1. **Find working examples** of similar code in the same codebase.
2. **Read reference implementations completely** before applying a pattern. Skimming guarantees subtle misuse.
3. **List every difference** between working and broken, however small.
4. **Map dependencies**: settings, environment, versions, initialization order, assumptions.

When library behavior is in question, check current documentation (Context7 MCP or the official docs) instead of trusting memory.

### Phase 3: Hypothesis and Testing

1. **State one hypothesis**: "X is the root cause because Y." Write it down.
2. **Test it minimally**: the smallest change, one variable at a time.
3. **Verify**: confirmed → Phase 4. Refuted → form a new hypothesis. Never stack another fix on top.
4. **Admit unknowns**: say "I don't understand X" and investigate or ask, rather than pretending.

### Phase 4: Implementation

1. **Write a failing test that reproduces the bug** (see `test-driven-development`). Watch it fail for the right reason.
2. **Implement one fix** that addresses the root cause. No "while I'm here" changes, no bundled refactors.
3. **Verify**: the new test passes, the full suite passes, and the original symptom is gone. Run the commands and read the output before claiming success.
4. **If the fix does not work**, stop and count attempts. Fewer than three: return to Phase 1 with the new information. Three or more: go to step 5.
5. **After three failed fixes, question the architecture.** Signs: each fix reveals a new problem elsewhere, fixes need sweeping refactors, or new symptoms keep appearing. Stop and discuss with the user whether the design itself is wrong before attempting a fourth fix.

Once the root cause is found, consider adding validation at each layer the bad data passed through so the bug class becomes impossible: [references/defense-in-depth.md](references/defense-in-depth.md).

## Red Flags: Stop and Return to Phase 1

- "Quick fix for now, investigate later"
- "Just try changing X and see"
- Several changes at once, then running the tests
- "Skip the test, I'll verify manually"
- "It's probably X" without evidence
- Proposing fixes before tracing the data flow
- "One more attempt" after two have failed
- The user asks "Is that actually happening?", "Will it show us...?", "Stop guessing", or sounds stuck: you have been assuming instead of verifying.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The issue is simple" | Simple issues have root causes too; the process is fast for them. |
| "Emergency, no time" | Systematic debugging is faster than thrashing. |
| "I'll write the test after the fix works" | Untested fixes don't stick. The failing test proves the fix. |
| "Multiple fixes at once saves time" | You can't tell what worked, and you add new bugs. |
| "I see the problem" | Seeing a symptom is not understanding the cause. |

## Domain Notes

**Flaky and timing-dependent tests**: replace arbitrary sleeps with condition-based waiting ([references/condition-based-waiting.md](references/condition-based-waiting.md)). To find which test leaves files or state behind, bisect with `${CLAUDE_SKILL_DIR}/scripts/find-polluter.sh <path> '<test glob>' ['<test command>']`.

**Frontend**: reproduce in the browser (Playwright MCP or the session's browser tools), read the console and network panels, and confirm the failing request or render before touching code. Check hydration mismatches, stale closures, and effect dependencies.

**Python and ML**:
- Pin down nondeterminism first: seed Python, NumPy, and the framework; disable nondeterministic kernels while debugging.
- Check shapes, dtypes, devices, and value ranges at each pipeline boundary; assert them.
- Verify data-label alignment and preprocessing parity between training and inference.
- Overfit a single batch: if the model cannot, the bug is in the model, loss, or optimizer wiring, not the data volume.
- Watch for silent broadcasting, in-place ops on tensors that require gradients, and leakage between splits.
- For NaNs, enable anomaly detection (`torch.autograd.set_detect_anomaly(True)`) and bisect the forward pass.

## When There Is No Root Cause

If investigation shows the issue is truly environmental, timing-dependent, or external: document what you investigated, add appropriate handling (retry, timeout, clear error), and add logging for next time. Most "no root cause" conclusions are incomplete investigations, so be sure before settling here.

## Fit With This Toolkit

- A non-trivial bug fix gets an RFD (see `feature-dev`) recording the symptom, root cause, evidence, and fix.
- Remove all temporary instrumentation (logging, debug prints, scratch scripts) before handing off.
- Use `test-driven-development` for the regression test and its verification gate before claiming the bug is fixed.
