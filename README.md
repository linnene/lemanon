# Lemanon

**Continuity skills for long-running agent projects.**

Lemanon is an installable, Git-native skill for creating and maintaining a
Markdown project knowledge base across chats, context compaction, and agent
handoffs.

The first release targets Codex, with a thin Claude Code adapter, and keeps
every generated project usable without Lemanon. It does not require a database
or background service.

## Status

Lemanon v0.1 is being prepared for its first public release.

## Install

Clone this repository, then expose the canonical skill directory to Codex:

```sh
git clone https://github.com/linnene/lemanon.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/lemanon/skills/lemanon" "${CODEX_HOME:-$HOME/.codex}/skills/lemanon"
```

Restart Codex if the skill is not discovered immediately. Invocation is
explicit by design: start with `$lemanon init` inside the intended project.
Lemanon never selects an external server or expands task authorization.

For Claude Code, follow
[`adapters/claude-code/README.md`](adapters/claude-code/README.md). The adapter
delegates to the same `skills/lemanon/SKILL.md`; it is not an independent fork.

## Lifecycle

- `$lemanon init` adds only missing core knowledge files and preserves existing
  rules.
- `$lemanon onboard` reads rules and hot state before opening relevant history.
- `$lemanon handoff` records a producer-owned recovery snapshot.
- `$lemanon receive` verifies another producer's claims without rewriting them.
- `$lemanon close` promotes supported outcomes into durable current state.
- `$lemanon audit` performs a read-only structure, privacy, and provenance
  review.

The normal path is `init` once, `onboard` at the start of a session, `handoff`
when work changes owner, `receive` by the next owner, and `close` when supported
outcomes can be synchronized. Run `audit` before sharing or after substantial
knowledge changes. See the synthetic
[`sample-project`](examples/sample-project/README.md) walkthrough.

## Uninstall

Remove the installed skill link or copied `lemanon` skill directory and, if
used, the Claude Code command adapter. The generated project knowledge remains ordinary Markdown under version control and continues to work without Lemanon.
Do not automatically delete a project's `knowledge/` directory during
uninstall.

## License

MIT
