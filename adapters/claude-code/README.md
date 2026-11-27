# Claude Code adapter

This adapter exposes Lemanon's explicit modes as one Claude Code command. It is
deliberately thin: `skills/lemanon/SKILL.md` remains canonical.

Do not fork or copy the workflow into this adapter. Updating two independent
instruction sets would make handoff semantics host-dependent.

## Install

Keep a local checkout of Lemanon, then copy or link
`commands/lemanon.md` into either:

- `.claude/commands/lemanon.md` for one project
- `$HOME/.claude/commands/lemanon.md` for the current user

Replace `LEMANON_REPOSITORY` in the installed command with the absolute path to
the checkout. That configured path must contain `skills/lemanon/SKILL.md`.
Do not point it at a copied or edited substitute.

Invoke `/lemanon init`, `/lemanon onboard`, `/lemanon handoff`,
`/lemanon receive`, `/lemanon close`, or `/lemanon audit`. The command passes
its arguments to the canonical workflow; project rules and authorization still
take precedence.

## Uninstall

Remove only the installed command file or symlink. Project knowledge remains
ordinary Markdown and must not be deleted implicitly.
