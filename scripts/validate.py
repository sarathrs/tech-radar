#!/usr/bin/env python3
"""
Validate radar.json against the schema.

Usage:
    python scripts/validate.py

Exit codes:
    0 - Valid
    1 - Invalid
"""

import json
import sys
from pathlib import Path
from datetime import datetime

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema library not installed. Install with: pip install jsonschema")
    sys.exit(1)


def validate_radar():
    """Load and validate radar.json against radar.schema.json."""

    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    radar_file = project_root / "data" / "radar.json"
    schema_file = project_root / "schema" / "radar.schema.json"

    # Check files exist
    if not radar_file.exists():
        print(f"Error: {radar_file} not found")
        return False

    if not schema_file.exists():
        print(f"Error: {schema_file} not found")
        return False

    # Load files
    try:
        with open(radar_file, 'r', encoding='utf-8') as f:
            radar_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing {radar_file}: {e}")
        return False
    except Exception as e:
        print(f"Error reading {radar_file}: {e}")
        return False

    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing {schema_file}: {e}")
        return False
    except Exception as e:
        print(f"Error reading {schema_file}: {e}")
        return False

    # Validate
    try:
        jsonschema.validate(instance=radar_data, schema=schema)
    except jsonschema.ValidationError as e:
        print(f"Schema validation error:")
        print(f"  Path: {'.'.join(str(p) for p in e.absolute_path)}")
        print(f"  Message: {e.message}")
        return False
    except jsonschema.SchemaError as e:
        print(f"Schema error: {e.message}")
        return False

    # Additional checks
    errors = []

    # Check all topics have at least one link
    for i, topic in enumerate(radar_data.get("topics", [])):
        if not topic.get("links"):
            errors.append(f"Topic {i} ({topic.get('name', 'unknown')}): no links")

        if len(topic.get("links", [])) > 0:
            for j, link in enumerate(topic["links"]):
                if not link.get("url"):
                    errors.append(f"Topic {i}, link {j}: missing URL")

    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    # Success
    print(f"[PASS] {radar_file} is valid")
    print(f"  Topics: {len(radar_data.get('topics', []))}")
    print(f"  Validated against: {schema_file}")
    return True


if __name__ == "__main__":
    success = validate_radar()
    sys.exit(0 if success else 1)
