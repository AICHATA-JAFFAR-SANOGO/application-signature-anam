import streamlit as st
from PIL import Image
import io
import time
import zipfile
import os
from datetime import datetime

# Fonction pour signer l'image
def signer_image(image, logo):
    img = image.convert("RGBA")
    logo = logo.convert("RGBA")

    # Adapter la taille du logo sans perte de qualité (utiliser un algorithme de redimensionnement de haute qualité)
    logo_width = int(img.width * 0.2)
    logo_height = int(logo.height * (logo_width / logo.width))
    logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

    # Coller le logo en haut à droite
    position = (img.width - logo_width - 10, 10)
    img.paste(logo, position, mask=logo)

    return img

# -------- Interface Streamlit --------
st.set_page_config(page_title="ANAM Signature App", page_icon="anam_logo_s3T_icon.ico", layout="centered")

# Animation d'ouverture
with st.spinner('Chargement de l\'application...'):
    time.sleep(2)

# Améliorer la visibilité du logo sur l'interface
st.image("anam_logo.png", width=200)
st.title("🔵 Application de Signature Automatique - ANAM")

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

uploaded_files = st.file_uploader("Téléverse tes photos à signer", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    logo = Image.open("anam_logo.png")

    # Créer un dossier temporaire pour stocker les images signées
    temp_dir = "temp_images"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    signed_images = []

    # Processus de signature pour chaque image
    for idx, uploaded_file in enumerate(uploaded_files):
        image = Image.open(uploaded_file)

        # Barre de progression
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)

        signed_img = signer_image(image, logo)

        # Enregistrer l'image signée dans le dossier temporaire
        img_path = os.path.join(temp_dir, f"signed_image_{idx+1}.png")
        signed_img.save(img_path, quality=95)  # Assurer une bonne qualité d'image

        signed_images.append(img_path)

    # Créer le fichier ZIP avec les images signées
    date_today = datetime.today().strftime('%Y-%m-%d')
    zip_filename = f"photos_signées_ANAM_{date_today}.zip"
    zip_path = os.path.join(temp_dir, zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in signed_images:
            zipf.write(file, os.path.basename(file))

    # Affichage et téléchargement du fichier ZIP
    with open(zip_path, "rb") as f:
        st.success(f"✅ Signature terminée ! Voici ton fichier ZIP :")
        st.download_button(
            label="Télécharger le fichier ZIP",
            data=f,
            file_name=zip_filename,
            mime="application/zip"
        )

    # Nettoyage du dossier temporaire
    for file in signed_images:
        os.remove(file)
    os.remove(zip_path)
    os.rmdir(temp_dir)
