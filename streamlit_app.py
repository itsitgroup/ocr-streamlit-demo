import io
import streamlit as st
import requests
import base64
from PIL import Image

# Serverless function URL (set in Streamlit secrets)
BACKEND_URL = st.secrets['BASE_URL']

# Add custom CSS for styling
st.markdown(
    """
    <style>
    .main-container {
        background-color: #f7f9fc;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .logo {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .logo img {
        max-height: 60px;
        margin-right: 20px;
    }
    .header {
        color: #333333;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        font-size: 0.9em;
        color: #666666;
        margin-top: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 5px !important;
        font-size: 16px !important;
        padding: 10px 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display logo and title
st.markdown(
    """
    <div class="logo">
        <img src="https://yourcompanylogo.com/logo.png" alt="Company Logo">
        <h1 class="header">Image to Text Converter</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Main container for content
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Allow the user to upload an image file
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the uploaded image file using PIL
        image = Image.open(uploaded_file)

        # Display the uploaded image
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert the image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Send the base64-encoded image to the backend
        with st.spinner("Processing image..."):
            response = requests.post(
                BACKEND_URL,
                data=image_base64
            )

        if response.status_code == 200:
            # Display the extracted text
            st.success("Text Extraction Successful!")
            st.markdown(
                f"""
                <div style="padding: 10px; background-color: #e8f5e9; border-radius: 5px;">
                    <strong>Extracted Text:</strong>
                    <p>{response.text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.error(f"Error: {response.text}")

    # End container styling
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        &copy; 2024 Your Company Name. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)