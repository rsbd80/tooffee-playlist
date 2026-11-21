import json
import re
from pathlib import Path

SOURCE = Path("source_playlist.m3u")
OUTPUT_M3U = Path("toffee_playlist.m3u")
OUTPUT_JSON = Path("toffee_data.json")

if not SOURCE.exists():
    raise FileNotFoundError("source_playlist.m3u not found")

text = SOURCE.read_text(encoding="utf-8")
channels = []

name = None
logo = ""
group = ""

for line in text.splitlines():
    line = line.strip()

    if not line:
        continue

    if line.startswith("#EXTINF"):
        name = line.split(",", 1)[-1].strip()

        logo_match = re.search(r'tvg-logo="([^"]*)"', line)
        group_match = re.search(r'group-title="([^"]*)"', line)

        logo = logo_match.group(1) if logo_match else ""
        group = group_match.group(1) if group_match else ""

    elif not line.startswith("#") and name:
        channels.append({
            "name": name,
            "image": logo,
            "category": group,
            "url": line
        })
        name = None
        logo = ""
        group = ""

OUTPUT_M3U.write_text(text, encoding="utf-8")

OUTPUT_JSON.write_text(
    json.dumps(channels, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Generated {len(channels)} channels")
print("M3U:", OUTPUT_M3U)
print("JSON:", OUTPUT_JSON)
