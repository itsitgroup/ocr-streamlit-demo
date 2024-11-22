import io
import streamlit as st
import requests
import base64
from PIL import Image

# Serverless function URL
BACKEND_URL = st.secrets['BASE_URL']

st.title("Image to Text Converter")

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
    response = requests.post(
        BACKEND_URL,
        data=image_base64
    )

    if response.status_code == 200:
        # Display the extracted text
        st.write("Extracted Text:")
        st.write(response.text)
    else:
        st.error(f"Error: {response.text}")