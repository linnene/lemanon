# Onboard

Use this mode to recover enough current context to act safely. It is not a
request to ingest the full archive.

## Read order

Read only as far as necessary, in this order:

- repository-root `AGENTS.md`
- `knowledge/AGENTS.md`
- `knowledge/PROJECT.md`
- `knowledge/STATUS.md`
- `knowledge/ROADMAP.md`
- the handoff index in `knowledge/handoffs/README.md`

Then open only the handoff, decision, evidence, source, or history records
needed for the active task. Prefer the newest relevant record, but resolve its
branch, commit, status, and provenance before relying on it.

## Output contract

State the current objective, verified state, open uncertainty, applicable
authorization, prohibited actions, and the smallest useful next action. Mark
producer claims as unverified until checked against their owning source.

Stop reading when those points can be answered. If they cannot, name the
missing record instead of guessing or loading the archive indiscriminately.
