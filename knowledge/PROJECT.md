# Project overview

## Purpose

Lemanon provides a small, installable project-continuity skill for agents that
work across long chats, context compaction, and changes of ownership.

## Users and outcomes

Developers and research teams should be able to recover current project state,
verify handoffs, and retain consequential decisions without loading a complete
archive into every session.

## Scope and boundaries

The project owns a Markdown-first schema, explicit lifecycle modes, deterministic
initialization and audit helpers, templates, and thin host adapters. It does not
replace Git, issue trackers, artifact storage, authorization, or task-specific
compute policy.

## Success and evidence

Success requires non-destructive initialization, idempotence, read-only audit,
producer-owned handoffs, receiver verification, portable installation, clean
public-source review, and a passing automated test suite.
