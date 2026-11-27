---
name: lemanon
description: Use when a long-running project needs durable state across chats, context compaction, or handoffs between AI agents.
---

# Lemanon

## Overview

Lemanon keeps current project truth small, traceable, and recoverable. The
knowledge base is a navigation and continuity layer; Git, source artifacts,
and independently verified evidence remain authoritative for their own state.

## Modes

| Invocation | Outcome |
| --- | --- |
| `$lemanon init` | Create the missing minimum knowledge structure without replacing existing files. |
| `$lemanon onboard` | Recover current project state with the smallest useful read set. |
| `$lemanon handoff` | Write a producer-owned recovery record. |
| `$lemanon receive` | Verify another producer's record without rewriting its history. |
| `$lemanon close` | Synchronize durable outcomes into current state and history. |
| `$lemanon audit` | Inspect structure, provenance, privacy, and stale state without mutation by default. |

Use exactly one mode per invocation. Ask for the intended mode only when it
cannot be inferred from the explicit command.

## Mode routing

- For `$lemanon init`, use `scripts/lemanon.py` and preserve every existing
  file.
- For `$lemanon audit`, follow `references/audit-policy.md`; auditing is
  read-only by default.
- For `$lemanon onboard`, follow `references/onboard.md` and stop reading when
  the active task can be stated with evidence and uncertainty.
- For `$lemanon handoff`, follow `references/handoff.md` and use
  `assets/scaffold/templates/HANDOFF.md`.
- For `$lemanon receive`, follow `references/receive.md`; verify before
  promoting producer claims into shared state.
- For `$lemanon close`, follow `references/close.md`; synchronize only durable,
  supported outcomes.

## Safety contract

- Work only inside the project placed in scope.
- Never silently replace an existing rules or knowledge file.
- Treat handoffs as recovery snapshots, not verified current truth.
- Preserve external data in its owning system; record paths and necessary
  summaries instead of copying raw artifacts.
- Request task-specific authorization before merge, push, deletion,
  publication, remote execution, or other external mutation.

## Quick reference

Start a new project with `init`, a new session with `onboard`, and a receiving
session with `receive`. Use `handoff` before transferring unfinished work and
`close` only when an outcome has a supported status. Run `audit` before public
release or after substantial knowledge changes.

## Common mistakes

- Loading the whole archive before reading current status.
- Promoting a producer's claim without checking its commit and evidence.
- Duplicating raw logs or generated artifacts inside the knowledge base.
- Treating a roadmap item as execution authorization.
