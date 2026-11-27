# Close

Use close after an outcome has a supported status and the durable knowledge
base must reflect it. Closing work does not authorize merge, push, publication,
deletion, remote execution, or any other external mutation.

## Synchronization targets

Update only the targets justified by the outcome:

- `STATUS.md` for current verified state, active blockers, and the next useful
  action
- `decisions/` for a decision, its alternatives, evidence, and consequences
- `evidence/` for compact verification records and owning artifact locations
- `HISTORY.md` for a concise chronological milestone or failure worth retaining
- the handoff index for the terminal or superseding status of the record

Keep detailed work logs out of hot state. Link to durable records instead.
Preserve negative results and limits when they may change a later decision.

## Completion check

Before marking work closed, confirm that the status wording does not overstate
the evidence, that branch and commit references resolve, and that pending work
is either retained with an owner or explicitly dropped. If evidence remains
insufficient, close the session as unresolved rather than closing the claim.
