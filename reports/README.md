# Reports

This folder is reserved for **generated reports and human-readable summaries** that sit on top of the main `xc3-bias-mitigation-llm` pipeline.

Typical contents include:

- Plain-text or Markdown summaries of model performance
- Exported tables of key metrics (e.g., refusal rates, regard distributions)
- Figures or artefacts that are directly referenced in the final paper, poster, or slides

---

## 1. Expected report files

Although the repository does not ship with pre-generated reports, the codebase is designed to write the following artefact(s) into this folder.

| File                                      | Created by                              | Description |
|-------------------------------------------|-----------------------------------------|-------------|
| `context_classifier_report.txt`          | `notebooks/ml_model_bias.ipynb`        | Text-based classification report (precision, recall, F1, support) for the DistilBERT-based refusal and regard classifiers, generated using `sklearn.metrics.classification_report`. |

> **Note:** The above file is created when you run the DistilBERT contextual classifier notebook end-to-end (see `notebooks/ml_model_bias.ipynb`). If you have not yet run that notebook, this folder will only contain `README.md`.

You are encouraged to add additional report files here as your analysis and documentation evolve. Examples include:

- `bias_metrics_summary.md` – a human-readable overview of bias metrics across models and conditions.
- `toxicity_overview.txt` – summarised toxicity scores for each model, attack type, or identity group.
- Exported plots or tables that are directly referenced in your final report or presentation.

---

## 2. How to generate `context_classifier_report.txt`

The DistilBERT contextual classifier notebook is the first component that writes into this folder.

1. **Ensure data is prepared**

   From the repository root, run:

   ```bash
   python src/lbm/prepare_wp1_gui_json.py
   ```

   This script reads WP1 GUI outputs and produces:

   - `data/interim/wp1_prompts_prepared.json`

2. **Open and run the notebook**

   Start Jupyter from the repo root:

   ```bash
   jupyter notebook
   ```

   Then open:

   - `notebooks/ml_model_bias.ipynb`

   and run all cells (Kernel → Restart & Run All).

3. **Check the generated report**

   After a successful run, you should see:

   - `reports/context_classifier_report.txt`

   This file contains:

   - Validation metrics for the **refusal classifier**
   - Validation metrics for the **regard classifier**  
   (both powered by a DistilBERT backbone with metadata-aware input encoding)

   These metrics are typically used in your documentation and presentations to justify that the learned classifier is sufficiently accurate to be used for downstream bias analysis.

---

## 3. Conventions for adding new reports

To keep this directory organised and easy to navigate:

- Prefer **descriptive, snake_case filenames** such as:
  - `bias_metrics_overview.txt`
  - `toxicity_by_identity_group.md`
  - `model_comparison_summary.md`

- Where possible, document:
  - **Source script or notebook** (e.g., in a header section of the report)
  - **Date generated**
  - **Key configuration** (e.g., model version, dataset snapshot, seed)

- Do **not** commit very large binary artefacts here (e.g., high-resolution videos, huge CSVs). Instead:
  - Store them in an external location (e.g., shared drive or object storage), and
  - Add a note or link in a small text/Markdown file inside this folder.

Following these conventions ensures that anyone cloning the repository can:

- Quickly see which reports exist and what produced them
- Recreate or update reports by re-running the appropriate notebook or script
- Confidently reference these artefacts in formal write-ups and presentations
