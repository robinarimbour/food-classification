
# --------------------------------
# Constants
# --------------------------------

NUTRIENTS = [
    "protein","total_fat","carbohydrate","energy","fiber",
    "potassium","sodium","cholesterol","trans_fat",
    "saturated_fat","sugars"
]

NUTRIENT_UNITS = {
    "protein": "g",
    "total_fat": "g",
    "carbohydrate": "g",
    "energy": "kcal",
    "fiber": "g",
    "potassium": "mg",
    "sodium": "mg",
    "cholesterol": "mg",
    "trans_fat": "g",
    "saturated_fat": "g",
    "sugars": "g"
}

MODEL_FEATURES = {
    "protein": "protein",
    "total_fat": "total_lipid_fat",
    "carbohydrate": "carbohydrate_by_difference",
    "energy": "energy",
    "fiber": "fiber_total_dietary",
    "potassium": "potassium_k",
    "sodium": "sodium_na",
    "cholesterol": "cholesterol",
    "trans_fat": "fatty_acids_total_trans",
    "saturated_fat": "fatty_acids_total_saturated",
    "sugars": "sugars_total"
}

INPUT_OPTIONS = [
    "🍔 Sample Food",
    "📷 Upload Label (OCR)",
    "✏️ Manual Entry"
]

GRADE_INFO = {
    "A": "Very Healthy",
    "B": "Healthy",
    "C": "Moderate",
    "D": "Unhealthy",
    "E": "Very Unhealthy"
}

GRADE_EMOJI = {
    "A": "🟢",
    "B": "🟢",
    "C": "🟡",
    "D": "🟠",
    "E": "🔴"
}

# --------------------------------
# Helper Functions
# --------------------------------

def convert_to_100g(value, serving_size):
    return (value / serving_size) * 100
