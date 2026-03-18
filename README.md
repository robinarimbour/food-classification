# Food Health Classification using Machine Learning

This project predicts the **health category of food products** based on their nutritional composition using **supervised machine learning**.  
The model was trained using the [**USDA SR Legacy Food Dataset**](https://fdc.nal.usda.gov/download-datasets/), a publicly available dataset containing standardized nutritional information for a wide variety of food products.
The target output is derived from the [**Nutri-Score system**](https://en.wikipedia.org/wiki/Nutri-Score), which evaluates food healthiness using key nutritional factors.

A **Streamlit web application** is included to allow users to input nutritional values and receive real-time predictions.

---

## Features

- Multi-class food health classification
- Target labels based on **Nutri-Score**
- Nutritional feature based prediction
- Interactive **Streamlit web app**
- Reproducible ML workflow using Jupyter notebooks

---

## Technologies Used

- Python
- Pandas, NumPy
- Scikit-learn
- Matplotlib / Seaborn
- Streamlit
- Jupyter Notebook

---

## Project Structure

    food-health-classification
    │
    ├── app.py
    ├── utils.py
    ├── requirements.txt
    ├── README.md
    │
    ├── assets/
    ├── datasets/
    ├── model_v2/
    |   └── pipeline_rf.pkl
    │
    └── notebooks/
        └── MultiClassFoodHealthClassification.ipynb

---

## Machine Learning Workflow

1. **Data Transformation**  
   The dataset was constructed by merging three CSV files — `food.csv`, `nutrients.csv`, and `food_nutrients.csv` — into a single consolidated DataFrame containing the nutritional attributes for each food item.

2. **Feature Selection**  
   Nutritional attributes such as protein, fat, carbohydrates, energy, fiber, sodium, sugar, saturated fat, trans fat, cholesterol, potassium and food category were selected as model inputs.

3. **Data Preprocessing**  
   - Handling missing values  
   - Finding outliers and validating nutritional features  
   - Checking correlation and removing irrelevant columns

4. **Nutri-Score Label Generation**  
   Nutri-Score rules were applied to compute the target labels used for classification.

5. **Feature Encoding & Scaling**  
   Within the model pipeline, categorical features were **one-hot encoded** and numerical features were **normalized** to ensure consistent feature scaling during model training.

6. **Model Training**  
   The following models were trained and evaluated:
   - K-Nearest Neighbors (KNN)
   - Naive Bayes
   - Decision Tree
   - Random Forest

7. **Model Performance**  
   Best accuracy achieved: Random Forest (**90.1%**)

8. **Deployment**  
   The trained model was integrated into a **Streamlit application** for real-time food health classification.

---

## Limitations

- **Missing FVNL Percentage**  
  The official Nutri-Score algorithm uses the percentage of **Fruits, Vegetables, Nuts, and Legumes (FVNL%)** to assign positive points.  
  This dataset did not contain FVNL%, so the **food category was used as an approximation**, which may not accurately represent the actual composition of the product.

- **Cheese Rule Not Implemented**  
  Nutri-Score applies a **special scoring rule for cheese**, allowing protein points to be counted even when negative nutrient points are high.  
  Since the dataset did not clearly identify cheese products, this rule was not applied.

- **Beverage Rules Not Applied**  
  Nutri-Score uses **separate scoring rules for beverages**, with different thresholds and scoring logic.  
  In this project, beverage-specific scoring was not implemented and beverage items were handled using the **machine learning model instead of Nutri-Score rules**.

- **Red Meat Rules Not Implemented**  
  The Nutri-Score algorithm includes specific considerations for **red meat products** in its updated versions. These category-specific adjustments were not applied due to limited product-level classification in the dataset.

- **Added Fats Rules Not Implemented**  
  Nutri-Score applies **special scoring rules for added fats (such as oils and butter)** with different thresholds and evaluation criteria. These rules were not implemented, as the dataset did not clearly distinguish added fats from other food categories.

---

## License

This project is open source and available under the **MIT License**.
