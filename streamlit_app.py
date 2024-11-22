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
        <img src="https://github.com/itsitgroup/ocr-streamlit-demo/blob/main/logo.png" alt="Its IT Group Logo">
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

        # Ensure the image is in RGB mode for JPEG compatibility
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Display the uploaded image
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert the image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Send the base64-encoded image to the backend
        with st.spinner("Processing image..."):
            payload = {"body": image_base64}  # Wrap base64 string in a JSON object
            response = requests.post(
                BACKEND_URL,
                json=payload  # Use `json` parameter to send as JSON
            )

        if response.status_code == 200:
            # Display the extracted text
            st.success("Text Extraction Successful!")
            
            # Parse the response
            extracted_data = response.json()
            
            # Ensure 'body' is parsed as JSON if it's a string
            body_data = extracted_data["body"]
            if isinstance(body_data, str):
                body_data = eval(body_data)  # Safely convert string to dictionary

            # Display the extracted text and processing time
            st.markdown(
                f"""
                <div style="padding: 10px; background-color: #e8f5e9; border-radius: 5px;">
                    <strong>Extracted Text:</strong>
                    <p>{body_data['text']}</p>
                    <strong>Processing Time:</strong> {body_data['elapsedTime']}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.error(f"Error: {response.json().get('body', 'Unknown error occurred')}")

    # End container styling
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        &copy; 2024 Its IT Group. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)