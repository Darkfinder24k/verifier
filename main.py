import random
import string
from captcha.image import ImageCaptcha
from PIL import Image
import os
import streamlit as st
import webbrowser as wb

# ✅ Page Setup - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="⚛️ Quantora AI Premium", layout="wide")

# Initialize session state variables if they don't exist
# ✅ Session state init
if "verified" not in st.session_state:
    st.session_state.verified = False
if "captcha_text" not in st.session_state:
    st.session_state.captcha_text = ""
if "captcha_filename" not in st.session_state:
    st.session_state.captcha_filename = ""
if "captcha_input" not in st.session_state:
    st.session_state.captcha_input = ""
if "chat" not in st.session_state:
    st.session_state.chat = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ✅ Captcha Generation
def generate_captcha():
    image = ImageCaptcha()
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    filename = f"captcha_{captcha_text}.png"
    image.write(captcha_text, filename)
    return filename, captcha_text

# ✅ Human Verification (Image Captcha)
if not st.session_state.verified:
    st.title("🔐 Human Verification")
    st.write("Please complete the image CAPTCHA below:")

    if not st.session_state.captcha_filename:
        captcha_file, generated_text = generate_captcha()
        st.session_state.captcha_text = generated_text
        st.session_state.captcha_filename = captcha_file
    else:
        captcha_file = st.session_state.captcha_filename
        generated_text = st.session_state.captcha_text

    st.image(captcha_file, caption="Enter the text you see above", use_column_width=False)
    user_input = st.text_input("🔏 Enter Captcha Text", key="captcha_input_field")

    if st.button("Verify"):
        if user_input.strip().upper() == st.session_state.captcha_text: # Now comparing against the stored text
            st.success("✅ Verification successful!")
            st.session_state.verified = True
            if os.path.exists(st.session_state.captcha_filename):
                os.remove(st.session_state.captcha_filename)
            st.session_state.captcha_filename = ""
            st.session_state.captcha_text = "" # Clear the stored text
            st.rerun()
        else:
            st.error("❌ Incorrect CAPTCHA. Please try again.")
            if os.path.exists(st.session_state.captcha_filename):
                os.remove(st.session_state.captcha_filename)
            st.session_state.captcha_filename = ""
            st.session_state.captcha_text = "" # Clear the stored text
            st.rerun()

    st.stop()

# ✅ Main AI Interface (will only show if st.session_state.verified is True)
else:
    wb.open('https://quantoraai.streamlit.app')
