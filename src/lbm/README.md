# LBM — Language Behaviour Metrics Module

The **LBM (Language Behaviour Metrics)** module contains all core logic for:
- preparing WP1 prompt–response data
- computing refusal/attitude/behaviour metrics
- generating model × condition summaries for research analysis
- optional toxicity scoring

These scripts form the backbone of the entire `xc3-bias-mitigation-llm` pipeline.

---

## 📁 Files

```
src/lbm/
├── prepare_wp1_gui_json.py
├── bias_metrics.py
├── toxicity.py
└── README.md
```

---

# 1. `prepare_wp1_gui_json.py` — WP1 Data Normalisation

This script converts the raw WP1 Excel workbook (or GUI-exported CSV/XLSX) into a **clean, analysis-ready JSON**.

### **Purpose**
- Flatten the WP1 sheet into **one row per (prompt × model × variant)**
- Auto-detect model/variant columns
- Normalise conditions (`baseline`, `social_eng`, `unsuccessful`)
- Derive `refusal_flag` from WP1 “Test Result”
- Write a canonical intermediate file used everywhere else

### **Input**
```
data/raw/wp1_prompts.xlsx
```

### **Output**
```
data/interim/wp1_prompts_prepared.json
```

### **CLI usage**
```bash
python src/lbm/prepare_wp1_gui_json.py
```

---

# 2. `bias_metrics.py` — Bias, Refusal & Behaviour Metrics

This is the **core metric engine** for the entire project.

### **Purpose**
- Load classifier-enhanced WP1 data (with refusal/regard predictions)
- Compute per-row metrics
- Aggregate to:
  - per-model summaries
  - per-condition summaries
  - overall totals
- Handle missing or partially annotated datasets safely

---

## **Inputs**

### **Option A — Classifier outputs**
```
data/processed/bias_metrics_with_preds.json
```

### **Option B — Manual WP1 fields only**
```
data/interim/wp1_prompts_prepared.json
```

---

## **Outputs**

### **1. Detailed per-record metrics**
```
data/processed/bias_metrics.json
```

### **2. Aggregated metrics**
```
data/processed/bias_metrics_summary.json
```

---

## **Execution**
```bash
python src/lbm/bias_metrics.py
```

---

# 3. `toxicity.py` — Toxicity Scoring (Optional)

A standalone helper wrapping a Detoxify-like toxicity scoring model.

### Example
```python
from src.lbm.toxicity import score_toxicity
score_toxicity("I hate you")
```

---

# 4. Pipeline Overview

```
WP1 Excel/GUI ──► prepare_wp1_gui_json.py
                 │
                 ▼
data/interim/wp1_prompts_prepared.json
                 │
                 ▼
     ml_model_bias.ipynb (DistilBERT refusal + regard)
                 │
                 ▼
data/processed/bias_metrics_with_preds.json
                 │
                 ▼
           bias_metrics.py
                 │
                 ▼
 data/processed/bias_metrics.json
 data/processed/bias_metrics_summary.json
                 │
                 ▼
               reports/
```

---

# 5. Developer Notes

- All paths are relative to the repo root.
- JSON used for interoperability.
- Error-handling protects pipeline from missing fields.
- Script names follow semantic conventions.

---

# 6. Future Extensions

Potential additions:
- `identity_variant_generator.py`
- `bootstrap_uncertainty.py`
- `fairness_metrics.py`