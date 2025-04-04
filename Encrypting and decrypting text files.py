import streamlit as st
from cryptography.fernet import Fernet
import random

st.markdown(
    """
    <style>
    
        /* Hide Streamlit Header and Menu */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}

        /* Set Fullscreen Background Image */
        .stApp {
            background: url("https://preview.redd.it/a7feesms1cu81.png?width=1920&format=png&auto=webp&s=fe804fb461b271a26a19de793383d09de496e45d") no-repeat center center fixed;
            background-size: cover;
        }

        /* Center Align Main Content */
        .stMain {
            display: flex;
            justify-content: center;
        }

        /* Glassmorphic Container */
        .stMainBlockContainer { 
            width: 40%; 
            padding: 16px;
            background: rgba(255, 255, 255, 0.09);
            box-shadow: 0 8px 32px 0 rgba(251, 10, 38), 0.37);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin: auto;
        }

        /* Title Container */
        .title-container { 
            text-align: center; 
            font-size: 24px;
            font-weight: bold;
            color: white;
        }

        /* Center Align Buttons */
        .button-container { 
            display: flex; 
            justify-content: center; 
        }

        /* Style Streamlit Buttons */
        .stButton>button {
            background-color: #FF4B4B !important;
            color: white !important;
            border-radius: 10px !important;
            font-size: 16px !important;
            padding: 10px 20px !important;
            border: none !important;
            box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.2) !important;
            transition: 0.3s ease-in-out;
        }

        .stButton>button:hover {
            background-color: #E33E3E !important;
            transform: scale(1.05);
        }

        /* Align Tabs */
        .stHorizontalBlock {
            margin-left: 15% !important;
            margin-right: 15% !important;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

if "file_storage" not in st.session_state:
    st.session_state.file_storage = {}

if "cipher" not in st.session_state:
    key = Fernet.generate_key()
    st.session_state.cipher = Fernet(key)

tab1, tab2 = st.tabs(["🔒 Encrypt File", "🔓 Decrypt File"])

with tab1:
    st.markdown("<div class='title-container'>Encrypt a Text File</div>", unsafe_allow_html=True)
    
    name = st.text_input("Enter File Name")
    uploaded_file = st.file_uploader("Upload a Text File", type=["txt"])

    if st.button("Encrypt & Save"):
        if name and uploaded_file:
            file_data = uploaded_file.read()
            encrypted_data = st.session_state.cipher.encrypt(file_data)
            password = str(random.randint(1000000, 9999999))
            
            st.session_state.file_storage[name] = {"encrypted": encrypted_data, "password": password}
            
            st.success(f"File '{name}' encrypted successfully!")
            st.write(f"🔑 **Password:** `{password}` (Save this to decrypt later)")
        else:
            st.warning("Enter a file name and upload a file!")

with tab2:
    st.markdown("<div class='title-container'>Decrypt a Text File</div>", unsafe_allow_html=True)

    if st.session_state.file_storage:
        selected_file = st.selectbox("Select Encrypted File", list(st.session_state.file_storage.keys()))
        entered_password = st.text_input("Enter 7-digit Password", type="password")

        if st.button("Decrypt & Download"):
            stored_password = st.session_state.file_storage[selected_file]["password"]
            if entered_password == stored_password:
                decrypted_data = st.session_state.cipher.decrypt(st.session_state.file_storage[selected_file]["encrypted"])
                st.success("File decrypted successfully! Download below:")
                st.download_button("Download Decrypted File", decrypted_data, f"{selected_file}_decrypted.txt", "text/plain")
            else:
                st.error("Incorrect password!")
    else:
        st.warning("No encrypted files available.")