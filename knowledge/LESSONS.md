# Lessons and reversed conclusions

- A handoff is recoverable producer context, not verified shared truth. Receiver
  verification is required before promotion.
- Host adapters must delegate to one canonical skill. Copying the workflow would
  create incompatible semantics over time.
- Public release auditing must scan fixtures and documentation as well as
  implementation files; synthetic test values should be constructed without
  embedding credential-like or personal-path literals in source.
