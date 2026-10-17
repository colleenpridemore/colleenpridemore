#!/usr/bin/env python3
"""Generate a human-friendly techstack.md from techstack.yml."""
from collections import defaultdict
from datetime import datetime
import pathlib, sys

try:
    import yaml
except Exception:
    print("Install PyYAML: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

INPUT_FILE = pathlib.Path("techstack.yml")
OUTPUT_FILE = pathlib.Path("techstack.md")

if not INPUT_FILE.exists():
    print(f"{INPUT_FILE} not found", file=sys.stderr)
    sys.exit(1)

data = yaml.safe_load(INPUT_FILE.read_text(encoding="utf-8")) or {}

repo_name = data.get("repo_name", INPUT_FILE.stem)
report_id = data.get("report_id", "unknown")
version = data.get("version", "1.0")
repo_type = data.get("repo_type", "unknown")
timestamp = data.get("timestamp", datetime.utcnow().isoformat() + "Z")
requested_by = data.get("requested_by", "")
provider = data.get("provider", "")
branch = data.get("branch", "")

tools = data.get("tools", [])

groups = defaultdict(list)
for tool in tools:
    category = tool.get("category", "Uncategorized")
    groups[category].append(tool)

lines = []
lines.append(f"# {repo_name}")
lines.append("")
lines.append(f"**Report ID**: {report_id}")
lines.append(f"**Version**: {version}")
lines.append(f"**Repository Type**: {repo_type}")
lines.append(f"**Timestamp**: {timestamp}")
lines.append(f"**Requested By**: {requested_by}")
lines.append(f"**Provider**: {provider}")
lines.append(f"**Branch**: {branch}")
lines.append("")
lines.append("## Tech Stack")
lines.append("")

if not tools:
    lines.append("No tools detected. Edit `techstack.yml` to add your tooling.")
else:
    for category in sorted(groups.keys()):
        group_tools = groups[category]
        lines.append(f"### {category} ({len(group_tools)})")
        lines.append("")
        lines.append("| Icon | Tool | Description | Website | Open Source | Hosted SaaS |")
        lines.append("|---|---|---|---|---:|---:|")
        for tool in group_tools:
            name = tool.get("name", "Unnamed")
            desc = tool.get("description", "—").replace("\n", " ")
            website = tool.get("website_url", "")
            site_md = f"[{website}]({website})" if website else "—"
            open_source = "Yes" if tool.get("open_source") else "No"
            hosted = "Yes" if tool.get("hosted_saas") else "No"
            img = tool.get("image_url", "")
            icon_md = f"<img src=\"{img}\" width=\"36\" height=\"36\" alt=\"{name}\" />" if img else ""
            tool_md = f"[{name}]({website})" if website else name
            lines.append(f"| {icon_md} | {tool_md} | {desc} | {site_md} | {open_source} | {hosted} |")
        lines.append("")

lines.append("---")
lines.append("")
lines.append("Generated from `techstack.yml`. To re-generate locally: `python3 generate_readme.py`")
lines.append("")

OUTPUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {OUTPUT_FILE}")
