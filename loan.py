import streamlit as st
import pickle
import numpy as np

# Load the trained model
model_path = "loan_model.sav"
with open(model_path, 'rb') as file:
    model = pickle.load(file)



# UI Layout
st.title("Loan Status Prediction System")
st.markdown("This app predicts whether a loan application will be approved or not based on the provided details.")

# Input fields for user data
st.header("Applicant Information")
gender = st.selectbox("Gender", ["Male", "Female"])
married = st.selectbox("Marital Status", ["Single", "Married"])
dependents = st.selectbox("Number of Dependents", ["0", "1", "2", "3+"])
education = st.selectbox("Education Level", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed", ["No", "Yes"])
applicant_income = st.number_input("Applicant Income", min_value=0, step=1000, value=0)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0, step=1000, value=0)
loan_amount = st.number_input("Loan Amount (in thousands)", min_value=0, step=1, value=0)
loan_amount_term = st.selectbox("Loan Amount Term (in days)", [12, 36, 60, 84, 120, 180, 240, 300, 360])
credit_history = st.selectbox("Credit History", ["No", "Yes"])
property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

# Preprocess user inputs for prediction
def preprocess_input():
    gender_num = 1 if gender == "Male" else 0
    married_num = 1 if married == "Married" else 0
    dependents_num = 3 if dependents == "3+" else int(dependents)
    education_num = 0 if education == "Graduate" else 1
    self_employed_num = 1 if self_employed == "Yes" else 0
    credit_history_num = 1 if credit_history == "Yes" else 0
    property_area_map = {"Urban": 2, "Semiurban": 1, "Rural": 0}
    property_area_num = property_area_map[property_area]

    return np.array([[
        gender_num, married_num, dependents_num, education_num, self_employed_num,
        applicant_income, coapplicant_income, loan_amount, loan_amount_term,
        credit_history_num, property_area_num
    ]])

# Predict button
if st.button("Predict Loan Approval"):
    user_input = preprocess_input()
    prediction = model.predict(user_input)

    if prediction[0] == 1:
        st.success("The loan application is likely to be approved!")
    else:
        st.error("The loan application is likely to be rejected.")

# Footer
st.markdown("---")
st.text("Developed by Anirudh Sharma")
