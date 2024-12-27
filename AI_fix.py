import streamlit as st
from PIL import Image
import pandas as pd
import base64

# Set page configuration (hanya satu kali di awal)
st.set_page_config(page_title="MushroomCheck", page_icon="🍄", layout="wide")

# Fungsi untuk menambahkan background dari file lokal
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    b64_image = base64.b64encode(image_data).decode()
    bg_style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_image}");
            background-size: cover;
            background-position: center;
        }}
        </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# Fungsi prediksi (simulasi)
def predict_mushroom(odor, spore_print_color, gill_color, ring_type, bruises):
    if odor in ["foul", "pungent"] or spore_print_color == "green":
        return "Poisonous"
    return "Non-Poisonous"

# Inisialisasi state untuk navigasi halaman
if "page" not in st.session_state:
    st.session_state.page = "home"

# Halaman 1: Home
if st.session_state.page == "home":
    # Tambahkan background untuk halaman pertama
    add_bg_from_local("image.png")

    # Konten halaman pertama
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end; padding: 60px 50px 20px 0;">
            <div style="text-align: left; max-width: 500px;">
                <h1 style="color: #FFD700; margin-bottom: 4px; font-size: 55px; font-family: Arial, sans-serif;">
                    MushroomCheck
                </h1>
                <p style="color: #FFFFFF; font-size: 17px; font-family: Arial, sans-serif; line-height: 1.5; margin-bottom: 20px;">
                    Curious if the mushroom you found is edible or poison? <br>
                    Let us guide you with accurate predictions and valuable insights <br>
                    to make informed decisions.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Tombol untuk navigasi ke halaman kedua
    col1, col2 = st.columns([2.2, 2])  # Kolom kiri lebih besar
    with col2:
        if st.button("Go to Next Page"):
            st.session_state.page = "predict"
            st.rerun()  # Menggunakan st.rerun() di Streamlit versi terbaru

# Halaman 2: Predict
elif st.session_state.page == "predict":
    # Tambahkan background untuk halaman kedua
    add_bg_from_local("image2.png")

    # Load dataset
    data = pd.read_csv("mushroom_dataset_fix.csv")

    # Layout input prediksi
    col1, col2 = st.columns([1, 2])  # Kolom kiri kosong, kolom kanan untuk input
    with col1:
        st.write("")  # Kosongkan kolom kiri
    with col2:
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>Enter Your Mushroom Features Below</h2>", unsafe_allow_html=True)

        # Input pengguna terbagi dalam dua kolom
        col_right1, col_right2 = st.columns(2)

        # Input kolom pertama
        with col_right1:
            odor = st.selectbox("Odor", options=data['odor'].unique(), key="odor")
            spore_print_color = st.selectbox("Spore Print Color", options=data['spore_print_color'].unique(), key="spore")
            gill_color = st.selectbox("Gill Color", options=data['gill_color'].unique(), key="gill_color")
            ring_type = st.selectbox("Ring Type", options=data['ring_type'].unique(), key="ring_type")
            bruises = st.selectbox("Bruises", options=data['bruises'].unique(), key="bruises")

        # Input kolom kedua
        with col_right2:
            stalk_surface_above = st.selectbox("Stalk Surface Above Ring", options=data['stalk_surface_above_ring'].unique(), key="stalk_above")
            stalk_surface_below = st.selectbox("Stalk Surface Below Ring", options=data['stalk_surface_below_ring'].unique(), key="stalk_below")
            gill_size = st.selectbox("Gill Size", options=data['gill_size'].unique(), key="gill_size")
            stalk_color_above = st.selectbox("Stalk Color Above Ring", options=data['stalk_color_above_ring'].unique(), key="stalk_color_above")
            stalk_color_below = st.selectbox("Stalk Color Below Ring", options=data['stalk_color_below_ring'].unique(), key="stalk_color_below")

        # Tombol submit prediksi
        if st.button("Submit"):
            result = predict_mushroom(odor, spore_print_color, gill_color, ring_type, bruises)
            if result == "Poisonous":
                st.markdown("""<div style='text-align: center; color: red;'>
                    <h3>⚠️Warning!</h3>
                    <p>Based on the details you provided, this mushroom is <b>POISONOUS</b>. Do not consume it to ensure your safety.</p
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div style='text-align: center; color: green;'>
                    <h3>✅ Good News!</h3>
                    <p>Based on the details you provided, this mushroom is <b>NOT POISONOUS</b>. Make sure to cook it properly before consuming.</p>
                </div>""", unsafe_allow_html=True)
            st.info("""
    ℹ️ **Important Note**:  
    This prediction is based solely on the data you provided. For complete certainty, consult a **mycology expert** or mushroom specialist before consuming any wild mushrooms.
    """)
        
        # Tombol untuk kembali ke halaman utama
        st.markdown("---")
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()  # Menggunakan st.rerun() untuk navigasi ulang