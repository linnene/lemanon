# Signal Garden: synthetic lifecycle

Signal Garden is a fictional repository used only to show the Lemanon flow. It
contains no private project facts, real infrastructure, or experimental data.

## Initialize

Run `$lemanon init` once at the repository root. Existing `AGENTS.md` content
is preserved. If it does not point to `knowledge/AGENTS.md`, Lemanon proposes a
manual addition instead of overwriting the file.

## Start a session

Run `$lemanon onboard`. The agent reads repository rules, knowledge rules,
project identity, current status, roadmap, and the handoff index in that order.
It opens older records only when they are relevant to the active task.

## Transfer unfinished work

Run `$lemanon handoff`. A producer records the exact branch and commit,
verified evidence locations, open blockers, failed attempts, and authorization
boundaries in its own handoff directory.

The receiving agent runs `$lemanon receive`. It preserves the producer record,
checks the named source and evidence, and records which claims were accepted,
rejected, unresolved, or not checked.

## Synchronize an outcome

Run `$lemanon close` only after the result has a supported status. Current state,
decisions, compact evidence, history, and the handoff index are updated only
where justified. Closing does not authorize merge, push, publication, deletion,
or remote execution.

## Review the knowledge base

Run `$lemanon audit`. The audit is read-only by default and reports structural,
privacy, provenance, link, size, and freshness issues without silently fixing
them.
