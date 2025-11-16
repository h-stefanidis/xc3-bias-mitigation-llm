# Configs – Lexicons for Identity & Sentiment Analysis

This folder contains YAML configuration files used by the **bias metrics pipeline** located in:

```
src/lbm/bias_metrics.py
```

These lexicons enable the system to detect:

- Mentions of demographic or protected groups  
- Sentiment (regard) associated with those groups  

The files are fully editable and human-readable, allowing easy adaptation and transparent evaluation.

---

## 1. `identity_lexicon.yaml`

A structured list of identity categories (e.g., gender, race, religion, nationality) and their surface forms.

Example:

```yaml
gender:
  - woman
  - man
  - nonbinary

race:
  - asian
  - black
  - white
```

### Purpose in the pipeline

- Enables identity tagging in `bias_metrics.py`  
- Supports group-wise aggregation of sentiment  
- Forms the basis for identity-aware evaluation metrics  

### Editing guidelines

- Keep terms lowercase  
- Prefer explicit identity markers (avoid ambiguous ones)  
- Add synonyms/variants as needed  
- Avoid slurs unless explicitly required for toxicity benchmarking  

---

## 2. `sentiment_words.yaml`

Defines three sentiment buckets:

- **positive**
- **negative**
- **neutral**

Example:

```yaml
positive:
  - kind
  - respectful
negative:
  - dangerous
  - inferior
neutral:
  - group
  - individual
```

### Purpose in the pipeline

- Measures sentiment/regard toward identity groups  
- Computes sentiment ratios across demographic categories  
- Supports group-conditioned fairness metrics  

### Editing guidelines

- Keep all entries lowercase  
- Avoid context-dependent words when possible  
- Expand categories gradually and re-test metrics  

---

## How These Lexicons Are Used

Both YAML files are consumed by:

```
src/lbm/bias_metrics.py
```

The script:

1. Loads the lexicons  
2. Detects identity mentions  
3. Assigns sentiment/regard labels  
4. Produces:
   - `bias_metrics.json`
   - `bias_metrics_summary.json`
   - summary variants

You can specify custom paths:

```bash
python src/lbm/bias_metrics.py   --lexicon configs/identity_lexicon.yaml   --sentiment configs/sentiment_words.yaml   --in <input_jsonl>   --out <output_json>   --summary <summary_json>
```

---

## Modifying Lexicons Safely

When updating lexicons:

1. Make incremental changes  
2. Validate YAML structure  
3. Re-run `bias_metrics.py` to confirm correct behaviour  
4. Commit changes with a clear message, e.g.:

```
Update nationality lexicon with additional variants
```

---

## Summary

These lexicons control how the system:

- Identifies demographic references  
- Measures regard and sentiment  
- Generates interpretable bias metrics  

They are intentionally transparent, editable, and central to reproducible evaluation.
