#!/usr/bin/env python3
"""
Render dashboard.html from radar.json.

Reads radar.json, computes diff vs previous version (if exists),
and renders the HTML dashboard with data injected as JSON blob.

Usage:
    python scripts/render.py

Outputs:
    - docs/index.html (main dashboard)
    - docs/archive/YYYY-MM-DD-HH-MM-SS.html (timestamped snapshot)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import hashlib

try:
    from jinja2 import Template
except ImportError:
    print("Error: jinja2 library not installed. Install with: pip install jinja2")
    sys.exit(1)


def load_json(path: Path) -> Dict[str, Any]:
    """Load JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return {}


def compute_diff(old_data: Dict, new_data: Dict) -> List[str]:
    """Compute human-readable diff between old and new radar data."""
    changes = []

    old_topics = {t['name']: t for t in old_data.get('topics', [])}
    new_topics = {t['name']: t for t in new_data.get('topics', [])}

    # New topics
    for name in new_topics:
        if name not in old_topics:
            changes.append(f"Added: {name}")

    # Removed topics
    for name in old_topics:
        if name not in new_topics:
            changes.append(f"Removed: {name}")

    # Updated topics (version changes)
    for name in old_topics:
        if name in new_topics:
            old_version = old_topics[name].get('latest_version', '')
            new_version = new_topics[name].get('latest_version', '')
            if old_version != new_version:
                changes.append(f"Updated: {name} ({old_version} -> {new_version})")

    return changes


def render_dashboard(radar_data: Dict, changes: List[str]) -> str:
    """Render HTML dashboard with embedded JSON data."""

    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    template_file = project_root / "templates" / "dashboard.html"

    if not template_file.exists():
        print(f"Error: Template not found at {template_file}")
        return ""

    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Create a simple template that injects the data
    # The template is mostly static HTML with a script tag injection point

    # Prepare JSON data for embedding
    json_data = json.dumps(radar_data.get('topics', []))

    # Create changes text
    changes_text = "No changes detected" if not changes else "; ".join(changes[:3])
    if len(changes) > 3:
        changes_text += f" and {len(changes) - 3} more changes"

    # Inject data into HTML
    script_injection = f"""
    <script>
        window.TOPICS_DATA = {json_data};
    </script>
    """

    # Insert script before closing </head> or at the end
    output = template_content.replace('</head>', f'{script_injection}</head>', 1)
    if '</head>' not in template_content:
        output = output.replace('</body>', f'{script_injection}</body>', 1)

    return output


def write_outputs(html_content: str, radar_file: Path):
    """Write output files."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # docs directory is inside tech-radar
    docs_dir = project_root / "docs"
    archive_dir = docs_dir / "archive"

    # Create directories
    docs_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Write main dashboard
    index_file = docs_dir / "index.html"
    try:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[PASS] Rendered {index_file}")
    except Exception as e:
        print(f"Error writing {index_file}: {e}")
        return False

    # Write archive snapshot with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    archive_file = archive_dir / f"{timestamp}.html"
    try:
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[PASS] Archived snapshot to {archive_file}")
    except Exception as e:
        print(f"Error writing {archive_file}: {e}")
        return False

    return True


def render():
    """Main render function."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Paths
    radar_file = project_root / "data" / "radar.json"
    backup_file = project_root / "data" / ".radar.backup.json"

    # Load new data
    new_data = load_json(radar_file)
    if not new_data:
        print("Error: No data to render")
        return False

    # Load old data for diff
    old_data = load_json(backup_file) if backup_file.exists() else {}
    changes = compute_diff(old_data, new_data)

    # Render HTML
    html_content = render_dashboard(new_data, changes)
    if not html_content:
        print("Error: Failed to render HTML")
        return False

    # Write outputs
    if not write_outputs(html_content, radar_file):
        print("Error: Failed to write outputs")
        return False

    # Update backup
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not update backup: {e}")

    # Print changes summary
    if changes:
        print(f"\nChanges detected ({len(changes)} total):")
        for change in changes[:5]:
            print(f"  * {change}")
        if len(changes) > 5:
            print(f"  ... and {len(changes) - 5} more")
    else:
        print("\nNo changes detected")

    return True


if __name__ == "__main__":
    success = render()
    sys.exit(0 if success else 1)
