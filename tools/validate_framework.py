#!/usr/bin/env python3
# Validate framework identity, links, evidence boundaries, and release metadata.

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CITATION = ROOT / "CITATION.cff"
SOURCE_LOG = ROOT / "docs" / "sources-and-evidence.md"
SECURITY = ROOT / "SECURITY.md"

OLD_NAME = "AI-Compressed Cyber Defense Framework"
OLD_SLUG = "ai-compressed-cyber-defense-framework"
CURRENT_VERSION = "v0.1.1"
CURRENT_REPOSITORY = (
    "https://github.com/GLOBAL-AI-GOVERNANCE/"
    "ai-cyber-resilience-framework"
)

REQUIRED_HEADINGS = (
    "# AI Cyber Resilience Framework",
    "## Core Thesis",
    "## Why This Framework Exists",
    "## Included Artifacts",
    "## Start Here: 5-Minute Assessment",
    "## Finished Outcome",
    "## Full Getting Started Path",
    "## Public-Safe Boundary",
    "## Source Grounding",
    "## Evidence Boundary",
    "## Citation",
    "## License",
)

REQUIRED_README_PHRASES = (
    "Structural security against AI-compressed cyberattacks",
    "It is not executable software, certification, or proof",
    "Named human owners",
    "qualified people validate the supplied evidence",
    "Final conclusions require current authoritative sources",
    "human engineering judgment",
    "actions/workflows/framework-checks.yml/badge.svg?branch=main",
)

REQUIRED_SOURCE_URLS = (
    "https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final",
    "https://www.nist.gov/blogs/taking-measure/"
    "rethinking-cybersecurity-inside-out",
    "https://www.anthropic.com/glasswing",
    "https://www.anthropic.com/news/expanding-project-glasswing",
    "https://www.aisi.gov.uk/blog/"
    "our-evaluation-of-claude-mythos-previews-cyber-capabilities",
)

MARKDOWN_LINK = re.compile(
    r"!?\[[^\]]*\]\((?P<destination>[^)\n]+)\)"
)
FENCED_CODE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)


def fail(message: str) -> None:
    raise SystemExit(f"Framework validation failed: {message}")


def repository_files() -> list[Path]:
    completed = subprocess.run(
        [
            "git",
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [
        ROOT / item.decode("utf-8")
        for item in completed.stdout.split(b"\0")
        if item
    ]


def text_files(files: list[Path]) -> list[Path]:
    return [
        path
        for path in files
        if path.suffix.lower() in {
            ".md",
            ".cff",
            ".yml",
            ".yaml",
            ".py",
            ".txt",
        }
        or path.name == "NOTICE"
    ]


def validate_identity(files: list[Path]) -> None:
    validator_path = Path(__file__).resolve()

    for path in text_files(files):
        if path.resolve() == validator_path:
            continue

        text = path.read_text(encoding="utf-8-sig")
        relative = path.relative_to(ROOT)

        if OLD_NAME in text:
            fail(f"old public identity remains in {relative}")

        if OLD_SLUG in text:
            fail(f"stale repository slug remains in {relative}")


def validate_readme() -> None:
    text = README.read_text(encoding="utf-8-sig")
    heading_lines = [
        line.strip()
        for line in text.splitlines()
        if line.lstrip().startswith("#")
    ]

    for heading in REQUIRED_HEADINGS:
        if heading_lines.count(heading) != 1:
            fail(f"heading must appear exactly once: {heading}")

    for phrase in REQUIRED_README_PHRASES:
        if phrase not in text:
            fail(f"README requirement is missing: {phrase}")

    if CURRENT_VERSION not in text:
        fail(f"README does not identify {CURRENT_VERSION}")

    if CURRENT_REPOSITORY not in text:
        fail("README does not use the current repository URL")


def extract_destination(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1:value.index(">")].strip()
    return value.split()[0].strip() if value else ""


def validate_markdown_links(files: list[Path]) -> None:
    for markdown in files:
        if markdown.suffix.lower() != ".md":
            continue

        text = markdown.read_text(encoding="utf-8-sig")
        text = FENCED_CODE.sub("", text)

        for match in MARKDOWN_LINK.finditer(text):
            destination = extract_destination(match.group("destination"))
            lower = destination.lower()

            if (
                not destination
                or destination.startswith("#")
                or lower.startswith(
                    (
                        "http://",
                        "https://",
                        "mailto:",
                        "tel:",
                        "data:",
                    )
                )
            ):
                continue

            path_part = unquote(urlsplit(destination).path)
            if not path_part:
                continue

            target = (
                ROOT / path_part.lstrip("/")
                if path_part.startswith("/")
                else markdown.parent / path_part
            )

            if not target.exists():
                fail(
                    "broken local Markdown link in "
                    f"{markdown.relative_to(ROOT)}: {destination}"
                )


def validate_citation() -> None:
    text = CITATION.read_text(encoding="utf-8-sig")
    requirements = (
        'title: "AI Cyber Resilience Framework: '
        'Structural Security Against AI-Compressed Cyberattacks"',
        'version: "v0.1.1"',
        'date-released: "2026-07-29"',
        f'repository-code: "{CURRENT_REPOSITORY}"',
        '  type: "report"',
        '- name: "Global AI Governance contributors"',
    )

    for requirement in requirements:
        if requirement not in text:
            fail(f"CITATION.cff requirement is missing: {requirement}")


def validate_source_log() -> None:
    text = SOURCE_LOG.read_text(encoding="utf-8-sig")

    if "**Verification date:** 2026-07-29" not in text:
        fail("source verification date is not current")

    if "**Final live re-check:** 2026-07-29" not in text:
        fail("source live re-check date is not current")

    if "not an independent replication" not in text:
        fail("source revalidation boundary is missing")

    for url in REQUIRED_SOURCE_URLS:
        if url not in text:
            fail(f"source log URL is missing: {url}")


def validate_security() -> None:
    text = SECURITY.read_text(encoding="utf-8-sig")
    requirements = (
        "Use GitHub private vulnerability reporting",
        "Do not place sensitive vulnerability details",
        "does not certify an architecture",
        "Users remain responsible for authorization",
    )

    for requirement in requirements:
        if requirement not in text:
            fail(f"security boundary is missing: {requirement}")


def validate_workflow() -> None:
    workflow = ROOT / ".github" / "workflows" / "framework-checks.yml"
    text = workflow.read_text(encoding="utf-8")

    references = re.findall(
        r"^\s*uses:\s*([^\s#]+)",
        text,
        re.MULTILINE,
    )
    external = [
        reference
        for reference in references
        if not reference.startswith(("./", "docker://"))
    ]

    if len(external) != 1:
        fail(
            "expected exactly one external workflow action, "
            f"found {len(external)}"
        )

    if not re.search(r"@[0-9a-f]{40}$", external[0]):
        fail("workflow action is not pinned to a full commit SHA")

    if "permissions:\n  contents: read" not in text:
        fail("workflow permissions are not read-only")


def validate_hygiene(files: list[Path]) -> None:
    for path in files:
        relative = path.relative_to(ROOT)

        if "__pycache__" in relative.parts:
            fail(f"tracked Python cache directory: {relative}")

        if path.suffix.lower() in {".pyc", ".pyo"}:
            fail(f"tracked Python bytecode: {relative}")


def main() -> None:
    files = repository_files()

    for required in (README, CITATION, SOURCE_LOG, SECURITY):
        if not required.is_file():
            fail(f"required file is missing: {required.relative_to(ROOT)}")

    validate_identity(files)
    validate_readme()
    validate_markdown_links(files)
    validate_citation()
    validate_source_log()
    validate_security()
    validate_workflow()
    validate_hygiene(files)

    print(
        "Framework validation passed: "
        f"{len(files)} repository files checked; "
        "identity, links, citation, sources, security, "
        "workflow pins, and hygiene verified."
    )


if __name__ == "__main__":
    main()
