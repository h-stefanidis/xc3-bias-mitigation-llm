# XC3 – Bias & Behaviour Analysis in Large Language Models

This repository contains the full code, data pipeline, and dashboards for the **XC3 – Bias Mitigation & Behaviour Analysis in Large Language Models** project.

The work centres on:

- **How large language models behave** under:
  - baseline prompts,
  - social‑engineering / jailbreak style prompts, and
  - identity‑injected variants.
- Measuring **refusal**, **regard/attitude**, and **toxicity** across:
  - different *models* (e.g., GPT, Gemini, Grok, Llama, Qwen, …),
  - different *conditions* (baseline vs social‑engineering vs unsuccessful),
  - and different *identity groups*.
- Providing **transparent, reproducible metrics and dashboards** that can be reused by:
  - researchers,
  - industry partners,
  - and teaching staff/markers.

The repository is organised as a **clear pipeline** from raw WP1 GUI exports → model outputs → classifier predictions → bias metrics → dashboards → reports.

---

## 🔍 1. High‑Level Architecture

The core pipeline looks like this:

```text
WP1 Excel / GUI exports
          │
          ▼
  prepare_wp1_gui_json.py
  (src/lbm/)
          │
          ▼
data/interim/wp1_prompts_prepared.json
          │
          ▼
 ml_model_bias.ipynb
 (DistilBERT refusal + regard)
          │
          ▼
data/processed/bias_metrics_with_preds.json
data/processed/bias_metrics_with_preds_summary.json
          │
          ▼
   bias_metrics.py
   (src/lbm/)
          │
          ▼
data/processed/bias_metrics.json
data/processed/bias_metrics_summary.json
          │
          ▼
 dashboards (src/dashboard/)
          │
          ▼
reports/ + poster + final paper
```

In addition, configuration files in `configs/` (e.g. `identity_lexicon.yaml`, `sentiment_words.yaml`) are used to define **identity categories** and **sentiment cues** that support the analysis.

Earlier exploratory work for Weeks 1–8 of the unit is preserved under `Weeks 1-8/` and is **separated from the main production pipeline** so markers and collaborators can see the evolution of the project without cluttering the current stack.

---

## 📁 2. Repository Structure

Top‑level layout:

```text
xc3-bias-mitigation-llm/
├── Weeks 1-8/          # Early exploratory work & prototypes (archived but available)
├── configs/            # Identity & sentiment lexicons
├── data/               # Raw, interim, and processed data
├── notebooks/          # Modelling & analysis notebooks (DistilBERT classifier)
├── reports/            # Generated reports & summaries
├── src/                # Core Python + dashboard code
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md           # (this file)
```

### 2.1. `configs/`

Small but important configuration layer:

- `identity_lexicon.yaml`  
  - Defines **identity terms and categories** (e.g. gender, race, religion, nationality, age groups, etc.).
  - Used to tag or filter prompts/responses by identity for downstream analysis.

- `sentiment_words.yaml`  
  - Lexicon of **positive / negative / neutral sentiment cues**.
  - Supports simple heuristic checks and serves as a backup/validation layer alongside the learned regard classifier.

- `configs/README.md`  
  - Documents the structure of these YAML files and how they are used.

These configs enable **consistent, explainable identity and sentiment handling** across scripts and notebooks.

### 2.2. `data/`

Standard three‑tier data structure:

```text
data/
├── raw/         # Input as obtained from WP1 GUI / manual exports
├── interim/     # Cleaned & normalised data ready for modelling
└── processed/   # Model predictions & metrics (ready for dashboards/reports)
```

Key files (once pipeline is run):

- `data/raw/wp1_prompts.xlsx`  
  Raw WP1 prompt sheet / GUI export.

- `data/interim/wp1_prompts_prepared.json`  
  Output of `src/lbm/prepare_wp1_gui_json.py`.  
  One row per (prompt × model × variant), with normalised metadata and refusal flags.

- `data/processed/bias_metrics_with_preds.json`  
  DistilBERT classifier predictions (refusal & regard) merged into the dataset.

- `data/processed/bias_metrics_with_preds_summary.json`  
  Aggregated metrics by model & condition, exported from the notebook.

- `data/processed/bias_metrics.json`  
  Full per‑record metrics, produced by `src/lbm/bias_metrics.py`.

- `data/processed/bias_metrics_summary.json`  
  Final summary metrics (model × condition × overall), used by dashboards and reports.

> **Note:** Raw data is not committed to Git if it is large or sensitive. You are expected to provide WP1 exports locally.

### 2.3. `notebooks/`

Currently contains a single key notebook:

- `ml_model_bias.ipynb`  
  - Implements a **DistilBERT‑based contextual classifier** that predicts:
    - `refusal_pred_label` (+ probability)
    - `regard_pred_label` (+ probability)
  - Uses `data/interim/wp1_prompts_prepared.json` as input.
  - Exports:
    - `data/processed/bias_metrics_with_preds.json`
    - `data/processed/bias_metrics_with_preds_summary.json`
    - `reports/context_classifier_report.txt`

The notebook is fully integrated into the pipeline:  
you run it **after data preparation** and **before bias metrics**.

### 2.4. `reports/`

Holds human‑readable outputs generated by notebooks and scripts, for example:

- `context_classifier_report.txt`  
  - Classification report (precision/recall/F1) for refusal & regard models.

Team‑members can add additional files here such as:

- descriptive `.md` or `.txt` summaries used for the final report
- export tables used in the poster or presentation

### 2.5. `src/`

Top‑level code directory:

```text
src/
├── lbm/          # Language Behaviour Metrics (core pipeline logic)
└── dashboard/    # Two dashboards: Next.js app + static HTML
```

#### 2.5.1. `src/lbm/` — Language Behaviour Metrics

Core scripts:

- `prepare_wp1_gui_json.py`  
  - Normalises WP1 Excel/GUI export to `data/interim/wp1_prompts_prepared.json`.

- `bias_metrics.py`  
  - Loads classifier outputs and/or WP1 flags.
  - Computes refusal rates, regard scores, word counts and aggregates by model and condition.
  - Writes:
    - `data/processed/bias_metrics.json`
    - `data/processed/bias_metrics_summary.json`.

- `toxicity.py`  
  - Lightweight wrapper for a Detoxify‑style toxicity model.
  - Provides a `score_toxicity(text)` style API that can be composed into notebooks or dashboards.

- `src/lbm/README.md`  
  - Explains the module and how it fits into the full pipeline.

These scripts encapsulate **all behaviour/metric computation**, keeping notebooks and dashboards clean.

#### 2.5.2. `src/dashboard/` — Dashboards

Contains **two active dashboards** that consume the processed metrics:

```text
src/dashboard/
├── README.md
├── bias-frontend/    # Modern interactive dashboard (Next.js + React)
└── frontend/         # Static HTML/CSS/JS dashboard (lightweight)
```

- `bias-frontend/`  
  - Full Next.js + React application.
  - Uses components, pages and a data folder (`public/data/`) for JSON inputs such as `human_annotations.json`.
  - Designed for deep, interactive analysis and polished client/marker demos.

- `frontend/`  
  - Static HTML (`toxicity_visualization.html`) plus CSS/JS.
  - Ideal for **quick previews**, offline demos, or simple expo screens.

---

### 2.6. `Weeks 1-8/` — Early Project Phase (Archived but Included)

This folder contains **earlier exploratory work** from the first half of the unit:

```text
Weeks 1-8/
├── configs/
├── data/
├── notebooks/
├── results/
└── src/
```

It documents:

- initial experiments and proof‑of‑concept work,
- smaller exploratory notebooks,
- and earlier configurations.

The Week 1–8 structure mirrors the main project but is intentionally **kept separate** so assessors can see the project’s evolution without confusing it with the final pipeline.

Each subfolder inside `Weeks 1-8/` has its own `README.md` where relevant, explaining what was done at that stage.

---

## 🧠 3. Core Concepts & Metrics (Short Summary)

The project focuses on a few key behavioural dimensions:

- **Refusal**  
  Whether the model *declines* to answer a prompt (e.g. “I cannot assist with that”).

- **Regard / Attitude**  
  Coarse‑grained sentiment or attitude towards an entity/identity (e.g. positive, neutral, negative).

- **Toxicity**  
  Presence of abusive, hateful, or otherwise harmful language based on toxicity scorers.

- **Identity‑conditioned behaviour**  
  How metrics above change when identity phrases are injected (e.g. “As a [identity] …”).

Each metric is computed per‑row and then aggregated:

- by **model_name** (e.g., GPT vs Gemini vs Grok),  
- by **condition** (baseline vs social engineering vs unsuccessful),  
- optionally by **identity group** (using `identity_lexicon.yaml`),  
- and then visualised via dashboards.

For full details, see:

- `src/lbm/bias_metrics.py`
- `notebooks/ml_model_bias.ipynb`
- `src/dashboard/README.md`

---

## ⚙️ 4. Getting Started (Quickstart)

### 4.1. Clone the repo

```bash
git clone https://github.com/h-stefanidis/xc3-bias-mitigation-llm.git
cd xc3-bias-mitigation-llm
```

### 4.2. Python dependencies

Create and activate a virtual environment (recommended), then:

```bash
pip install -r requirements.txt
```

This will install:

- `pandas`, `numpy`, `scikit-learn`
- `torch`, `transformers`
- plotting / utility libraries as needed by notebooks
- any additional CLI or helper tools

### 4.3. Optional: Node/Next.js for dashboard

If you want to run the interactive dashboard:

```bash
cd src/dashboard/bias-frontend
npm install          # or pnpm install
```

---

## 🚀 5. Typical Workflows

### 5.1. Run the full evaluation pipeline from scratch

1. **Place WP1 raw data**

   Save the WP1 Excel/GUI export as:

   ```text
   data/raw/wp1_prompts.xlsx
   ```

2. **Prepare the WP1 JSON**

   From the repo root:

   ```bash
   python src/lbm/prepare_wp1_gui_json.py
   ```

   This creates:

   ```text
   data/interim/wp1_prompts_prepared.json
   ```

3. **Run the DistilBERT classifier notebook**

   ```bash
   jupyter notebook
   ```

   Then open:

   ```text
   notebooks/ml_model_bias.ipynb
   ```

   Configure hyper‑parameters if needed near the top, then “Run All”.  
   This produces:

   ```text
   data/processed/bias_metrics_with_preds.json
   data/processed/bias_metrics_with_preds_summary.json
   reports/context_classifier_report.txt
   ```

4. **Compute final metrics**

   ```bash
   python src/lbm/bias_metrics.py
   ```

   Outputs:

   ```text
   data/processed/bias_metrics.json
   data/processed/bias_metrics_summary.json
   ```

5. **Explore via dashboards**

   - **Interactive Next.js app**

     ```bash
     cd src/dashboard/bias-frontend
     npm run dev
     ```

     Visit `http://localhost:3000` in your browser.

   - **Static HTML dashboard**

     Open:

     ```text
     src/dashboard/frontend/toxicity_visualization.html
     ```

     directly in a browser.

---

### 5.2. Adding a new model or dataset

To extend the analysis to a new model or dataset:

1. Integrate the model’s outputs into the WP1‑style schema or extend `prepare_wp1_gui_json.py`.
2. Ensure key fields exist:
   - `model_name`, `condition`, `output_text`, `refusal_flag` (if available).
3. Re‑run:
   - `prepare_wp1_gui_json.py`
   - `ml_model_bias.ipynb`
   - `bias_metrics.py`
4. Update dashboards if you introduce new dimensions (e.g., new conditions).

---

### 5.3. Using the lexicons (`configs/`)

If you change identity groups or sentiment cues:

1. Edit `configs/identity_lexicon.yaml` and/or `configs/sentiment_words.yaml`.
2. Re‑run the parts of the pipeline that depend on them (typically notebooks that consume these configs, or any scripts that perform lexicon‑based tagging).
3. Regenerate metrics and dashboards if necessary.

---

## 🧪 6. Testing & Reproducibility Notes

- Scripts in `src/lbm/` are **idempotent**:  
  re‑running them will overwrite the same output files using current code and data.

- To avoid GPU out‑of‑memory errors when running the notebook:
  - reduce `BATCH_SIZE`,
  - reduce `MAX_LEN`,
  - or increase gradient accumulation steps.

- Set random seeds in the notebook for reproducible Train/Validation splits.

- Large or sensitive raw data is **not committed**.  
  Paths are designed so that placing the WP1 file in `data/raw/` is sufficient.

---

## 👩‍🏫 7. How to Read This Repo (For Markers / Reviewers)

If you are assessing this project, the most important entry points are:

1. **This README** → for the big picture.
2. `src/lbm/README.md` → for the metric and data‑prep internals.
3. `notebooks/README.md` + `ml_model_bias.ipynb` → for the modelling approach.
4. `src/dashboard/README.md` → for how the dashboard works and how it consumes metrics.
5. `reports/context_classifier_report.txt` (once generated) → for classifier performance evidence.
6. `Weeks 1-8/` → to see initial exploratory work and how the project matured.

This structure is designed so that you can:

- follow the pipeline in a **top‑down** way, or  
- dive into **any layer** (data, modelling, metrics, visualisation) independently.

---

## 📄 8. License

The repository includes a `LICENSE` file at the root.  
Please refer to that file for the precise licensing terms.

---

## 📬 9. Contact

Maintainer: **Harrison Stefanidis**  
Unit: **COS80029 – Technology Application Project**  
Institution: Swinburne University of Technology

For questions, collaboration, or extension of this work, please reach out or open an issue in the repository.
