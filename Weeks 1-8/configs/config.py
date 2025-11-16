"""
config.py

Configuration for the Week 1–8 prototype notebooks.

- llm_test_config: models under test (e.g., DeepSeek) via the HF router.
- llm_judge_config: LLM used as a “judge” in the evaluation pipeline.
- directory_data: where processed datasets, responses, and evaluations are stored.

NOTE:
    - API keys are loaded from environment variables for safety.
    - This file is only used by the Week 1–8 notebooks.
"""

import os

# --------------------------------------------------------------------
# 1) Models under test (used in llm_response_pipeline.ipynb)
# --------------------------------------------------------------------

llm_test_config = {
    # Use an environment variable for security; leave empty string as default.
    "api_key": os.environ.get("HF_API_KEY", ""),
    "models": [
        {
            "alias": "deepseek",
            "model_name": "deepseek-ai/DeepSeek-V3.1:novita",
        },
        # You can add more models here if needed, e.g.:
        # {
        #     "alias": "gemma",
        #     "model_name": "google/gemma-2-9b-it:nebius",
        # },
    ],
}

# --------------------------------------------------------------------
# 2) Judge model (used in evaluation_pipeline.ipynb)
# --------------------------------------------------------------------

llm_judge_config = {
    # Also read from the same HF router key by default
    "api_key": os.environ.get("HF_API_KEY", ""),
    # Replace this with whatever judge model you actually used:
    "model_name": "meta-llama/Meta-Llama-3.1-8B-Instruct",
}

# --------------------------------------------------------------------
# 3) Directory layout for datasets and outputs
# --------------------------------------------------------------------
# IMPORTANT:
# These paths are interpreted relative to the PROJECT ROOT from the
# perspective of the notebooks, which live in `Weeks 1-8/notebooks/`.
#
# Example from llm_response_pipeline.ipynb:
#     Path(directory_data["processed_dataset_dir"]) / "combined_datasets.jsonl"
#
# When run with cwd = `Weeks 1-8/notebooks`, "../data/processed" resolves to
# `Weeks 1-8/data/processed`, which is what we want.
# --------------------------------------------------------------------

directory_data = {
    # Where cleaned/sliced datasets live (JSONL).
    "processed_dataset_dir": "../data/processed",

    # Per-model output locations
    "deepseek": {
        "baseline": {
            "response_dir": "../data/output/response/deepseek/baseline",
            "eval_dir": "../data/output/evaluation/deepseek/baseline",
        },
        "mitigation": {
            "response_dir": "../data/output/response/deepseek/mitigation",
            "eval_dir": "../data/output/evaluation/deepseek/mitigation",
        },
    },

    # Example for an additional model (commented for now)
    # "gemma": {
    #     "baseline": {
    #         "response_dir": "../data/output/response/gemma/baseline",
    #         "eval_dir": "../data/output/evaluation/gemma/baseline",
    #     },
    #     "mitigation": {
    #         "response_dir": "../data/output/response/gemma/mitigation",
    #         "eval_dir": "../data/output/evaluation/gemma/mitigation",
    #     },
    # },
}
