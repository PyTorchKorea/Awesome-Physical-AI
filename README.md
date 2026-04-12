# Awesome Physical AI [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> 🤖 Physical AI (Robotics & Embodied AI) 분야의 오픈소스 모델과 데이터셋을 체계적으로 정리한 큐레이션 리스트.
> A curated list of open-source models and datasets for Physical AI (Robotics & Embodied AI).

[![Models](https://img.shields.io/badge/Models-15-blue)](https://pytorchkr.github.io/Awesome-Physical-AI)
[![Datasets](https://img.shields.io/badge/Datasets-10-green)](https://pytorchkr.github.io/Awesome-Physical-AI)
[![Organizations](https://img.shields.io/badge/Organizations-21-orange)](https://pytorchkr.github.io/Awesome-Physical-AI)
[![Updated](https://img.shields.io/badge/Updated-2026-04-12-lightgrey)](https://github.com/PyTorchKR/Awesome-Physical-AI)
[![Dashboard](https://img.shields.io/badge/🌐_Dashboard-Live-brightgreen)](https://pytorchkr.github.io/Awesome-Physical-AI)

> **[👉 인터랙티브 대시보드에서 필터링 및 시각화 보기 | View Interactive Dashboard](https://pytorchkr.github.io/Awesome-Physical-AI)**

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
| [Genesis](https://github.com/Genesis-Embodied-AI/Genesis) | Genesis Authors (MIT/CMU/Stanford) | 2024 | manipulation, locomotion, navigation | manipulator, humanoid, quadruped, mobile, drone | RL, sim2real | 22,000 | [📄](https://arxiv.org/abs/2501.00599)  |
| [LeRobot](https://github.com/huggingface/lerobot) | Hugging Face | 2024 | manipulation | manipulator | IL, diffusion, VLA | 9,800 | [📄](https://arxiv.org/abs/2408.01730) [🤗](https://huggingface.co/lerobot) |
| [openpi (π0 Open Implementation)](https://github.com/Physical-Intelligence/openpi) | Physical Intelligence | 2025 | manipulation, dexterous | manipulator, humanoid | VLA, diffusion | 5,800 | [📄](https://arxiv.org/abs/2410.24164) [🤗](https://huggingface.co/physical-intelligence/pi0) |
| [π0 (pi-zero)](https://github.com/Physical-Intelligence/openpi) | Physical Intelligence | 2024 | manipulation, whole-body | manipulator, humanoid | VLA, diffusion | 4,200 | [📄](https://arxiv.org/abs/2410.24164) [🤗](https://huggingface.co/physical-intelligence) |
| [Isaac Lab](https://github.com/isaac-sim/IsaacLab) | NVIDIA | 2023 | manipulation, locomotion, navigation | manipulator, humanoid, quadruped, mobile | RL, IL, sim2real | 3,400 | [📄](https://arxiv.org/abs/2301.04195)  |
| [ACT (Action Chunking with Transformers)](https://github.com/tonyzhaozh/act) | Stanford | 2023 | manipulation, dexterous | manipulator | IL | 3,100 | [📄](https://arxiv.org/abs/2304.13705)  |
| [GR00T N1](https://github.com/NVIDIA/Isaac-GR00T) | NVIDIA | 2025 | manipulation, whole-body | humanoid | VLA, IL | 3,100 | [📄](https://arxiv.org/abs/2503.14734) [🤗](https://huggingface.co/nvidia/GR00T-N1-2B) |
| [Diffusion Policy](https://github.com/real-stanford/diffusion_policy) | Columbia University | 2023 | manipulation | manipulator | IL, diffusion | 2,800 | [📄](https://arxiv.org/abs/2303.04137)  |
| [Mobile ALOHA](https://github.com/MarkFzp/mobile-aloha) | Stanford | 2024 | manipulation, navigation, whole-body | mobile, manipulator | IL | 2,200 | [📄](https://arxiv.org/abs/2401.02117)  |
| [OpenVLA](https://github.com/openvla/openvla) | Stanford / UC Berkeley | 2024 | manipulation | manipulator | VLA | 2,100 | [📄](https://arxiv.org/abs/2406.09246) [🤗](https://huggingface.co/openvla/openvla-7b) |
| [Octo](https://github.com/octo-models/octo) | UC Berkeley / Stanford / CMU / others | 2023 | manipulation | manipulator, mobile | IL, VLA | 1,700 | [📄](https://arxiv.org/abs/2405.12213) [🤗](https://huggingface.co/rail-berkeley/octo-base) |
| [HumanPlus](https://github.com/MarkFzp/humanplus) | Stanford | 2024 | manipulation, whole-body | humanoid | IL | 1,600 | [📄](https://arxiv.org/abs/2406.10454)  |
| [RoboFlamingo](https://github.com/RoboFlamingo/RoboFlamingo) | ByteDance | 2023 | manipulation | manipulator | VLA | 980 | [📄](https://arxiv.org/abs/2311.01378)  |
| [GR-1](https://github.com/bytedance/GR-1) | BAAI / Beijing Academy of AI | 2024 | manipulation | manipulator | VLA, IL | 720 | [📄](https://arxiv.org/abs/2312.13139)  |
| [CrossFormer](https://github.com/rail-berkeley/crossformer) | UC Berkeley / others | 2024 | manipulation | manipulator, mobile | IL, VLA | 520 | [📄](https://arxiv.org/abs/2408.11812) [🤗](https://huggingface.co/rail-berkeley/crossformer) |

---

## 📦 Datasets

> 스타 수 기준 내림차순 정렬 | Sorted by GitHub stars (auto-updated weekly)

| Name | Organization | Year | Category | Source | Modality | Trajectories | ⭐ Stars | Links |
|------|-------------|------|----------|--------|----------|-------------|---------|-------|
| [Meta-World](https://github.com/Farama-Foundation/Metaworld) | Stanford / Berkeley | 2019 | manipulation | simulation | proprioception | — | 1,400 | [📄](https://arxiv.org/abs/1910.10897)  |
| [ManiSkill2](https://github.com/haosulab/ManiSkill) | UC San Diego / Shanghai AI Lab | 2023 | manipulation, dexterous | simulation | rgb, rgbd, proprioception | 36,000 | 1,200 | [📄](https://arxiv.org/abs/2302.04659) [🤗](https://huggingface.co/datasets/haosulab/ManiSkill) |
| [Open X-Embodiment (OXE)](https://github.com/google-deepmind/open_x_embodiment) | Google DeepMind / RT-X Team | 2023 | manipulation | real, teleoperation | rgb, rgbd, proprioception | 1,000,000 | 1,100 | [📄](https://arxiv.org/abs/2310.08864) [🤗](https://huggingface.co/datasets/jxu124/OpenX-Embodiment) |
| [DROID](https://github.com/droid-dataset/droid) | UC Berkeley / Stanford / others | 2024 | manipulation | real, teleoperation | rgb, rgbd, proprioception | 76,000 | 680 | [📄](https://arxiv.org/abs/2403.12945) [🤗](https://huggingface.co/datasets/droid-dataset/droid) |
| [HumanoidBench](https://github.com/carlosferrazza/humanoid-bench) | CMU / UC San Diego / MIT | 2024 | locomotion, manipulation, whole-body | simulation | rgb, proprioception | — | 560 | [📄](https://arxiv.org/abs/2403.10506)  |
| [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO) | UMass Amherst / Bosch | 2023 | manipulation | simulation | rgb, proprioception | 130,000 | 480 | [📄](https://arxiv.org/abs/2306.03310) [🤗](https://huggingface.co/datasets/openvla/modified_libero_spatial) |
| [RoboAgent Dataset](https://github.com/rail-berkeley/roboagent) | CMU | 2023 | manipulation | real, teleoperation | rgb, proprioception | 7,500 | 390 | [📄](https://arxiv.org/abs/2309.01918)  |
| [Language-Table](https://github.com/google-research/language-table) | Google | 2023 | manipulation | real, simulation, teleoperation | rgb, proprioception | 600,000 | 340 | [📄](https://arxiv.org/abs/2210.01911) [🤗](https://huggingface.co/datasets/google/language_table) |
| [BridgeData V2](https://github.com/rail-berkeley/bridge_data_v2) | UC Berkeley | 2023 | manipulation | real, teleoperation | rgb, proprioception | 60,096 | 320 | [📄](https://arxiv.org/abs/2308.12952) [🤗](https://huggingface.co/datasets/rail-berkeley/bridge_orig) |
| [RH20T](https://github.com/rh20t/rh20t_api) | Shanghai AI Lab | 2023 | manipulation, dexterous | real, teleoperation | rgb, rgbd, tactile, proprioception, audio | 110,000 | 285 | [📄](https://arxiv.org/abs/2307.00595)  |

---

## 🤝 How to Contribute

새 모델 또는 데이터셋을 추가하려면 GitHub Issue를 열어주세요.
To add a new model or dataset, please open a GitHub Issue:

- **[➕ Add a Model](https://github.com/PyTorchKR/Awesome-Physical-AI/issues/new?template=add-model.yml)**
- **[➕ Add a Dataset](https://github.com/PyTorchKR/Awesome-Physical-AI/issues/new?template=add-dataset.yml)**

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
