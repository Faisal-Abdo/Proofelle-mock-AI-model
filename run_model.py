import json
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ================= CONFIG =================
MODEL_NAME = "google/flan-t5-small"  # change freely
DB_FILE = "brand-data.json"
# ========================================

# Load model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Load canonical brand data
with open(DB_FILE, "r") as f:
    BRAND_DB = json.load(f)


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group())


def validate_metadata(input_data):
    warnings = []
    suggested_fixes = {}
    score = 1.0

    brand = input_data.get("brand")
    model_name = input_data.get("model_name")

    # ---------- Deterministic Validation ----------
    if not brand or brand not in BRAND_DB:
        return {
            "validation_status": "FAIL",
            "validation_score": 0.0,
            "warnings": ["Unknown or missing brand"],
            "suggested_fixes": {}
        }

    if not model_name or model_name not in BRAND_DB[brand]:
        return {
            "validation_status": "FAIL",
            "validation_score": 0.0,
            "warnings": ["Unknown or missing model for given brand"],
            "suggested_fixes": {}
        }

    # Auto-fill canonical fields
    canonical = BRAND_DB[brand][model_name]
    suggested_fixes.update(canonical)

    # ---------- AI Reasoning Layer ----------
    prompt = f"""
You MUST return ONLY valid JSON.
No explanations. No markdown.

Schema:
{{
  "warnings": [string],
  "confidence_adjustment": number between -1 and 0
}}

Input:
{json.dumps(input_data, indent=2)}

Canonical truth:
{json.dumps(canonical, indent=2)}

Return JSON now.
"""

    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = model.generate(**inputs, max_new_tokens=200)
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
        ai_json = extract_json(decoded)

        warnings.extend(ai_json.get("warnings", []))
        score += ai_json.get("confidence_adjustment", 0)

    except Exception:
        warnings.append("AI output could not be parsed as strict JSON")
        score -= 0.3

    score = max(0.0, min(1.0, round(score, 2)))

    status = "PASS" if score >= 0.85 else "REVIEW" if score >= 0.4 else "FAIL"

    return {
        "validation_status": status,
        "validation_score": score,
        "warnings": warnings,
        "suggested_fixes": suggested_fixes
    }
