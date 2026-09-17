#!/usr/bin/env python3
"""Assert the cross-file invariants documented in CONTRIBUTING.md.

Every rule in CONTRIBUTING.md maps to a check here. If you add a rule there,
add the check here too — and vice versa.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAXONOMY = ("languages", "development", "frameworks")
ENTRY_KEYS = {"name", "source", "category", "tags"}
EXCLUDED = {"templates", ".github", ".git", ".claude-plugin", ".codegraph"}
MIN_DESCRIPTION = 40

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(path: Path) -> dict[str, str]:
    """Parse the leading YAML frontmatter, handling folded (>) and literal (|) scalars."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    key: str | None = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line[:1].strip() and ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            fields[key] = "" if value in (">", "|", ">-", "|-", ">+", "|+") else value
        elif key and line[:1] in (" ", "\t"):
            fields[key] = f"{fields[key]} {line.strip()}".strip()
    return fields


def declared_skills() -> dict[str, Path]:
    """Root-level directories that are single-skill plugins."""
    found: dict[str, Path] = {}
    for path in sorted(ROOT.iterdir()):
        if not path.is_dir() or path.name in EXCLUDED:
            continue
        if (path / ".claude-plugin" / "plugin.json").is_file():
            found[path.name] = path
    return found


def latest_version_tag() -> str | None:
    result = subprocess.run(
        ["git", "tag", "-l", "v*", "--sort=-v:refname"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    for tag in result.stdout.split():
        if re.fullmatch(r"v\d+\.\d+\.\d+", tag):
            return tag[1:]
    return None


def main() -> int:
    marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json")
    entries = marketplace.get("plugins", [])
    skills = declared_skills()

    entry_names = [entry.get("name") for entry in entries]
    if len(entry_names) != len(set(entry_names)):
        fail("marketplace.json has duplicate entry names")
    for name in sorted(set(entry_names) - set(skills)):
        fail(f"marketplace entry '{name}' has no matching skill directory")
    for name in sorted(set(skills) - set(entry_names)):
        fail(f"skill directory '{name}' has no matching marketplace entry")

    versions: dict[str, str] = {}

    for entry in entries:
        name = entry.get("name")
        if set(entry) != ENTRY_KEYS:
            fail(f"entry '{name}': keys must be exactly {sorted(ENTRY_KEYS)}, got {sorted(entry)}")
        if entry.get("source") != f"./{name}":
            fail(f"entry '{name}': source must be './{name}', got {entry.get('source')!r}")
        if entry.get("category") not in TAXONOMY:
            fail(f"entry '{name}': category must be one of {list(TAXONOMY)}, got {entry.get('category')!r}")

        directory = skills.get(name)
        if directory is None:
            continue

        manifest = read_json(directory / ".claude-plugin" / "plugin.json")
        skill = frontmatter(directory / "SKILL.md")

        if manifest.get("name") != name:
            fail(f"'{name}': plugin.json name is {manifest.get('name')!r}; must equal the directory name")
        if skill.get("name") != name:
            fail(f"'{name}': SKILL.md frontmatter name is {skill.get('name')!r}; must equal the directory name")

        description = skill.get("description", "")
        if not description:
            fail(f"'{name}': SKILL.md frontmatter is missing a description")
        elif len(description) < MIN_DESCRIPTION:
            fail(f"'{name}': SKILL.md description is {len(description)} chars; minimum is {MIN_DESCRIPTION}")

        if sorted(entry.get("tags", [])) != sorted(manifest.get("keywords", [])):
            fail(
                f"'{name}': entry tags {sorted(entry.get('tags', []))} "
                f"!= plugin.json keywords {sorted(manifest.get('keywords', []))}"
            )

        versions[name] = manifest.get("version", "")

    distinct = sorted(set(versions.values()))
    if len(distinct) > 1:
        fail(f"plugin versions must be identical across the catalog, got {versions}")
    elif distinct:
        version = distinct[0]
        tag = latest_version_tag()
        if tag is not None and tag != version:
            fail(f"catalog version is {version} but the latest v* tag is v{tag}")
        changelog = ROOT / "CHANGELOG.md"
        if not changelog.is_file():
            fail("CHANGELOG.md is missing")
        elif not re.search(rf"^##\s*\[{re.escape(version)}\]", changelog.read_text(encoding="utf-8"), re.M):
            fail(f"CHANGELOG.md has no '## [{version}]' entry")

    if errors:
        print(f"invariant check failed ({len(errors)} problem(s)):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"invariants hold for {len(skills)} skill(s); version {distinct[0] if distinct else 'n/a'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
