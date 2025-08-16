import streamlit as st
import pickle
import pandas as pd
from streamlit_lottie import st_lottie
import requests

# Load the trained pipeline (model + preprocessing)
model = pickle.load(open("E:/Project/car_price_model.pkl", "rb"))

# --- Custom Page Config ---
st.set_page_config(page_title="Car Price Prediction", page_icon="🚗", layout="wide")

st.markdown(
    """
    <style>
    /* === Animated Gradient Background for whole interface === */
    body {
        background: linear-gradient(-45deg, #1e1e1e, #333333, #444444, #1a1a1a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: white;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* === General text + number input boxes === */
    input[type="text"], input[type="number"] {
        background-color: #2e2e2e !important;  /* darker so visible against bg */
        color: white !important;
        border-radius: 8px;
        border: 1px solid #777777;
        padding: 6px;
        transition: all 0.3s ease-in-out;
    }

    input[type="text"]:hover, input[type="number"]:hover {
        transform: scale(1.02);
        border-color: #aaaaaa;
        box-shadow: 0 0 10px rgba(255,255,255,0.3);
    }

    input[type="text"]:focus, input[type="number"]:focus {
        transform: scale(1.03);
        border-color: #ffffff;
        box-shadow: 0 0 15px rgba(255,255,255,0.5);
        outline: none !important;
    }

    /* Placeholder text */
    input::placeholder {
        color: #cccccc !important;
        transition: color 0.3s ease-in-out;
    }

    /* === Dropdown (selectbox) === */
    div[data-baseweb="select"] > div {
        background-color: #2e2e2e !important; /* darker like inputs */
        color: white !important;
        border-radius: 8px;
        border: 1px solid #777777;
        transition: all 0.3s ease-in-out;
    }

    div[data-baseweb="select"] > div:hover {
        transform: scale(1.02);
        border-color: #aaaaaa;
        box-shadow: 0 0 10px rgba(255,255,255,0.3);
    }

    div[data-baseweb="select"] > div:focus {
        transform: scale(1.03);
        border-color: #ffffff;
        box-shadow: 0 0 15px rgba(255,255,255,0.5);
    }

    /* Selected value text */
    div[data-baseweb="select"] span {
        color: white !important;
    }

    /* Dropdown menu options */
    div[data-baseweb="popover"] div {
        background-color: #2e2e2e !important;
        color: white !important;
        transition: background-color 0.2s ease-in-out;
    }

    div[data-baseweb="option"]:hover {
        background-color: #555555 !important;
        color: white !important;
        transform: scale(1.02);
    }
    </style>
    """,
    unsafe_allow_html=True
)






# --- Lottie Animation Loader ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

car_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")

# --- Title + Animation ---
st.title("🚗 Car Price Prediction App")
st_lottie(car_animation, height=250, key="car")

# --- User Inputs ---
st.subheader("Enter Car Details")
col1, col2 = st.columns(2)

with col1:
    car_name = st.text_input("Car Name", "Swift")
    year = st.number_input("Year of Purchase", min_value=1990, max_value=2025, value=2015)
    present_price = st.number_input("Present Price (in lakhs)", min_value=0.0, value=5.0, step=0.1)
    kms_driven = st.number_input("KMs Driven", min_value=0, value=30000, step=1000)

with col2:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    owner = st.number_input("Number of Previous Owners", min_value=0, max_value=3, value=0)

# --- Convert to DataFrame (same format as training) ---
input_data = pd.DataFrame([{
    "Car_Name": car_name,
    "Year": year,
    "Present_Price": present_price,
    "Kms_Driven": kms_driven,
    "Fuel_Type": fuel_type,
    "Seller_Type": seller_type,
    "Transmission": transmission,
    "Owner": owner
}])

# --- Prediction Button ---
if st.button("🔮 Predict Selling Price"):
    prediction = model.predict(input_data)[0]
    st.success(f"💵 Estimated Selling Price: **{prediction:.2f} lakhs**")
    st.balloons()  # 🎉 cool Streamlit animation
