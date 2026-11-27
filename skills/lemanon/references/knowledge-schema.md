# Knowledge schema

Lemanon separates hot current state from durable records and historical
sources. An initialized project starts with the core navigation layer; record
directories appear only when a workflow creates a real record.

## Core files

- `knowledge/PROJECT.md`: stable purpose, boundaries, and success conditions.
- `knowledge/STATUS.md`: authoritative current facts, blockers, and next work.
- `knowledge/ROADMAP.md`: future phases, gates, and authorization state.
- `knowledge/SOURCES.md`: locations and ownership of code, evidence, and assets.
- `knowledge/HISTORY.md`: phase changes and superseded state.
- `knowledge/LESSONS.md`: failures, reversed conclusions, and costly mistakes.
- `knowledge/handoffs/README.md`: producer ownership and shared-state rules.

## Invariants

- Current claims belong in `STATUS.md`; historical claims remain traceable.
- Plans never imply authorization.
- Handoffs are recovery records until independently verified and promoted.
- External artifacts stay in their owning system; store provenance and concise
  conclusions instead of raw copies.
- Existing files are preserved. Initialization reports proposed rule additions
  rather than silently editing them.
