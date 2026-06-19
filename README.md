# Python AML & Fraud Detection Toolkit — Preview

**Bangladesh MFS Transaction Monitoring | BFIU-Calibrated Rules | LightGBM ML**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LightGBM](https://img.shields.io/badge/LightGBM-ML%20Layer-009900?style=flat-square)](https://lightgbm.readthedocs.io)
[![Jupyter](https://img.shields.io/badge/Jupyter-3%20Notebooks-F37626?style=flat-square&logo=jupyter&logoColor=white)](notebooks/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

> ⚡ **This is the free preview.** Contains data generation + EDA only.
> **[→ Get the full toolkit on Gumroad ($39)](https://monsurhabib01.gumroad.com/l/cbnfic)** — includes rule engine, LightGBM ML layer, threshold backtesting, regulatory profile builder, SAR export, and full documentation.

---

## What's in This Preview

| File | What It Does |
|------|-------------|
| `generate_data.py` | Synthetic bKash/Nagad transaction generator (10,000+ txns, BDT amounts, BD phone format, 8 divisions) |
| `notebooks/01_data_generation.ipynb` | Data generation walkthrough + full EDA + temporal analysis |

Run it:
```bash
git clone https://github.com/monsurhabib01/aml-detection-preview.git
cd aml-detection-preview
pip install -r requirements.txt
python generate_data.py
# or open notebooks/01_data_generation.ipynb in Jupyter
```

---

## What's in the Full Toolkit

```
Synthetic bKash/Nagad Data (10,000+ transactions)
              ↓
  Rule Engine — 6 BFIU-Calibrated Rules         ← FULL TOOLKIT ONLY
  (STRUCTURING · VELOCITY · DORMANT_SPIKE · LATE_NIGHT · ROUND_AMOUNT · HIGH_VALUE)
              ↓
  Composite Risk Score (0–100) → LOW / MEDIUM / HIGH
              ↓
  Threshold Backtesting — tune precision vs recall   ← FULL TOOLKIT ONLY
              ↓
  LightGBM ML Layer — reduces false positives        ← FULL TOOLKIT ONLY
              ↓
  SAR Candidates Export (.csv)                       ← FULL TOOLKIT ONLY
```

**Full toolkit includes:**
- `detect_anomalies.py` — Rule engine with composite risk scoring
- `threshold_backtest.py` — Backtest rule thresholds (rare in AML tutorials)
- `reg_profile.py` — Regulatory customer profile builder (EDD triggers)
- `run_pipeline.py` — End-to-end pipeline in one command
- `visualize.py` — 6-chart compliance monitoring dashboard
- `notebooks/02` + `03` — Rule engine + LightGBM notebooks
- `RULE_CALIBRATION.md` — Every rule weight cited against BFIU Circular No. 5 (2019)
- `configs/` — Configurable rule weights (no hardcoding)
- CI/CD pipeline + automated test suite

## 🔴 Why Your Kaggle Credit Card Dataset Won't Get You Hired

Every hiring manager at a fintech has seen that dataset. It's overused, context-free, and proves nothing about financial crime domain knowledge.

This toolkit is built on **realistic Bangladesh MFS (bKash/Nagad) transaction patterns**, calibrated against actual **BFIU reporting rules**, with the same 3-layer detection hierarchy used by real AML compliance teams.

**[→ Get the full toolkit — $39 one-time, all future updates included](https://monsurhabib01.gumroad.com/l/cbnfic)**

---

## Tech Stack

Python 3.9+ · Pandas · NumPy · Scikit-learn · LightGBM · Matplotlib · Seaborn · Jupyter

---

## Contact

**Monsur Habib** — AML Data Analyst · Dhaka, Bangladesh

🌐 [aitipseveryday.com](https://aitipseveryday.com) · 💼 [Fiverr](https://www.fiverr.com/mdmonsurhabib) · 📧 habibmonsur01@gmail.com

---

MIT License — preview files free for educational use.
