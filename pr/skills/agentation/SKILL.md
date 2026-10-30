---
name: agentation
description: Adds the Agentation visual feedback toolbar to a React 18+ app (Next.js App or Pages Router, Vite, React Router, Remix) so the user can click elements in the browser and send precise, selector-level annotations to the agent, optionally synced live through the agentation-mcp server. Use when the user wants to annotate the UI, give visual design feedback to Claude, or set up Agentation.
argument-hint: "[optional: mcp | manual]"
license: PolyForm Shield 1.0.0. Adapted from benjitaylor/agentation, © 2026 Benji Taylor. See NOTICE.md.
---

# Agentation Setup

Set up the toolbar and, when requested, connect it to Claude Code. A visible toolbar and a healthy MCP server do not prove that browser feedback reaches the agent, so verify that final step before calling setup complete.

## Steps

1. **Inspect the project**
   - Read the project's instructions and detect the package manager from the lockfile.
   - Look for `agentation` in `package.json` and an existing `<Agentation` mount before installing.
   - If it is already mounted, inspect its `endpoint` and the current MCP setup (`claude mcp get agentation`). An existing mount may still lack a working connection, so keep going, and never add a second mount.
   - Install it as a dev dependency if missing: `npm install -D agentation` (or the pnpm, yarn, or bun equivalent).

2. **Choose the connection mode**
   - **MCP (live sync)**: the toolbar posts annotations to a local HTTP server, default `http://localhost:4747`, and Claude Code reads them through MCP tools. Preserve any existing custom port or proxy URL. If the browser and Claude Code run on different machines or in a container, ask for the reachable URL; the server binds loopback only by default, so add `--host <address>` (or set `AGENTATION_HOST`) to the server command in step 4 to expose another interface, and only on a network you trust.
   - **Manual**: omit `endpoint`. Annotations stay in the browser; the user copies them from the toolbar and pastes them into the chat.
   - If `$ARGUMENTS` or the request does not make the mode clear, ask one brief question and keep inspecting meanwhile. Do not enable a server connection the user did not ask for.

3. **Mount the component (development only)**

   | Framework | Where | Development guard |
   |-----------|-------|-------------------|
   | Next.js App Router | Root `app/layout.tsx`, inside `<body>` after `{children}` | `process.env.NODE_ENV === "development"` |
   | Next.js Pages Router | `pages/_app.tsx`, after `<Component {...pageProps} />` | `process.env.NODE_ENV === "development"` |
   | Vite | The root component (`src/App.tsx`) or next to `<App />` in `src/main.tsx` | `import.meta.env.DEV` |
   | React Router 7 / Remix (Vite) | The root route `app/root.tsx`, inside `<body>` of the `Layout` export | `import.meta.env.DEV` |

   ```tsx
   import { Agentation } from "agentation";

   // MCP mode: pass the server URL chosen in step 2. Manual mode: omit endpoint.
   {process.env.NODE_ENV === "development" && (
     <Agentation endpoint="http://localhost:4747" />
   )}
   ```

   - In Vite-based projects, use `import.meta.env.DEV`, Vite's documented development flag, which is statically replaced and tree-shaken from production builds.
   - The package ships its own `"use client"` boundary, so keep Next.js root layouts as Server Components.
   - Preserve existing props and callbacks (`onAnnotationAdd`, `onSubmit`, `webhookUrl`, `copyFormat`, ...). For hash-based routers, add `useHashLocation`.

4. **Register the MCP server with Claude Code (MCP mode only)**
   - Run this yourself; it is non-interactive. The launch command needs the `server` subcommand:

     ```bash
     claude mcp add agentation -- npx -y agentation-mcp server
     ```

     It writes to local scope (this project, this user). Add `--scope user` (before `agentation`) to use it in every project, or `--scope project` to share it through `.mcp.json`, which asks each teammate to approve it.
   - For a custom port, append `--port <port>` after `server` and use the same port in `endpoint`.
   - Do not run `npx agentation-mcp init` through the Bash tool: it is an interactive wizard that waits for keyboard input. The user can run it in their own terminal instead.
   - The agentation-mcp server requires Node.js 20 or newer (22 or 24 LTS recommended). The toolbar itself has no Node requirement.
   - Claude Code starts the server as a stdio process, and that process also opens the HTTP port. The port is only served while a Claude Code session with the server connected is running, so do not start a second `agentation-mcp server` by hand on the same port.
   - A server added mid-session may not connect until Claude Code restarts. Ask the user to run `/mcp` and confirm `agentation` is connected; if it is missing, they should exit and resume with `claude --continue`. The tools then appear as `mcp__agentation__agentation_*`; when tool search is on, search for "agentation" to load them.

5. **Verify the round trip**
   - Run `npx agentation-mcp doctor` (add `--http-url <url>` for a custom URL). Doctor checks Node, the Claude Code config, and server reachability, not browser delivery.
   - Start the dev server (see the `run-local` skill), open the app, and create one clearly labeled test annotation through the toolbar, or ask the user to.
   - Read it back with `agentation_get_all_pending` and check the exact comment text and page URL, not just a non-zero count. Leave unrelated annotations alone.
   - If nothing arrives, check the component `endpoint`, browser network errors or CORS (a forwarded or non-local origin needs `AGENTATION_CORS_ORIGINS`), and whether the browser and Claude Code point to the same server.
   - If browser or MCP tools are unavailable in this session, state exactly which part is unverified and give the user that final check. Do not claim live sync works until the test annotation has been read back.

## Working With Annotations

Once connected, these MCP tools drive the feedback loop:

| Tool | Use |
|------|-----|
| `agentation_get_all_pending` / `agentation_get_pending` | Fetch unresolved annotations (all sessions / one session) |
| `agentation_list_sessions` / `agentation_get_session` | List sessions, or read one session with all its annotations |
| `agentation_acknowledge` | Mark an annotation as seen before working on it |
| `agentation_resolve` / `agentation_dismiss` | Close it with a summary after fixing, or decline with a reason |
| `agentation_reply` | Ask a clarifying question in the annotation thread |
| `agentation_watch_annotations` | Hands-free mode: blocks until new annotations arrive; call it again after handling each batch |

Each annotation includes the element's selector, text, position, and often the React component and source location, so locate the source directly instead of guessing. Fix, verify in the browser, then resolve.

## Notes

- The development guard keeps the toolbar out of production builds.
- Requires React 18 or newer and a desktop browser; the toolbar is a React component, so other frameworks are not supported.
- Installing the toolbar does not install, configure, or connect the MCP server, and manual copy mode needs no server.
