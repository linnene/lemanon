# Handoffs

Handoffs restore task state; they do not replace authoritative current status.

- Producers write under a producer-specific directory.
- Receivers verify claims and add their own record instead of rewriting history.
- `shared/` contains only accepted cross-agent contracts with named evidence.
