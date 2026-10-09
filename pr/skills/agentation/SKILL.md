---
name: agentation
description: Adds the Agentation visual feedback toolbar to a React 18+ app (Next.js App or Pages Router, Vite, React Router, Remix) so the user can click elements in the browser and send precise, selector-level annotations to the agent, optionally synced live through the agentation-mcp server. Use when the user wants to annotate the UI, give visual design feedback to Claude, or set up Agentation.
argument-hint: "[optional: mcp | manual]"
license: PolyForm Shield 1.0.0. Adapted from benjitaylor/agentation, © 2026 Benji Taylor. See NOTICE.md.
---

# Agentation Setup

Set up the toolbar and, when requested, connect it to Claude Code. A visible toolbar and a healthy MCP server do not prove that browser feedback reaches the agent: verify that final step before calling setup complete.

## Steps

1. **Inspect the project**
   - Read the project's instructions and detect the package manager from the lockfile.
   - Look for `agentation` in `package.json` and an existing `<Agentation` mount before installing.
   - If already mounted, inspect its `endpoint` and the current MCP setup. Do not exit just because the component exists, and never add a duplicate mount.
   - Install it as a dev dependency if missing: `npm install -D agentation` (or the pnpm/yarn/bun equivalent).

2. **Choose the connection mode**
   - **MCP (live sync)**: annotations go straight to Claude Code through a local HTTP server, default `http://localhost:4747`. Preserve any existing custom port or proxy URL. If the browser and the agent run on different machines, ask for the reachable URL.
   - **Manual**: omit `endpoint`; the user copies annotations from the toolbar and pastes them into the chat. Never enable a server connection silently.
   - If `$ARGUMENTS` or the request does not make the mode clear, ask one brief question and keep inspecting meanwhile.

3. **Mount the component (development only)**

   | Framework | Where |
   |-----------|-------|
   | Next.js App Router | Root `app/layout.tsx`, inside `<body>` after `{children}` |
   | Next.js Pages Router | `pages/_app.tsx`, after `<Component {...pageProps} />` |
   | Vite / CRA | The root component (`src/App.tsx`) or next to `<App />` in `src/main.tsx` |
   | React Router / Remix | The root route component (`app/root.tsx`), inside `<body>` |

   ```tsx
   import { Agentation } from "agentation";

   // MCP mode: pass the server URL chosen in step 2. Manual mode: omit endpoint.
   {process.env.NODE_ENV === "development" && (
     <Agentation endpoint="http://localhost:4747" />
   )}
   ```

   - In Vite projects use `import.meta.env.DEV` instead of `process.env.NODE_ENV === "development"`.
   - The package ships its own client boundary, so keep Next.js root layouts as Server Components.
   - Preserve existing props and callbacks (`onAnnotationAdd`, `webhookUrl`, `copyFormat`, ...).

4. **Configure Claude Code (MCP mode only)**
   - Register the server; the launch command must include the `server` subcommand:
     `claude mcp add agentation -- npx -y agentation-mcp server`
     (or run `npx agentation-mcp init` for the guided setup). Node 20+ is required.
   - Use the same custom port in the server command and the component's `endpoint`.
   - Tell the user to restart Claude Code (or run `/mcp` to reconnect) so the `agentation_*` tools load. Do not start a second server on a port the working server already owns.

5. **Verify the round trip**
   - Run `npx agentation-mcp doctor` (add `--http-url <url>` for a custom URL).
   - Start the dev server (see `run-local`), open the app, and create one clearly labeled test annotation through the toolbar, or ask the user to.
   - Read it back with `agentation_get_all_pending` (or the session-scoped tools) and check the exact comment text and page URL, not just a non-zero count.
   - If nothing arrives, check the component `endpoint`, browser network errors or CORS, and whether the browser and agent point to the same server.
   - If browser or MCP tools are unavailable in this session, state exactly which part is unverified and give the user that final check. Do not claim live sync works.

## Working With Annotations

Once connected, the MCP tools drive the feedback loop:

| Tool | Use |
|------|-----|
| `agentation_get_all_pending` / `agentation_get_pending` | Fetch unresolved annotations (all sessions / one session) |
| `agentation_acknowledge` | Mark an annotation as seen before working on it |
| `agentation_resolve` / `agentation_dismiss` | Close it after fixing, or decline with a reason |
| `agentation_reply` | Ask a clarifying question in the annotation thread |
| `agentation_watch_annotations` | Hands-free mode: wait for new annotations and handle them as they arrive |

Each annotation includes the element's selector, text, position, and often the React component, so locate the source directly instead of guessing. Fix, verify in the browser, then resolve.

## Notes

- The development guard keeps the toolbar out of production builds.
- Requires React 18 or newer; desktop browsers only. Vue and Svelte are not supported.
- Installing the toolbar does not install, configure, or connect the MCP server.
- Manual copy mode needs no server.
