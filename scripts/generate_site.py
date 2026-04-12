#!/usr/bin/env python3
"""
generate_site.py — Regenerate README.md and docs/data.json from YAML data files.

Run after updating data files (e.g., after update_stats.py or a new PR merge).

Usage:
  python scripts/generate_site.py
"""

import json
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
README_PATH = ROOT / "README.md"
TODAY = date.today().isoformat()

BADGE_BASE = "https://img.shields.io/badge"
REPO_URL = "https://github.com/PyTorchKR/Awesome-Physical-AI"
DASHBOARD_URL = "https://pytorchkr.github.io/Awesome-Physical-AI"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def badge(label: str, value: str, color: str = "blue") -> str:
    label_enc = label.replace("-", "--").replace(" ", "_")
    value_enc = str(value).replace("-", "--").replace(" ", "_")
    return f"![{label}]({BADGE_BASE}/{label_enc}-{value_enc}-{color})"


def stars_badge(n: int) -> str:
    if n >= 10000:
        s = f"{n // 1000}k%2B"
    elif n >= 1000:
        s = f"{n / 1000:.1f}k".rstrip("0").rstrip(".")
    else:
        s = str(n)
    return f"![Stars]({BADGE_BASE}/⭐-{s}-yellow)"


def link(text: str, url: str) -> str:
    return f"[{text}]({url})" if url else text


def tag_str(tags: list[str]) -> str:
    return " ".join(f"`{t}`" for t in tags)


# ─────────────────────────────────────────────────────────────────────────────
# README generation
# ─────────────────────────────────────────────────────────────────────────────

def model_row(m: dict) -> str:
    stats = m.get("stats", {})
    stars = stats.get("github_stars", 0)
    name_cell = link(m["name"], m.get("github_url") or m.get("project_url") or "")
    paper = f"[📄]({m['paper_url']})" if m.get("paper_url") else ""
    hf = f"[🤗]({m['hf_url']})" if m.get("hf_url") else ""
    cats = ", ".join(m.get("categories", []))
    hw = ", ".join(m.get("hardware", []))
    learn = ", ".join(m.get("learning", []))
    return (
        f"| {name_cell} | {m['org']} | {m['year']} | {cats} | {hw} | {learn} "
        f"| {stars:,} | {paper} {hf} |"
    )


def dataset_row(d: dict) -> str:
    stats = d.get("stats", {})
    stars = stats.get("github_stars", 0)
    dl = stats.get("hf_downloads", 0)
    name_cell = link(d["name"], d.get("github_url") or d.get("project_url") or "")
    paper = f"[📄]({d['paper_url']})" if d.get("paper_url") else ""
    hf = f"[🤗]({d['hf_url']})" if d.get("hf_url") else ""
    scale = d.get("scale", {})
    traj = f"{scale.get('trajectories', 0):,}" if scale.get("trajectories") else "—"
    cats = ", ".join(d.get("categories", []))
    src = ", ".join(d.get("source", []))
    mod = ", ".join(d.get("modality", []))
    return (
        f"| {name_cell} | {d['org']} | {d['year']} | {cats} | {src} | {mod} "
        f"| {traj} | {stars:,} | {paper} {hf} |"
    )


def generate_readme(models: list[dict], datasets: list[dict]) -> str:
    n_models = len(models)
    n_datasets = len(datasets)
    n_orgs = len({m["org"] for m in models} | {d["org"] for d in datasets})

    model_rows = "\n".join(model_row(m) for m in sorted(models, key=lambda x: -x.get("stats", {}).get("github_stars", 0)))
    dataset_rows = "\n".join(dataset_row(d) for d in sorted(datasets, key=lambda x: -x.get("stats", {}).get("github_stars", 0)))

    return f"""# Awesome Physical AI [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> 🤖 Physical AI (Robotics & Embodied AI) 분야의 오픈소스 모델과 데이터셋을 체계적으로 정리한 큐레이션 리스트.
> A curated list of open-source models and datasets for Physical AI (Robotics & Embodied AI).

[![Models](https://img.shields.io/badge/Models-{n_models}-blue)]({DASHBOARD_URL})
[![Datasets](https://img.shields.io/badge/Datasets-{n_datasets}-green)]({DASHBOARD_URL})
[![Organizations](https://img.shields.io/badge/Organizations-{n_orgs}-orange)]({DASHBOARD_URL})
[![Updated](https://img.shields.io/badge/Updated-{TODAY}-lightgrey)]({REPO_URL})
[![Dashboard](https://img.shields.io/badge/🌐_Dashboard-Live-brightgreen)]({DASHBOARD_URL})

> **[👉 인터랙티브 대시보드에서 필터링 및 시각화 보기 | View Interactive Dashboard]({DASHBOARD_URL})**

---

## Contents

- [Models](#-models)
- [Datasets](#-datasets)
- [How to Contribute](#-how-to-contribute)
- [Taxonomy](#-taxonomy)

---

## 🤖 Models

> 스타 수 기준 내림차순 정렬 | Sorted by GitHub stars (auto-updated weekly)

| Name | Organization | Year | Category | Hardware | Learning | ⭐ Stars | Links |
|------|-------------|------|----------|----------|----------|---------|-------|
{model_rows}

---

## 📦 Datasets

> 스타 수 기준 내림차순 정렬 | Sorted by GitHub stars (auto-updated weekly)

| Name | Organization | Year | Category | Source | Modality | Trajectories | ⭐ Stars | Links |
|------|-------------|------|----------|--------|----------|-------------|---------|-------|
{dataset_rows}

---

## 🤝 How to Contribute

새 모델 또는 데이터셋을 추가하려면 GitHub Issue를 열어주세요.
To add a new model or dataset, please open a GitHub Issue:

- **[➕ Add a Model]({REPO_URL}/issues/new?template=add-model.yml)**
- **[➕ Add a Dataset]({REPO_URL}/issues/new?template=add-dataset.yml)**

이슈가 등록되면 봇이 자동으로 PR을 생성하고, 관리자가 검토 후 머지합니다.
A bot will automatically create a PR from your issue for admin review.

---

## 📐 Taxonomy

### Models

| Field | Valid Values |
|-------|-------------|
| `categories` | `manipulation` · `locomotion` · `navigation` · `dexterous` · `whole-body` · `aerial` |
| `hardware` | `manipulator` · `humanoid` · `quadruped` · `biped` · `mobile` · `drone` · `hand` |
| `learning` | `VLA` · `IL` · `RL` · `diffusion` · `world_model` · `sim2real` |
| `framework` | `pytorch` · `jax` · `tensorflow` |
| `communication` | `ros2` · `grpc` · `lcm` · `zenoh` |

### Datasets

| Field | Valid Values |
|-------|-------------|
| `source` | `real` · `simulation` · `teleoperation` · `human_demo` · `mocap` |
| `modality` | `rgb` · `rgbd` · `depth` · `lidar` · `tactile` · `proprioception` · `audio` · `force_torque` |

---

<sub>📊 Stats auto-updated every Sunday via GitHub Actions · README auto-generated by <code>scripts/generate_site.py</code></sub>
"""


# ─────────────────────────────────────────────────────────────────────────────
# docs/data.json generation
# ─────────────────────────────────────────────────────────────────────────────

def generate_data_json(models: list[dict], datasets: list[dict]) -> dict:
    return {
        "metadata": {
            "last_updated": TODAY,
            "total_models": len(models),
            "total_datasets": len(datasets),
            "total_orgs": len({m["org"] for m in models} | {d["org"] for d in datasets}),
        },
        "models": models,
        "datasets": datasets,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    models = load_yaml(DATA_DIR / "models.yaml")
    datasets = load_yaml(DATA_DIR / "datasets.yaml")

    # Write README
    readme_content = generate_readme(models, datasets)
    README_PATH.write_text(readme_content, encoding="utf-8")
    print(f"✅ README.md written ({len(models)} models, {len(datasets)} datasets)")

    # Write docs/data.json
    DOCS_DIR.mkdir(exist_ok=True)
    data_json = generate_data_json(models, datasets)
    (DOCS_DIR / "data.json").write_text(
        json.dumps(data_json, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"✅ docs/data.json written")


if __name__ == "__main__":
    main()
