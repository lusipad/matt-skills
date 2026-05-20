#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_BUCKETS = ("engineering", "productivity", "misc")
PRIVATE_BUCKETS = ("personal", "in-progress", "deprecated")
CODEX_SKILLS_PATH = "./.agents/skills/"
UNSUPPORTED_PUBLIC_FRONTMATTER = (
    "argument-hint",
    "disable-model-invocation",
    "allowed-tools",
    "user-invocable",
    "model",
    "effort",
    "agent",
    "hooks",
)


def skill_dirs(bucket):
    root = ROOT / "skills" / bucket
    return sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )


def load(path):
    return path.read_text(encoding="utf-8")


def public_skills():
    skills = []
    for bucket in PUBLIC_BUCKETS:
        for path in skill_dirs(bucket):
            skills.append(
                {
                    "bucket": bucket,
                    "name": path.name,
                    "plugin_path": f"./skills/{bucket}/{path.name}",
                    "readme_link": f"./skills/{bucket}/{path.name}/SKILL.md",
                    "bucket_link": f"./{path.name}/SKILL.md",
                    "canonical_link": f"../../../skills/{bucket}/{path.name}/SKILL.md",
                }
            )
    return skills


def private_skills():
    skills = []
    for bucket in PRIVATE_BUCKETS:
        for path in skill_dirs(bucket):
            skills.append(
                {
                    "bucket": bucket,
                    "name": path.name,
                    "plugin_path": f"./skills/{bucket}/{path.name}",
                    "readme_link": f"./skills/{bucket}/{path.name}/SKILL.md",
                }
            )
    return skills


def frontmatter_name(text):
    match = re.search(r"(?m)^name:\s*([^\n]+)\s*$", text)
    return match.group(1).strip() if match else None


def main():
    errors = []
    public = public_skills()
    private = private_skills()

    readme = load(ROOT / "README.md")
    for skill in public:
        canonical_path = ROOT / "skills" / skill["bucket"] / skill["name"] / "SKILL.md"
        canonical_text = load(canonical_path)
        for field in UNSUPPORTED_PUBLIC_FRONTMATTER:
            if re.search(rf"(?m)^{re.escape(field)}\s*:", canonical_text):
                errors.append(
                    f"{canonical_path.relative_to(ROOT)} has platform-specific frontmatter field {field}"
                )

        if skill["readme_link"] not in readme:
            errors.append(f"README.md missing {skill['readme_link']}")

        bucket_readme = load(ROOT / "skills" / skill["bucket"] / "README.md")
        if skill["bucket_link"] not in bucket_readme:
            errors.append(
                f"skills/{skill['bucket']}/README.md missing {skill['bucket_link']}"
            )

    for skill in private:
        if skill["readme_link"] in readme:
            errors.append(f"README.md exposes private skill {skill['readme_link']}")

    claude_manifest = json.loads(load(ROOT / ".claude-plugin" / "plugin.json"))
    claude_paths = claude_manifest.get("skills")
    expected_claude_paths = [skill["plugin_path"] for skill in public]
    if sorted(claude_paths or []) != sorted(expected_claude_paths):
        errors.append(
            ".claude-plugin/plugin.json skills mismatch: "
            f"expected {expected_claude_paths}, got {claude_paths}"
        )

    codex_manifest = json.loads(load(ROOT / ".codex-plugin" / "plugin.json"))
    if codex_manifest.get("skills") != CODEX_SKILLS_PATH:
        errors.append(
            f".codex-plugin/plugin.json must set skills to {CODEX_SKILLS_PATH}"
        )

    root_names = {path.name for path in ROOT.iterdir()}
    if ".Codex-plugin" in root_names:
        errors.append("Use lowercase .codex-plugin, not .Codex-plugin")

    adapters_root = ROOT / ".agents" / "skills"
    adapter_paths = sorted(
        path for path in adapters_root.iterdir() if (path / "SKILL.md").is_file()
    )
    expected_adapter_names = sorted(skill["name"] for skill in public)
    adapter_names = [path.name for path in adapter_paths]
    if adapter_names != expected_adapter_names:
        errors.append(
            ".agents/skills adapters mismatch: "
            f"expected {expected_adapter_names}, got {adapter_names}"
        )

    public_by_name = {skill["name"]: skill for skill in public}
    for adapter in adapter_paths:
        text = load(adapter / "SKILL.md")
        name = adapter.name
        if frontmatter_name(text) != name:
            errors.append(f"{adapter / 'SKILL.md'} frontmatter name mismatch")
        canonical = public_by_name.get(name, {}).get("canonical_link")
        if canonical and canonical not in text:
            errors.append(f"{adapter / 'SKILL.md'} missing canonical link {canonical}")

    for skill in private:
        if (adapters_root / skill["name"]).exists():
            errors.append(f".agents/skills exposes private skill {skill['name']}")
        if skill["plugin_path"] in claude_paths:
            errors.append(f".claude-plugin exposes private skill {skill['plugin_path']}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "OK: README, bucket READMEs, Claude manifest, Codex manifest, and adapters are in sync."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
