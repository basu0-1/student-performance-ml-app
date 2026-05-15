import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Student Predictor", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOG ACTIVITY ----------------
def log_activity(username, action):
    log_file = "logs.csv"

    new_log = {
        "username": username,
        "action": action,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.DataFrame([new_log])

    if os.path.exists(log_file):
        df.to_csv(log_file, mode='a', header=False, index=False)
    else:
        df.to_csv(log_file, index=False)

# ---------------- SAVE PREDICTION ----------------
def save_prediction(username, age, studytime, absences, prediction):
    file = "predictions.csv"

    new_data = {
        "username": username,
        "age": age,
        "studytime": studytime,
        "absences": absences,
        "prediction": prediction,
    }

    df = pd.DataFrame([new_data])

    if os.path.exists(file):
        df.to_csv(file, mode='a', header=False, index=False)
    else:
        df.to_csv(file, index=False)

# ---------------- LOGIN ----------------
def login():
    st.title("🔐 Login")

    username = st.text_input("Enter Username")

    if st.button("Enter App"):
        if username.strip():
            st.session_state.logged_in = True
            st.session_state.username = username
            log_activity(username, "login")
            st.rerun()
        else:
            st.error("Enter username")

# ---------------- LOGOUT ----------------
def logout():
    log_activity(st.session_state.get("username", "unknown"), "logout")
    st.session_state.logged_in = False
    st.rerun()

# ---------------- MAIN APP ----------------
def main_app():

    model = pickle.load(open("model/model.pkl", "rb"))
    features = pickle.load(open("model/features.pkl", "rb"))

    st.title("🎓 Student Performance Predictor")
    st.write(f"👤 Logged in as: {st.session_state.username}")

    if st.button("Logout"):
        logout()

    st.subheader("📋 Enter Student Details")

    age = st.slider("Age", 15, 22, 18)
    studytime = st.slider("Study Time (1-4)", 1, 4)
    absences = st.slider("Absences", 0, 30)
    sex = st.selectbox("Sex", ["Male", "Female"])
    school = st.selectbox("School", ["GP", "MS"])

    if st.button("Predict"):

        input_dict = {feature: 0 for feature in features}

        input_dict["age"] = age
        input_dict["studytime"] = studytime
        input_dict["absences"] = absences

        if "sex_M" in input_dict:
            input_dict["sex_M"] = 1 if sex == "Male" else 0

        if "school_MS" in input_dict:
            input_dict["school_MS"] = 1 if school == "MS" else 0

        input_data = np.array([list(input_dict.values())])
        prediction = model.predict(input_data)[0]

        save_prediction(
            st.session_state.username,
            age,
            studytime,
            absences,
            prediction
        )

        st.success(f"🎯 Predicted Final Grade: {prediction:.2f}")

# ---------------- ROUTING ----------------
if st.session_state.logged_in:
    main_app()
else:
    login()