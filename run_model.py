import json
import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM

# ==================================================
# Developer Configuration (CHANGE MODEL HERE ONLY)
# ==================================================
MODEL_NAME = "google/flan-t5-small"  # change freely: flan-t5-base, mistral-instruct, etc.
REFERENCE_DATA_FILE = "brand-data.json"
# ==================================================


@st.cache_resource
def load_model_and_tokenizer():
    """
    Loads any HuggingFace model safely.
    Automatically detects seq2seq vs causal.
    Cached to prevent Streamlit reloading crashes.
    """
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    try:
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        model_type = "seq2seq"
    except Exception:
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        model_type = "causal"

    # Safety fixes
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model.eval()
    return tokenizer, model, model_type


tokenizer, model, model_type = load_model_and_tokenizer()

with open(REFERENCE_DATA_FILE, "r") as f:
    reference_data = json.load(f)


def validate_metadata(user_input: dict) -> dict:
    """
    AI-driven schema & logic validation.
    Does NOT compare equality.
    Uses reference data as contextual examples only.
    """

    prompt = f"""
You are an AI validator for Proofelle, a luxury product digital authenticity platform.

Reference examples of valid luxury product metadata:
{json.dumps(reference_data, indent=2)}

User-submitted product metadata:
{json.dumps(user_input, indent=2)}

Validation rules:
1. Check completeness of fields.
2. Detect logical inconsistencies (brand, price, retailer, date).
3. Standardize values where possible.
4. Assign a validation_score between 0 and 1.
5. Return STRICT JSON ONLY with:
   - validation_status (PASS / REVIEW / FAIL)
   - validation_score
   - warnings (array)
   - suggested_fixes (object)
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        if model_type == "seq2seq":
            outputs = model.generate(
                **inputs,
                max_new_tokens=350
            )
        else:
            outputs = model.generate(
                **inputs,
                max_new_tokens=350,
                do_sample=True,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )

    raw_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Robust JSON extraction
    try:
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        if start == -1 or end == -1:
            raise ValueError("No JSON found")

        json_block = raw_text[start:end]
        return json.loads(json_block)

    except Exception as e:
        return {
            "validation_status": "REVIEW",
            "validation_score": 0.45,
            "warnings": [
                "AI output could not be parsed as strict JSON",
                str(e)
            ],
            "suggested_fixes": {}
        }
