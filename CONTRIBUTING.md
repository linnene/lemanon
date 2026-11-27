# Contributing

Contributions should preserve Lemanon's small, explicit, and non-destructive
model.

## Before changing behavior

- State the failure or decision the change addresses.
- Delete work that cannot change that decision.
- Add a focused failing test using a synthetic project and synthetic values.
- Keep host adapters thin; change the canonical skill rather than copying it.
- Preserve existing project files unless the user explicitly authorizes a
  change.

## Verification

Run the complete suite and repository audit on an authorized remote environment
or in CI when local execution is restricted:

```sh
python -m unittest discover -s tests -v
python skills/lemanon/scripts/lemanon.py audit . --json
```

Do not submit credentials, personal paths, private infrastructure names, raw
project data, or real customer content. Public examples must remain synthetic.
Explain any audit warning instead of suppressing it without a documented reason.
