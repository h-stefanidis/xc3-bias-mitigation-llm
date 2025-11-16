# Weeks 1–8: Prototype LLM Bias Benchmarking (Archived)

> **Status:** Archived / not part of the final delivered system.  
> This folder contains the Week 1–8 prototype developed during early exploration of dataset preparation and LLM bias benchmarking.  
> It is included for transparency, historical reference, and reproducibility.

The final pipeline (delivered to the client) is located in the project root.  
This prototype shows the original approach to dataset processing, LLM evaluation, and metric generation.

---

# 1. Overview

The Week 1–8 prototype implements a complete workflow for bias benchmarking:

- Download public bias datasets (CrowS-Pairs, StereoSet, HolisticBias)  
- Clean and **10% sample** each dataset  
- Generate a unified combined JSONL dataset  
- Produce LLM responses using early notebooks  
- Evaluate responses with a judge model  
- Generate baseline statistics + Markdown summary reports  

All outputs are reproducible using scripts in `src/`.

---

# 2. Folder Structure

```
Weeks 1-8/
├── configs/      # configuration files (YAML + Python)
├── data/         # raw, processed, interim, outputs (mostly git-ignored)
├── notebooks/    # prototype notebooks
├── results/      # generated stats + exports (git-ignored)
└── src/          # scripts for data prep + metrics
```

---

# 3. `configs/`

### `week6_pilot.yaml`
Defines:

- Raw dataset paths  
- Processed dataset outputs  
- Sampling ratio (10%)  
- Location to store attack prompt templates  

### `config.py`
Used by notebooks. Provides:

- `llm_test_config` – models queried for responses  
- `llm_judge_config` – judge model used for evaluation  
- `directory_data` – directories for processed data, responses, and evaluation outputs  

API keys are **not** stored here; they must be provided via environment variables.

### `models.json`
Model alias → model name mapping for template pipelines.

### `api_keys.json` (example)
Contains placeholder entries only.  
Real keys must be stored in untracked local files or environment variables.

---

# 4. `data/`

Most of this folder is **generated** and **git-ignored**.

```
data/
├── raw/          # downloaded source datasets
├── processed/    # 10% slices + combined datasets
├── interim/      # notebook scratch space
├── output/       # model responses + evaluation results
└── registry.json # auto-generated dataset manifest
```

### Raw datasets
Created by:

```bash
python src/scripts/download_datasets.py
```

Includes all CrowS-Pairs, StereoSet, and HolisticBias components.

### Processed datasets
Created by:

```bash
python src/scripts/clean_and_slice.py
python src/scripts/dataset_generator.py
```

Generates:

- `*_10pct.jsonl` files  
- `combined_datasets.jsonl`  
- `attack_prompts.json` (kept under version control)

### Interim (`data/interim/`)
Temporary notebook outputs (safe to delete).

### Output (`data/output/`)
LLM responses + evaluation files, organised by model and condition.

### Registry (`data/registry.json`)
Auto-generated mapping of raw and processed dataset files.

---

# 5. `notebooks/`

All notebooks must be run from:

```
Weeks 1-8/notebooks/
```

### `crows-pair_logP.ipynb`
Log-probability analysis for CrowS-Pairs.  
Reads raw CSV and writes interim files.

### `crosws-pair_bias_calculation_SPR.ipynb`
Computes Stereotype Preference Rate (SPR).  
Outputs final CSVs to:

```
../results/exports/
```

### `llm_response_pipeline.ipynb`
Generates LLM responses using models in `llm_test_config`.

### `evaluation_pipeline.ipynb`
Evaluates responses with judge model in `llm_judge_config`.  
Outputs to:

```
../data/output/evaluation/<model>/baseline/
```

### `Template_master_pipeline_V1.0.ipynb`
Original combined pipeline draft. Kept only for reference.

---

# 6. `src/`

Scripts must be run from inside:

```
Weeks 1-8/
```

### Download raw datasets
```bash
python src/scripts/download_datasets.py
```

### Clean and 10% sample
```bash
python src/scripts/clean_and_slice.py
```

### Generate combined dataset
```bash
python src/scripts/dataset_generator.py
```

### Compute baseline statistics
```bash
python src/scripts/stats_baseline_only.py --csv results/runs/<baseline_file>.csv
```

### Generate Markdown / HTML summary
```bash
python src/scripts/make_summary_report.py --prefix results/<file_base>
```

---

# 7. `results/`

This directory stores **generated** statistics and exports.  
It is fully git-ignored.

```
results/
├── runs/        # per-run stats (sweeps, binaries, distributions, summary)
└── exports/     # final tables for reporting / dashboards
```

Examples:

- `*_sweeps.csv`  
- `*_binaries.csv`  
- `*_distributions.csv`  
- `*_summary.md`  
- `crows_pairs_bias_report.csv`  
- `crows_pairs_model_choices.csv`

---

# 8. Reproducing the Pipeline

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Enter folder
```bash
cd "Weeks 1-8"
```

### 3. Download datasets
```bash
python src/scripts/download_datasets.py
```

### 4. Clean & sample datasets
```bash
python src/scripts/clean_and_slice.py
```

### 5. Generate combined dataset
```bash
python src/scripts/dataset_generator.py
```

### 6. Generate model responses
Open:

```
notebooks/llm_response_pipeline.ipynb
```

### 7. Evaluate responses
Open:

```
notebooks/evaluation_pipeline.ipynb
```

### 8. Generate baseline statistics (optional)
```bash
python src/scripts/stats_baseline_only.py --csv results/runs/<file>.csv
```

### 9. Create summary report (optional)
```bash
python src/scripts/make_summary_report.py --prefix results/<file_base>
```

---

# 9. Notes & Caveats

- This folder contains **early experimental work**, not the final implemented system.  
- All processed data and results are **reproducible** and intentionally **git-ignored**.  
- API keys must **never** be committed — use environment variables.  
- Some datasets (e.g., CrowS-Pairs, HolisticBias) contain sensitive identity terms.  
- LLM outputs vary over time; results may not be identical across different runs.

For any production or research use, refer to the **main project pipeline** located at the root of the repository.
