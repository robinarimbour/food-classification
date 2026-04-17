
import numpy as np
import pandas as pd
import joblib
import streamlit as st
from PIL import Image
import easyocr
import cv2
import re
from utils import NUTRIENTS, NUTRIENT_UNITS, MODEL_FEATURES, INPUT_OPTIONS, GRADE_INFO, GRADE_EMOJI, convert_to_100g


# --------------------------------
# Session State
# --------------------------------

def init_session_state():
    for nutrient in NUTRIENTS:
        if nutrient not in st.session_state:
            st.session_state[nutrient] = 0.0

    if "serving_size" not in st.session_state:
        st.session_state.serving_size = 100.0

# --------------------------------
# Load Resources
# --------------------------------

@st.cache_resource
def load_model():
    return joblib.load("model_v2/pipeline_rf.pkl")


@st.cache_data
def load_data():
    food_category = pd.read_csv("datasets/food_category.csv")
    sample_foods = pd.read_csv("assets/sample_foods.csv")
    return food_category, sample_foods


@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en'], gpu=False)


@st.cache_resource
def load_nutriscore_images():
    return {
        "A": Image.open("assets/nutriscore_a.jpg"),
        "B": Image.open("assets/nutriscore_b.jpg"),
        "C": Image.open("assets/nutriscore_c.jpg"),
        "D": Image.open("assets/nutriscore_d.jpg"),
        "E": Image.open("assets/nutriscore_e.jpg"),
    }

# --------------------------------
# Sample Food Autofill
# --------------------------------

def autofill_sample_food(sample_foods):

    selected_food = st.selectbox(
        "Select Sample Food (Auto-fill nutrients)",
        ["None"] + list(sample_foods["food"])
    )

    if selected_food != "None":

        row = sample_foods[sample_foods["food"] == selected_food].iloc[0]

        for nutrient in NUTRIENTS:
            st.session_state[nutrient] = float(row[nutrient])

# -------------------------
# OCR Helper functions
# -------------------------

def preprocess_image(image):
    img = np.array(image)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    return gray


def extract_value(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return float(match.groups()[-1])
    return 0.0


def extract_nutrients_from_image(reader, image):

    processed_img = preprocess_image(image)
    results = reader.readtext(processed_img)

    text = " ".join([res[1] for res in results])

    serving = extract_value(r"Serving Size\s+(\d+\.?\d*)", text)
    return {
        "serving_size": serving if serving > 0 else 100.0,
        "protein": extract_value(r"Protein\s+(\d+\.?\d*)", text),
        "total_fat": extract_value(r"Total Fat\s+(\d+\.?\d*)", text),
        "carbohydrate": extract_value(r"(?:Carbohydrate|Total Carbohydrate)\s+(\d+\.?\d*)", text),
        "energy": extract_value(r"(?:Calories|Energy)\s+(\d+\.?\d*)", text),
        "fiber": extract_value(r"Fiber\s+(\d+\.?\d*)", text),
        "potassium": extract_value(r"Potassium\s+(\d+\.?\d*)", text),
        "sodium": extract_value(r"(?:Salt|Sodium)\s+(\d+\.?\d*)", text),
        "cholesterol": extract_value(r"Cholesterol\s+(\d+\.?\d*)", text),
        "trans_fat": extract_value(r"Trans Fat\s+(\d+\.?\d*)", text),
        "saturated_fat": extract_value(r"Saturated Fat\s+(\d+\.?\d*)", text),
        "sugars": extract_value(r"Sugars?\s+(\d+\.?\d*)", text),
    }

# -------------------------
# Image Upload
# -------------------------

def image_upload(reader):

    uploaded_file = st.file_uploader(
        "Upload Nutrition Label",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_file is not None:

        if "last_uploaded_file" not in st.session_state or \
           st.session_state.last_uploaded_file != uploaded_file.name:

            image = Image.open(uploaded_file)

            with st.spinner("Extracting nutrients from label..."):
                extracted = extract_nutrients_from_image(reader, image)

            for key, value in extracted.items():
                st.session_state[key] = value

            st.session_state.last_uploaded_file = uploaded_file.name

            st.success("Nutrients extracted and filled below!")

        # st.image(uploaded_file, width=250)

# --------------------------------
# Nutrient Inputs
# --------------------------------

def nutrient_inputs():

    serving_size = st.number_input(
        "Serving Size (g)",
        min_value=1.0,
        value=st.session_state.serving_size,
        step=1.0
    )

    inputs = {}

    for nutrient in NUTRIENTS:
        label = nutrient.replace("_", " ").title() + f' ({NUTRIENT_UNITS[nutrient]})'

        inputs[nutrient] = st.number_input(
            f"{label}",
            value=st.session_state[nutrient]
        )

    return serving_size, inputs

# --------------------------------
# Build Model Input
# --------------------------------

def build_model_input(nutrients, serving_size, category_id):

    converted = {
        MODEL_FEATURES[k]: convert_to_100g(v, serving_size)
        for k, v in nutrients.items()
    }

    converted["food_category_id"] = category_id

    return pd.DataFrame([converted])

# --------------------------------
# Prediction Display
# --------------------------------

def display_nutri_score(score, nutriscore_images):
    """Display Nutri Score image."""
    
    score_image = nutriscore_images.get(score)

    if score_image:
        st.image(score_image, width=250)
    else:
        st.warning("Nutri score image not found.")

def display_prediction(model, input_df, nutriscore_images):

    prediction = model.predict(input_df)[0]
    probs = model.predict_proba(input_df)

    confidence = np.max(probs) * 100

    label = GRADE_INFO[prediction]
    emoji = GRADE_EMOJI[prediction]

    # Title
    st.subheader(f"Nutri-Score Grade: {prediction}")

    # Image
    display_nutri_score(prediction, nutriscore_images)

    # Status message
    getattr(st, {
        "A": "success",
        "B": "success",
        "C": "warning",
        "D": "error",
        "E": "error"
    }[prediction])(f"{emoji} {label}")

    # Confidence
    st.write(f"**Confidence:** {confidence:.2f}%")

    # prob_df = pd.DataFrame(
    #     probabilities,
    #     columns=["Nutri A", "Nutri B", "Nutri C", "Nutri D", "Nutri E"]
    # )
    # st.dataframe(prob_df)



# --------------------------------
# App
# --------------------------------

def main():

    st.set_page_config(page_title="Food Health Classifier")

    st.title("Food Health Classification")

    init_session_state()

    model = load_model()
    food_category, sample_foods = load_data()
    reader = load_ocr_reader()
    nutriscore_images = load_nutriscore_images()

    st.sidebar.title("Navigation")
    selected_index = st.sidebar.radio(
        "Input Method",
        range(len(INPUT_OPTIONS)),
        format_func=lambda x: INPUT_OPTIONS[x]
    )
    st.sidebar.divider()

    if selected_index == 0:
        autofill_sample_food(sample_foods)

    elif selected_index == 1:
        image_upload(reader)

    elif selected_index == 2:
        st.write("Enter nutrients manually below.")
        
    with st.form("prediction_form"):
        st.subheader("Nutrient Information")

        serving_size, nutrient_values = nutrient_inputs()

        category_mapping = dict(
            zip(food_category["description"], food_category["id"])
        )

        selected_category = st.selectbox(
            "Select Food Category",
            list(category_mapping.keys())
        )

        category_id = category_mapping[selected_category]

        submit = st.form_submit_button("Predict")

    if submit:
        st.header("Prediction")

        input_df = build_model_input(
            nutrient_values,
            serving_size,
            category_id
        )

        display_prediction(model, input_df, nutriscore_images)


if __name__ == "__main__":
    main()