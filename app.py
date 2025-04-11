import streamlit as st
from PIL import Image
import io
import time
import zipfile
import os
import shutil
from datetime import datetime

# Fonction pour signer l'image
def signer_image(image, filigrane):
    img = image.convert("RGBA")
    filigrane = filigrane.convert("RGBA")

    # Adapter la taille du filigrane
    logo_width = int(img.width * 0.2)
    logo_height = int(filigrane.height * (logo_width / filigrane.width))
    filigrane = filigrane.resize((logo_width, logo_height), Image.LANCZOS)

    # Coller le filigrane en bas à gauche
    position = (10, img.height - logo_height - 10)
    img.paste(filigrane, position, mask=filigrane)

    return img

# -------- Interface Streamlit --------
st.set_page_config(page_title="ANAM Signature App", page_icon="anam_logo_s3T_icon.ico", layout="centered")

# Animation d'ouverture
with st.spinner('Chargement de l\'application...'):
    time.sleep(2)

# Logo interface
st.image("anam_logo.png", width=200)
st.title("🔵 Application de Signature Automatique - ANAM")

# Style
st.markdown(""" 
<style>
    .css-1d391kg {background-color: #f0f4ff;}
    .css-18e3th9 {background-color: #f0f4ff;}
    .stButton>button {
        background-color: #2574f4;
        color: white;
        height: 3em;
        width: 100%;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Upload
uploaded_files = st.file_uploader("Téléverse tes photos à signer", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    # Charger le filigrane
    filigrane = Image.open("FILIGRANE_ANAM.png")

    # Dossier temporaire
    temp_dir = "temp_images"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    signed_images = []

    for idx, uploaded_file in enumerate(uploaded_files):
        image = Image.open(uploaded_file)
        signed_image = signer_image(image, filigrane)

        # Sauvegarder dans dossier temporaire
        save_path = os.path.join(temp_dir, f"signed_{idx}.png")
        signed_image.save(save_path)
        signed_images.append(save_path)

    # Télécharger toutes les images dans un zip
    zip_filename = f"signed_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for img_path in signed_images:
            zipf.write(img_path, os.path.basename(img_path))

    with open(zip_filename, "rb") as fp:
        btn = st.download_button(
            label="📦 Télécharger toutes les images signées",
            data=fp,
            file_name=zip_filename,
            mime="application/zip"
        )

    # Nettoyer
    for img_path in signed_images:
        os.remove(img_path)
    os.remove(zip_filename)
    shutil.rmtree(temp_dir)
