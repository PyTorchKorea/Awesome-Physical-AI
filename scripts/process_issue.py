#!/usr/bin/env python3
"""
process_issue.py — Parse a GitHub Issue form body and append a new entry to the YAML.

Called by .github/workflows/process-issue.yml when a new "Add Model" or
"Add Dataset" issue is opened. The workflow passes the issue body and metadata
via environment variables, and this script:
  1. Parses the structured issue form
  2. Validates the entry
  3. Writes it to data/models.yaml or data/datasets.yaml
  4. The workflow then creates a PR for admin review

Environment variables (set by the GitHub Actions workflow):
  ISSUE_BODY        — raw issue body text
  ISSUE_TYPE        — "model" or "dataset"
  ISSUE_NUMBER      — GitHub issue number (for PR description)
  ISSUE_AUTHOR      — GitHub username of issue author

Usage (from GitHub Actions):
  python scripts/process_issue.py
"""

import os
import re
import sys
from pathlib import Path
from datetime import date

import yaml

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
TODAY = date.today().isoformat()


def parse_form(body: str) -> dict[str, str]:
    """Parse GitHub issue form body into a key→value dict.

    GitHub Forms render as:
        ### Field Label
        value
    """
    result: dict[str, str] = {}
    current_key = None
    current_lines: list[str] = []

    for line in body.splitlines():
        heading = re.match(r"^###\s+(.+)$", line)
        if heading:
            if current_key is not None:
                result[current_key] = "\n".join(current_lines).strip()
            current_key = heading.group(1).strip().lower().replace(" ", "_")
            current_lines = []
        elif current_key is not None:
            if line.strip() not in ("_No response_", ""):
                current_lines.append(line)

    if current_key is not None:
        result[current_key] = "\n".join(current_lines).strip()

    return result


def parse_list(value: str) -> list[str]:
    """Parse a comma-separated string into a cleaned list."""
    return [v.strip() for v in re.split(r"[,\n]+", value) if v.strip()]


def to_int(value: str, default: int = 0) -> int:
    try:
        return int(re.sub(r"[^\d]", "", value))
    except (ValueError, TypeError):
        return default


def build_model_entry(form: dict) -> dict:
    return {
        "id": re.sub(r"[^a-z0-9-]", "", form.get("id", "").lower().replace(" ", "-")),
        "name": form.get("name", ""),
        "org": form.get("organization", ""),
        "year": to_int(form.get("year", str(date.today().year))),
        "description_en": form.get("description_(english)", ""),
        "description_ko": form.get("description_(korean)", ""),
        "github_url": form.get("github_url", ""),
        "paper_url": form.get("paper_url_(arxiv)", ""),
        "hf_url": form.get("huggingface_url", ""),
        "project_url": form.get("project_page_url", ""),
        "categories": parse_list(form.get("categories", "")),
        "hardware": parse_list(form.get("hardware_targets", "")),
        "learning": parse_list(form.get("learning_methods", "")),
        "framework": parse_list(form.get("framework", "")),
        "communication": parse_list(form.get("communication", "")),
        "stats": {
            "github_stars": 0,
            "github_forks": 0,
            "hf_downloads": 0,
            "last_updated": TODAY,
        },
        "added_date": TODAY,
        "tags": parse_list(form.get("tags", "")),
    }


def build_dataset_entry(form: dict) -> dict:
    return {
        "id": re.sub(r"[^a-z0-9-]", "", form.get("id", "").lower().replace(" ", "-")),
        "name": form.get("name", ""),
        "org": form.get("organization", ""),
        "year": to_int(form.get("year", str(date.today().year))),
        "description_en": form.get("description_(english)", ""),
        "description_ko": form.get("description_(korean)", ""),
        "github_url": form.get("github_url", ""),
        "paper_url": form.get("paper_url_(arxiv)", ""),
        "hf_url": form.get("huggingface_url", ""),
        "project_url": form.get("project_page_url", ""),
        "categories": parse_list(form.get("categories", "")),
        "hardware": parse_list(form.get("hardware_targets", "")),
        "source": parse_list(form.get("data_source", "")),
        "modality": parse_list(form.get("modality", "")),
        "scale": {
            "trajectories": to_int(form.get("number_of_trajectories", "0")),
            "hours": to_int(form.get("total_hours", "0")),
            "environments": to_int(form.get("number_of_environments", "0")),
            "robots": to_int(form.get("number_of_robot_types", "0")),
        },
        "stats": {
            "github_stars": 0,
            "hf_downloads": 0,
            "last_updated": TODAY,
        },
        "added_date": TODAY,
        "tags": parse_list(form.get("tags", "")),
    }


def append_entry(yaml_path: Path, entry: dict) -> None:
    with open(yaml_path, encoding="utf-8") as f:
        entries = yaml.safe_load(f) or []

    # Check for duplicate id
    existing_ids = {e.get("id") for e in entries}
    if entry["id"] in existing_ids:
        print(f"::error::Entry with id '{entry['id']}' already exists in {yaml_path.name}")
        sys.exit(1)

    entries.append(entry)
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(entries, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    print(f"✅ Appended '{entry['id']}' to {yaml_path.name}")


def main() -> None:
    body = os.environ.get("ISSUE_BODY", "")
    issue_type = os.environ.get("ISSUE_TYPE", "").lower()
    issue_number = os.environ.get("ISSUE_NUMBER", "?")
    author = os.environ.get("ISSUE_AUTHOR", "unknown")

    if not body:
        print("::error::ISSUE_BODY is empty")
        sys.exit(1)

    if issue_type not in ("model", "dataset"):
        print(f"::error::ISSUE_TYPE must be 'model' or 'dataset', got: '{issue_type}'")
        sys.exit(1)

    form = parse_form(body)
    print(f"Parsed form fields: {list(form.keys())}")

    if issue_type == "model":
        entry = build_model_entry(form)
        yaml_path = DATA_DIR / "models.yaml"
    else:
        entry = build_dataset_entry(form)
        yaml_path = DATA_DIR / "datasets.yaml"

    if not entry["id"]:
        print("::error::Could not determine entry 'id' from form")
        sys.exit(1)

    if not entry["name"]:
        print("::error::Entry 'name' is required")
        sys.exit(1)

    append_entry(yaml_path, entry)
    print(f"Entry '{entry['name']}' added by @{author} (issue #{issue_number})")


if __name__ == "__main__":
    main()
