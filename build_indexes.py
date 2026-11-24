from pathlib import Path
import re

AREAS = [
    "Projects",
    "Skills & AI",
    "Writing & Worlds",
    "Music",
    "Ideas & Research",
    "Personal",
]

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def parse_frontmatter(text: str) -> dict:
    match = FM_RE.match(text)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data

def build_area_index(root: Path, area: str):
    area_dir = root / area
    if not area_dir.exists():
        return

    grouped = {}
    for md in sorted(area_dir.rglob("*.md")):
        if md.name == "_index.md":
            continue
        meta = parse_frontmatter(md.read_text(encoding="utf-8", errors="ignore"))
        project = meta.get("project", "none") or "none"
        status = meta.get("status", "reference")
        summary = meta.get("summary", "(no summary yet)")
        rel_path = md.relative_to(area_dir).as_posix()
        grouped.setdefault(project, []).append((status, md.stem, rel_path, summary))

    lines = [f"# {area} — Index\n"]
    for project in sorted(grouped.keys(), key=lambda x: (x == "none", x.lower())):
        heading = "General" if project == "none" else project
        lines.append(f"\n## {heading}\n")
        lines.append("| Note | Status | Summary |")
        lines.append("|---|---|---|")
        for status, title, rel_path, summary in grouped[project]:
            lines.append(f"| [{title}]({rel_path}) | `{status}` | {summary} |")

    (area_dir / "_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Built {area}/_index.md ({sum(len(v) for v in grouped.values())} notes)")

if __name__ == "__main__":
    repo_root = Path(".")
    for area in AREAS:
        build_area_index(repo_root, area)