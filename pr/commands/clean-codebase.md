---
description: Clean and professionalize code using automated review to identify issues before cleanup
argument-hint: "[optional: path/to/scope]"
---

# Clean Codebase

Clean and professionalize the codebase to make it production-ready, using code-reviewer agents to systematically identify issues.

## Core Principles

- **Review before removing**: Use code-reviewer agents to identify issues with high confidence
- **Verify usage**: Always search for references before removing any code
- **Preserve functionality**: Never change behavior, only clean up code
- **Ask when uncertain**: If there's doubt about usage, ask the user

---

## Phase 0: Scope Identification

**Goal**: Determine what to clean

**Target scope**: $ARGUMENTS

**Actions**:

1. If `$ARGUMENTS` is empty or blank → scan and clean the entire codebase
2. If `$ARGUMENTS` contains a file path → clean only that specific file
3. If `$ARGUMENTS` contains a folder path → clean all code files within that folder recursively

---

## Phase 1: Automated Review

**Goal**: Use code-reviewer agents to systematically identify cleanup opportunities

**Actions**:

1. Launch 2 code-reviewer agents in parallel with different focuses:

   **Agent 1 - Dead Code Detection**:
   ```
   Review the codebase at [scope] for dead code and unused elements. Focus on:
   - Unused imports
   - Unused variables and functions
   - Commented-out code blocks
   - Dead code paths
   - Redundant code

   For each issue, verify it's truly unused by searching for references.
   Only report issues with confidence >= 80.
   ```

   **Agent 2 - Comment and Documentation Quality**:
   ```
   Review the codebase at [scope] for comment and documentation quality. Focus on:
   - Unprofessional or outdated comments
   - Redundant comments that just restate code
   - Missing documentation for complex logic
   - TODO comments that appear completed
   - Boilerplate comments with no value

   Only report issues with confidence >= 80.
   ```

2. Wait for both agents to complete

3. Consolidate findings into a prioritized list

---

## Phase 2: Review Findings

**Goal**: Present issues to user and confirm cleanup plan

**Actions**:

1. Present consolidated findings grouped by type:
   - **Dead Code**: Unused imports, variables, functions
   - **Comment Cleanup**: Unprofessional/outdated/redundant comments
   - **Other Issues**: Any other quality issues identified

2. For any items where removal is uncertain, ask the user

3. Get user approval before proceeding with cleanup

---

## Phase 3: Dead Code Removal

**Goal**: Remove verified unused code

**Actions**:

For each confirmed dead code item:

1. **Unused imports**: Remove import statements not used in the file
2. **Unused variables**: Remove variables declared but never used
3. **Unused functions**: Remove functions/methods never called (only if verified unused across entire codebase)
4. **Dead code**: Remove commented-out code blocks serving no purpose
5. **Redundant code**: Remove duplicate logic or unnecessary abstractions

**CRITICAL**: Before removing any function, class, or significant code block:
- Search the entire codebase for references
- Check for dynamic usage (reflection, dynamic imports)
- Check configuration files for references
- If ANY doubt exists, ask the user

---

## Phase 4: Comment Professionalization

**Goal**: Clean up comments to professional standards

**Actions**:

**Remove these types of comments**:
- References to past versions ("this replaces the old implementation")
- Boilerplate comments that add no value
- TODO comments that are already done
- Commented-out code with notes like "keeping for reference"
- Obvious comments that restate what code does (`i++ // increment i`)
- Personal notes or temporary markers

**Keep and maintain these**:
- Documentation comments for public APIs, functions, and classes
- Complex logic explanations where the "why" isn't obvious
- Important warnings or caveats
- License headers (do not modify)
- JSDoc/TSDoc/docstrings that provide genuine value

**Ensure balance**:
- Not excessive (every line doesn't need a comment)
- Not too sparse (complex logic should be explained)
- Professional tone throughout

---

## Phase 5: Documentation Update

**Goal**: Update inline documentation to match current code

**Actions**:

1. **Update outdated docstrings**: Ensure function/method documentation matches actual behavior
2. **Fix parameter documentation**: Parameter names, types, and descriptions should match actual signature
3. **Update return value docs**: Ensure return types and descriptions are accurate
4. **Add missing documentation**: For public APIs, classes, and complex functions that lack documentation
5. **Remove stale documentation**: Remove docs for parameters that no longer exist
6. **Ensure type accuracy**: Type annotations in comments should match actual types

---

## Phase 6: Code Formatting

**Goal**: Apply consistent formatting

**Actions**:

1. Identify project's linter/formatter:
   - ESLint, Prettier (JavaScript/TypeScript)
   - Black, Ruff (Python)
   - rustfmt (Rust)
   - gofmt (Go)

2. Run the project's linter/formatter if available

3. Fix any linting errors or warnings

4. Address IDE/language server diagnostics and errors

5. Ensure consistent code style throughout the target scope

---

## Phase 7: Verification

**Goal**: Ensure nothing is broken

**Actions**:

1. If a test suite exists, run tests to verify nothing broke
2. Check for any new linting errors
3. Verify the application still builds/compiles

---

## Phase 8: Summary

**Goal**: Report what was cleaned

**Actions**:

Summarize to user:
- Number of unused imports removed
- Number of unused variables/functions removed
- Number of comments cleaned up
- Documentation updates made
- Formatting changes applied
- Any items skipped and why

---

## Safety Guidelines

**DO NOT:**
- Remove code that might be used dynamically (reflection, dynamic imports)
- Remove code referenced in configuration files
- Remove exported/public API without explicit confirmation
- Change any actual functionality or behavior
- Modify test files in ways that would break tests
- Remove environment-specific code without understanding context
- Make any git commits or push changes
- Update standalone documentation files (README, docs/)
- Add new features or refactor architecture
- Change configuration files unless fixing clear errors

**ALWAYS:**
- Search for usages across the entire codebase before removing anything
- Ask the user if uncertain whether something is used
- Preserve all existing functionality
- Run tests after making changes if a test suite exists
- Make changes incrementally and verify nothing breaks
