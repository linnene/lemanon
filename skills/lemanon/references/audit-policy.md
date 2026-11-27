# Audit policy

`$lemanon audit` is read-only. It reports findings without changing files,
accepting claims, or repairing history.

## Severity

- `error`: missing core knowledge or credential-like content.
- `warning`: broken or out-of-scope links, user-specific absolute paths,
  files above 1 MiB, invalid audit configuration, or status not verified in
  more than 90 days.
- `info`: useful lifecycle state that is not itself unsafe, including a newly
  initialized project awaiting its first verification.

Finding details never reproduce a suspected credential or username.

## Large-file allowlist

Projects may add `.lemanon-audit.json`:

```json
{
  "large_files": ["docs/reference.pdf"]
}
```

Paths are repository-relative and exempt only the size warning. Secret and
personal-path checks still apply. Invalid configuration produces a warning and
grants no exemption.

## Scope

The audit skips Git metadata, Lemanon execution workspaces, Python caches, and
symlinks. Relative Markdown links that leave the project are reported instead
of followed.
