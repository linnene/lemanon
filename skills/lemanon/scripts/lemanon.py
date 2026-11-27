#!/usr/bin/env python3
"""Dependency-free deterministic helpers for the Lemanon skill."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Sequence


SKILL_DIR = Path(__file__).resolve().parents[1]
SCAFFOLD = SKILL_DIR / "assets" / "scaffold"

CORE_ASSETS = {
    "AGENTS.md": SCAFFOLD / "AGENTS.md",
    "knowledge/AGENTS.md": SCAFFOLD / "knowledge" / "AGENTS.md",
    "knowledge/README.md": SCAFFOLD / "knowledge" / "README.md",
    "knowledge/PROJECT.md": SCAFFOLD / "knowledge" / "PROJECT.md",
    "knowledge/STATUS.md": SCAFFOLD / "knowledge" / "STATUS.md",
    "knowledge/ROADMAP.md": SCAFFOLD / "knowledge" / "ROADMAP.md",
    "knowledge/SOURCES.md": SCAFFOLD / "knowledge" / "SOURCES.md",
    "knowledge/HISTORY.md": SCAFFOLD / "knowledge" / "HISTORY.md",
    "knowledge/LESSONS.md": SCAFFOLD / "knowledge" / "LESSONS.md",
    "knowledge/handoffs/README.md": (
        SCAFFOLD / "knowledge" / "handoffs" / "README.md"
    ),
}

LARGE_FILE_BYTES = 1024 * 1024
STALE_STATUS_DAYS = 90
SKIP_PARTS = {".git", ".superpowers", "__pycache__"}
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
LAST_VERIFIED = re.compile(r"(?im)^-?\s*Last verified:\s*(\d{4}-\d{2}-\d{2})\s*$")
PERSONAL_PATHS = (
    re.compile("/" + "Users" + r"/[^/\s]+"),
    re.compile("/" + "home" + r"/[^/\s]+"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+"),
)
SECRET_PATTERNS = (
    re.compile("AK" + r"IA[0-9A-Z]{16}"),
    re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|secret|password)"
        r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+\-]{16,}"
    ),
)


@dataclass(frozen=True)
class InitReport:
    created: list[str]
    existing: list[str]
    proposals: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, list[str]]:
        return asdict(self)


@dataclass(frozen=True)
class AuditFinding:
    code: str
    path: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class AuditReport:
    error: list[AuditFinding]
    warning: list[AuditFinding]
    info: list[AuditFinding]

    def to_dict(self) -> dict[str, list[dict[str, str]]]:
        return {
            severity: [finding.to_dict() for finding in getattr(self, severity)]
            for severity in ("error", "warning", "info")
        }


def _has_knowledge_pointer(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return "knowledge/AGENTS.md" in text


def init_project(project: Path, dry_run: bool = False) -> InitReport:
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError(f"project directory does not exist: {project}")

    created: list[str] = []
    existing: list[str] = []
    proposals: list[str] = []
    warnings: list[str] = []

    for relative, asset in CORE_ASSETS.items():
        destination = project / relative
        if destination.exists():
            existing.append(relative)
            if not destination.is_file():
                warnings.append(relative)
                continue
            if relative == "AGENTS.md" and not _has_knowledge_pointer(destination):
                proposals.append(relative)
            continue

        created.append(relative)
        if dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(asset.read_bytes())

    return InitReport(
        created=sorted(created),
        existing=sorted(existing),
        proposals=sorted(proposals),
        warnings=sorted(warnings),
    )


def _project_files(project: Path) -> list[Path]:
    return sorted(
        path
        for path in project.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and not any(part in SKIP_PARTS for part in path.relative_to(project).parts)
    )


def _load_large_file_allowlist(project: Path) -> tuple[set[str], list[AuditFinding]]:
    config = project / ".lemanon-audit.json"
    if not config.exists():
        return set(), []
    try:
        payload = json.loads(config.read_text(encoding="utf-8"))
        values = payload.get("large_files", [])
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise ValueError("large_files must be a string list")
        return {Path(item).as_posix() for item in values}, []
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return set(), [
            AuditFinding(
                code="invalid-audit-config",
                path=".lemanon-audit.json",
                detail="audit allowlist is not a valid large_files string list",
            )
        ]


def _decode_for_scan(path: Path) -> str:
    return path.read_bytes().decode("utf-8", errors="replace")


def _audit_markdown_links(project: Path, path: Path, text: str) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    relative = path.relative_to(project).as_posix()
    for raw_target in MARKDOWN_LINK.findall(text):
        target = raw_target.strip().strip("<>").split(maxsplit=1)[0]
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        candidate = (path.parent / target).resolve()
        try:
            candidate.relative_to(project)
        except ValueError:
            findings.append(
                AuditFinding("outside-project-link", relative, "relative link leaves project scope")
            )
            continue
        if not candidate.exists():
            findings.append(
                AuditFinding("broken-link", relative, "relative Markdown target does not exist")
            )
    return findings


def audit_project(project: Path) -> AuditReport:
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError(f"project directory does not exist: {project}")

    errors: list[AuditFinding] = []
    warnings: list[AuditFinding] = []
    info: list[AuditFinding] = []

    for relative in CORE_ASSETS:
        if not (project / relative).is_file():
            errors.append(AuditFinding("missing-core", relative, "required core file is missing"))

    large_allowlist, config_warnings = _load_large_file_allowlist(project)
    warnings.extend(config_warnings)

    for path in _project_files(project):
        relative = path.relative_to(project).as_posix()
        if path.stat().st_size > LARGE_FILE_BYTES and relative not in large_allowlist:
            warnings.append(
                AuditFinding("large-file", relative, "file exceeds the default 1 MiB review threshold")
            )

        text = _decode_for_scan(path)
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            errors.append(
                AuditFinding("suspected-secret", relative, "credential-like value detected and redacted")
            )
        if any(pattern.search(text) for pattern in PERSONAL_PATHS):
            warnings.append(
                AuditFinding("personal-path", relative, "user-specific absolute home path detected")
            )
        if path.suffix.lower() == ".md":
            warnings.extend(_audit_markdown_links(project, path, text))

    status = project / "knowledge" / "STATUS.md"
    if status.is_file():
        text = status.read_text(encoding="utf-8", errors="replace")
        match = LAST_VERIFIED.search(text)
        if match:
            verified = date.fromisoformat(match.group(1))
            if (date.today() - verified).days > STALE_STATUS_DAYS:
                warnings.append(
                    AuditFinding("stale-status", "knowledge/STATUS.md", "last verification exceeds 90 days")
                )
        elif "Last verified: not yet verified" in text:
            info.append(
                AuditFinding("unverified-status", "knowledge/STATUS.md", "project has not recorded its first verification")
            )
        else:
            warnings.append(
                AuditFinding("missing-verification-date", "knowledge/STATUS.md", "status has no parseable Last verified field")
            )

    key = lambda item: (item.path, item.code, item.detail)
    return AuditReport(
        error=sorted(errors, key=key),
        warning=sorted(warnings, key=key),
        info=sorted(info, key=key),
    )


def _print_init_report(report: InitReport, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        return
    for label, values in report.to_dict().items():
        print(f"{label}:")
        for value in values:
            print(f"  - {value}")


def _print_audit_report(report: AuditReport, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        return
    for severity, findings in report.to_dict().items():
        print(f"{severity}:")
        for finding in findings:
            print(f"  - {finding['code']}: {finding['path']} — {finding['detail']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lemanon")
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init", help="initialize project knowledge")
    init_parser.add_argument("project", type=Path)
    init_parser.add_argument("--dry-run", action="store_true")
    init_parser.add_argument("--json", action="store_true", dest="as_json")
    audit_parser = subparsers.add_parser("audit", help="audit project knowledge")
    audit_parser.add_argument("project", type=Path)
    audit_parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "init":
        try:
            report = init_project(args.project, dry_run=args.dry_run)
        except ValueError as error:
            print(str(error))
            return 2
        _print_init_report(report, args.as_json)
        return 0
    if args.command == "audit":
        try:
            report = audit_project(args.project)
        except ValueError as error:
            print(str(error))
            return 2
        _print_audit_report(report, args.as_json)
        return 1 if report.error else 0
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
