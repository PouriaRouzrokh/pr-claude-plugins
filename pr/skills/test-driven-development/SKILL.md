---
name: test-driven-development
description: Red-green-refactor test-driven development plus a verification gate that forbids claiming work is done, fixed, or passing without fresh command output as evidence. Covers when full TDD applies, writing honest tests (JS/TS with Vitest or Jest, Python with pytest, ML code), and verifying before commits and handoffs. Use when implementing a feature or bug fix with real logic, writing or repairing tests, and before claiming any task is complete.
license: MIT. Adapted from obra/superpowers. See NOTICE.md.
---

# Test-Driven Development

Write the test first. Watch it fail. Write the minimal code to pass. Then prove it with fresh output before saying it works.

**Core principle:** if you did not watch the test fail, you do not know whether it tests the right thing.

## When to Apply

Match rigor to the task, as ATLAS does (see `atlas-development`).

| Work | Approach |
|------|----------|
| Business logic, data transforms, parsers, API handlers, bug fixes | **Full TDD**: no production code without a failing test first. |
| Refactoring | Characterization tests first, then refactor while staying green. |
| UI components | Test behavior (rendering states, interactions) with Testing Library; verify visuals in the browser. |
| Styling, spikes, throwaway prototypes, generated code, config | Skip TDD, but still run the verification gate. |

When you skip TDD for a spike, throw the spike away and rebuild test-first once the approach is clear.

## Red-Green-Refactor

### RED: write one failing test

One behavior, a name that describes it, real code (mocks only at true boundaries: network, clock, filesystem).

```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = async () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };
  await expect(retryOperation(operation)).resolves.toBe('success');
  expect(attempts).toBe(3);
});
```

### Verify RED: watch it fail (mandatory)

Run the single test. Confirm it **fails** (not errors), with the expected message, because the feature is missing (not because of a typo). A test that passes immediately is testing existing behavior; fix the test.

### GREEN: minimal code

Write the simplest code that passes. No extra options, no speculative abstractions, no unrelated refactors.

### Verify GREEN: watch it pass (mandatory)

Run the test, then the **whole suite** (`npm test`, `pnpm vitest run`, `pytest`, `cargo test`, whatever the repo uses). Output must be clean: no new warnings or errors. A failure anywhere goes in your report by name, even if you did not cause it.

### REFACTOR

Only when green: remove duplication, improve names, extract helpers. Re-run tests after each change. Add no behavior.

Repeat with the next failing test.

## Writing Honest Tests

Read [references/writing-good-tests.md](references/writing-good-tests.md) before writing or changing tests. The short version:

- Name the production change that would make the test fail before you write it.
- Assert on real behavior, never on mock behavior.
- Keep test-only helpers in test utilities, out of production classes.
- Understand a dependency's side effects before mocking it.
- One behavior per test; an "and" in the name means split it.

### Stack notes

- **TypeScript/React**: Vitest or Jest with Testing Library; query by role and label (`getByRole('button', { name: /save/i })`); `userEvent` over `fireEvent`; MSW for network boundaries; Playwright for end-to-end flows that are committed to the repo.
- **Python**: pytest with fixtures and `parametrize`; `tmp_path` for files; `monkeypatch` for env and time; `pytest -x -q` while iterating.
- **ML code**: test shapes, dtypes, and value ranges of each transform; golden-output tests with tolerances (`np.testing.assert_allclose`); a tiny-data overfit test for training loops; fixed seeds; keep heavy tests behind a marker (`@pytest.mark.slow`).

## Verification Gate

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Before saying anything is done, fixed, passing, or ready (and before committing, opening a PR, or moving on):

1. **Identify** the command that proves the claim.
2. **Run** it fully and freshly in this turn.
3. **Read** the output: exit code, failure counts, warnings.
4. **Report** the actual state with the evidence. If it does not confirm the claim, say what is still broken.

| Claim | Requires | Not sufficient |
|-------|----------|----------------|
| Tests pass | Test command output with 0 failures | An earlier run, "should pass" |
| Build succeeds | Build command exits 0 | Lint passing |
| Bug fixed | The original reproduction now passes | "Code changed, so it's fixed" |
| Regression test works | Red-green verified: revert the fix, see it fail, restore | One passing run |
| Subagent finished | `git diff` shows the expected changes | The agent's own report |
| Requirements met | Line-by-line check against the RFD or request | Tests passing |

Words like "should", "probably", "seems to", or an early "Done!" are signals you skipped the gate.

## Red Flags: Start Over

- Production code written before its test
- A new test that passes immediately
- "I'll add tests later" or "I already tested it manually"
- Keeping pre-written code "as reference" while writing tests after the fact
- Claiming success without having run the command in this turn

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test it | Write the API you wish existed; write the assertion first. |
| Test is too complicated | The design is too complicated; simplify the interface. |
| Must mock everything | The code is too coupled; inject dependencies. |
| Huge setup | Extract fixtures; if still huge, simplify the design. |

## Fit With This Toolkit

- `feature-dev` and `mvp-dev` call for proactive self-testing; this skill is how to do it. Tests written this way are committed, unlike the temporary scripts their cleanup steps remove.
- Bug fixes start in `systematic-debugging`; its Phase 4 hands off here for the regression test.
- Record what was tested and the final suite result in the RFD.
