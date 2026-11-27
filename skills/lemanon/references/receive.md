# Receive

Use this mode to inspect and accept or reject a producer handoff.

## Ownership and verification

Never rewrite the producer record. Record receiver findings separately. Check
the exact branch and commit before inspecting implementation claims, and open
only the evidence needed to distinguish acceptance from a competing
explanation.

A claim becomes shared project state only after it has been independently
accepted. Acceptance means the receiver verified the relevant source and
recorded the scope and limits of that verification; it does not mean every
claim in the handoff is true.

## Procedure

- Read project rules and hot state using the onboard order.
- Confirm producer, receiver, status, exact branch and commit, and evidence
  locations.
- Classify each consequential claim as accepted, rejected, unresolved, or not
  checked.
- Record the verification method and its result in a receiver-owned note.
- Promote only independently accepted facts to `knowledge/STATUS.md` or other
  authoritative records.
- Use `handoffs/shared/` only for neutral coordination material jointly owned
  by multiple agents, never to blur producer ownership.
- Preserve the authorization boundary. Receiving a record grants no new
  authorization to merge, push, publish, delete, or execute external work.

If the named commit is unavailable or evidence cannot be reached, leave the
handoff unresolved and report the exact blocker.
