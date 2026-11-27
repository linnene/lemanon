<p align="center">
  <img src="assets/lemanon-logo.png" alt="Lemanon lemon logo" width="148">
</p>

# Lemanon

**Pick up where the last agent left off.**

Lemanon is a Git-native skill that gives Codex and Claude Code a shared project
knowledge base. After a chat restart or context compaction, an agent can find
the current status, see why decisions were made, and verify a handoff by
following a few Markdown files.

[![Version v0.1.0](https://img.shields.io/badge/version-v0.1.0-445ad4)](https://github.com/linnene/lemanon/tree/v0.1.0)
[![CI](https://github.com/linnene/lemanon/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/linnene/lemanon/actions/workflows/checks.yml)
[![MIT license](https://img.shields.io/badge/license-MIT-16845b)](LICENSE)

[Quick start](#install) · [Workflow](#lifecycle) · [Example](examples/sample-project/README.md)

## Install

### Codex

Clone Lemanon into a directory you plan to keep, then link the skill into Codex:

```sh
git clone https://github.com/linnene/lemanon.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/lemanon/skills/lemanon" "${CODEX_HOME:-$HOME/.codex}/skills/lemanon"
```

Open the project you want to initialize. In the Codex chat, run
`$lemanon init`. If Codex does not discover the skill, restart it.

### Claude Code

Install the [Claude Code adapter](adapters/claude-code/README.md), then run
`/lemanon init` in your project. Both hosts use the same workflow.

## Lifecycle

Set up the knowledge base once. In a new session, use `onboard` to recover
context. When another agent takes over unfinished work, use `handoff` on the
sending side and `receive` on the receiving side.

| Codex command | What it does |
| --- | --- |
| `$lemanon init` | Add missing knowledge files and preserve existing project rules. |
| `$lemanon onboard` | Read project rules and current status, then open relevant background. |
| `$lemanon handoff` | Record the branch, commit, evidence, blockers, and next action. |
| `$lemanon receive` | Verify the handoff against its sources and record what was confirmed. |
| `$lemanon close` | Update project status and history with supported outcomes. |
| `$lemanon audit` | Check for missing files, broken links, stale status, and possible sensitive content in a read-only pass. |

Follow the full workflow in the [Signal Garden example](examples/sample-project/README.md).

## What lives in your repo

```text
knowledge/
├── AGENTS.md    Rules for maintaining the knowledge base
├── README.md    Index and entry points
├── PROJECT.md   Purpose, scope, and success criteria
├── STATUS.md    Current state, open questions, and next action
├── ROADMAP.md   Planned work and decision gates
├── SOURCES.md   Pointers to evidence and artifacts
├── HISTORY.md   Milestones and superseded state
├── LESSONS.md   Failed approaches and lessons worth keeping
└── handoffs/    Producer records and receiver notes
```

The repository root's `AGENTS.md` can point agents to these files. Commit the
Markdown alongside your code so future sessions can recover the context from
the same Git checkout. Keep large artifacts in their original location and
record their addresses in the knowledge base.

## Uninstall

Remove the installed skill link or directory and the Claude Code adapter if
installed. Your knowledge base remains ordinary Markdown under version control.

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [MIT License](LICENSE)
