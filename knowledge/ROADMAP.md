# Roadmap

## Current phase

Prepare and verify the public v0.1 release.

## Entry and exit gates

The release gate requires a clean remote unit suite, a clean repository audit,
no private project identifiers or infrastructure in public source, and a
passing public CI run at the published commit.

## Future phases

- Gather real-world onboarding and handoff failures without collecting private
  project content.
- Add adapters only when they can delegate to the canonical workflow.
- Automate repeated checks only after their policies remain stable.

## Authorization state

The repository owner authorized public repository creation and the initial
push. This plan does not authorize unrelated publication, deletion, or access
to external project data.
