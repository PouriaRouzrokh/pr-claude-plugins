---
name: atlas-development
description: Development philosophy for building production-ready applications. ATLAS is a 5-step framework (Architect, Trace, Link, Assemble, Stress-test) that prevents common "vibe coding" failures. Reference this skill when developing features, MVPs, or full applications.
---

# ATLAS Development Framework

Build production-ready applications, not demos. ATLAS prevents the failures that plague AI-assisted development: building before designing, skipping validation, no data modeling, no testing.

## When to Use ATLAS

**Use full ATLAS for:**
- New applications or MVPs
- Features with external integrations (APIs, databases, auth)
- Features requiring new data models or schema changes
- Complex multi-component features

**Use partial ATLAS (Link + Assemble + Stress-test) for:**
- Adding features to existing codebases
- Features using existing patterns and integrations
- Moderate complexity changes

**Skip ATLAS for:**
- Bug fixes (just fix and test)
- One-line changes
- Documentation updates
- Refactoring without behavior changes
- UI tweaks with no new logic

ATLAS is a thinking philosophy, not a checklist to follow blindly. Apply the steps that add value to your specific task.

## The ATLAS Process

| Step | Phase | What You Do |
|------|-------|-------------|
| **A** | Architect | Define problem, users, success metrics |
| **T** | Trace | Data schema, integrations map, stack proposal |
| **L** | Link | Validate ALL connections before building |
| **A** | Assemble | Build with layered architecture |
| **S** | Stress-test | Test functionality, error handling |

### Skills by Phase

| ATLAS Phase | Related Skills |
|-------------|---------------|
| Architect | `create-prd` |
| Assemble | `frontend-design`, `generate-image-nb`, `generate-svg` |
| Stress-test | `writing-clearly-and-concisely` (docs quality) |

---

## A — Architect

**Purpose:** Know exactly what you're building before touching code.

### Questions to Answer

1. **What problem does this solve?**
   - One sentence. If you can't say it simply, you don't understand it.

2. **Who is this for?**
   - Be specific: "Me" / "Sales team" / "YouTube subscribers"
   - Not "everyone"

3. **What does success look like?**
   - Measurable outcome: "I can see my metrics in one dashboard"
   - Not vague: "It works"

4. **What are the constraints?**
   - Budget (API costs)
   - Time (MVP vs full build)
   - Technical (must use Supabase, must integrate with X)

### Output

```markdown
## App Brief
- **Problem:** [One sentence]
- **User:** [Who specifically]
- **Success:** [Measurable outcome]
- **Constraints:** [List]
```

---

## T — Trace

**Purpose:** Design before building. This is where most "vibe coders" fail.

### Data Schema

Define your source of truth BEFORE building:

```
Tables:
- users (id, email, name, created_at)
- saved_items (id, user_id, title, content, source, created_at)
- metrics (id, user_id, platform, value, date)

Relationships:
- users 1:N saved_items
- users 1:N metrics
```

### Integrations Map

List every external connection:

| Service | Purpose | Auth Type | Available? |
|---------|---------|-----------|------------|
| Supabase | Database | API Key | Yes |
| YouTube API | Metrics | OAuth | Via MCP |
| Notion | Save items | API Key | Yes |

### Technology Stack Proposal

Based on requirements, propose:
- Database (Supabase, Firebase, Postgres, etc.)
- Backend (Supabase Functions, n8n, custom API)
- Frontend (React, Next.js, vanilla, etc.)
- Any other services needed

User approves or overrides before proceeding.

### Edge Cases

Document what could break:

- API rate limits (YouTube: 10,000 quota/day)
- Auth token expiry
- Database connection timeout
- Invalid user input
- MCP server unavailability

### Output

- Data schema diagram or markdown table
- Technology stack (approved by user)
- Integrations checklist
- Edge cases documented

---

## L — Link

**Purpose:** Validate all connections BEFORE building. Nothing worse than building for 2 hours then discovering the API doesn't work.

### Connection Validation Checklist

```
[ ] Database connection tested
[ ] All API keys verified
[ ] MCP servers responding
[ ] OAuth flows working
[ ] Environment variables set
[ ] Rate limits understood
```

### How to Test

**Database:**
- Test via MCP or direct API call
- Should return empty array or existing data, not error

**APIs:**
- Make a simple GET request
- Verify response format matches expectations

**MCPs:**
- List available tools
- Test one simple operation

### Output

All green checkmarks. If anything fails, fix it before proceeding.

---

## A — Assemble

**Purpose:** Build the actual application with proper architecture.

### Architecture Layers

Follow separation of concerns:

1. **Frontend** (what user sees)
   - UI components
   - User interactions
   - Display logic

2. **Backend** (what makes it work)
   - API routes
   - Business logic
   - Data validation

3. **Database** (source of truth)
   - Schema implementation
   - Migrations
   - Indexes

### Build Order

1. Database schema first
2. Backend API routes second
3. Frontend UI last

This order prevents building UI for data structures that don't exist.

### Component Strategy

- Use existing component libraries (don't reinvent buttons)
- Keep components small and focused
- Document any non-obvious logic

### Output

Working application with:
- Functional database
- API endpoints responding
- UI rendering correctly

---

## S — Stress-test

**Purpose:** Test before shipping. This is the step most "vibe coding" tutorials skip entirely.

### Proactive Self-Testing

Test your own work before anyone else sees it. Run the code yourself:

- **Backend**: Call your API endpoints, invoke your functions, run database queries. Verify correct responses and data flow.
- **Frontend**: Open the UI, click through flows, take screenshots. Use Playwright if available.
- **Logic**: Write quick validation scripts to confirm business logic behaves correctly.
- **Integration**: Verify new code works with existing features — don't assume, verify.

After all tests pass, **clean up every test artifact**: remove temporary scripts, debug print statements, console.logs, hardcoded test data, temporary routes, and any code added solely for testing. The codebase must contain zero testing residue.

### Functional Testing

Does it actually work?

```
[ ] All buttons do what they should
[ ] Data saves to database
[ ] Data retrieves correctly
[ ] Navigation works
[ ] Error states handled
```

### Integration Testing

Do the connections hold?

```
[ ] API calls succeed
[ ] MCP operations work
[ ] Auth persists across sessions
[ ] Rate limits not exceeded
```

### Edge Case Testing

What breaks?

```
[ ] Invalid input handled gracefully
[ ] Empty states display correctly
[ ] Network errors show feedback
[ ] Long text doesn't break layout
```

### User Acceptance

Is this what was wanted?

```
[ ] Solves the original problem
[ ] User can accomplish their goal
[ ] No major friction points
```

### Code Professionalization

Before handoff, review every file you changed. The code must read as if written by a senior engineer:

```
[ ] No redundant or duplicated code blocks
[ ] No dead code, unused imports, or unused variables
[ ] No debug artifacts (console.log, print, TODO/FIXME/HACK)
[ ] Consistent naming following project conventions
[ ] Comments present where logic is non-obvious, absent where obvious
[ ] No overly complex logic that could be simplified
[ ] Consistent formatting and style throughout
[ ] No hardcoded values that should be constants or configuration
[ ] Error messages are clear and helpful
```

This is not optional. Messy, careless code erodes trust. Every file should be clean, well-organized, and easy to follow.

### Output

Test report with:
- What passed
- What failed
- What needs fixing
- What was cleaned up during professionalization

---

## Multi-Agent Approaches in ATLAS

Complex ATLAS workflows benefit from running multiple agents. Choose the right strategy based on task needs.

### Subagents (Default)

Subagents are lightweight workers that report results back. Use them for:
- **Trace**: Multiple code-explorer agents analyzing different parts of the codebase in parallel
- **Assemble**: Code-architect agents proposing different implementation approaches
- **Stress-test**: Code-reviewer agents checking different quality dimensions (bugs, security, performance)

Subagents are cheaper, faster, and sufficient when each agent works independently and you synthesize their outputs.

### Agent Teams

Agent teams are independent sessions with inter-agent messaging. Consider them for:
- **Trace + Link**: When architects need to debate schema decisions, negotiate shared components, and validate that integration plans are consistent across layers
- **Assemble**: Full-stack features where frontend, backend, and data agents need to coordinate file ownership and share interface contracts
- **Stress-test**: When reviewers should challenge each other's findings — e.g., security reviewer flagging that a performance optimization bypasses validation

Agent teams are experimental, more expensive, and add coordination overhead. Use them only when inter-agent communication provides a clear advantage over consolidating subagent outputs yourself.

### Decision Guide

| ATLAS Phase | Subagents | Agent Teams |
|-------------|-----------|-------------|
| Architect | N/A (interactive with user) | N/A |
| Trace | Parallel exploration of codebase | Architects debating schema/integration choices |
| Link | Independent validation checks | Cross-layer validation coordination |
| Assemble | Independent implementation tasks | Multi-layer features needing coordination |
| Stress-test | Independent review dimensions | Adversarial review with cross-referencing |

---

## Anti-Patterns (What NOT to Do)

These are the mistakes that cause projects to fail:

1. **Building before designing** — You end up rewriting everything
2. **Skipping connection validation** — Hours wasted on broken integrations
3. **No data modeling** — Schema changes cascade into UI rewrites
4. **No testing** — Ship broken code, lose trust
5. **Hardcoding everything** — No flexibility for changes
6. **Shipping messy code** — Redundancies, debug leftovers, inconsistent naming, missing or excessive comments. Unprofessional code erodes trust even when it works

---

## Quick Reference: When to Apply Each Step

| Context | Apply |
|---------|-------|
| PRD creation | A (Architect) — define problem, users, success |
| MVP planning | A + T — architecture + data schema + integrations |
| Feature development | T + L + A — trace dependencies, link/validate, assemble |
| Bug fixes | L + A + S — validate context, fix, test |

---

## Extended Framework (Production Builds)

For production builds, add:

+ **V — Validate**: Security/input sanitization, edge cases, unit tests
+ **M — Monitor**: Logging, observability, alerts

These steps are optional for MVPs but required for production deployments.
