# Handoff

Use a handoff to make unfinished work recoverable by another session or agent.
A handoff is a producer-owned snapshot, not an independent verification or a
grant of authority.

## Procedure

- Resolve the project root and applicable rules.
- Copy `assets/scaffold/templates/HANDOFF.md` into a producer-specific folder
  under `knowledge/handoffs/`.
- Record the exact branch and commit. If work is uncommitted, say so and list
  the relevant paths without implying they are durable.
- Separate verified evidence from claims, pending work, blockers, and failed
  attempts.
- Record evidence locations instead of copying raw data from its owning
  system.
- State the receiver only when known; otherwise use `unassigned`.
- State existing authorization and prohibited actions explicitly. Never infer
  permission to merge, push, publish, delete, or run remote work.
- Add a link and status to the handoff index without rewriting prior records.

Use `draft`, `ready`, `accepted`, `closed`, or `superseded` as status values.
The producer may correct its own record by appending a dated correction; do
not erase the earlier claim.
