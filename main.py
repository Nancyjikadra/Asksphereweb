import streamlit as st
import requests
import os

# Set page configuration
st.set_page_config(page_title="Video Q&A", page_icon="🎥")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f5;
        padding: 20px;
        border-radius: 10px;
    }
    h1 {
        color: #333;
    }
    .trust-elements {
        margin-top: 20px;
        font-size: 14px;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Video Question Answering")

# User input
question = st.text_input("Ask a question about the videos:")

if question:
    # Call the backend API
    response = requests.post(f"{os.getenv('API_URL')}/api/predict", json={"question": question})
    if response.status_code == 200:
        result = response.json()
        st.subheader("Answer")
        st.write(result["answer"])
        st.subheader("Confidence")
        st.write(f"{result['confidence']:.2%}")
        st.subheader("Selected Videos")
        st.write(", ".join(result["selected_videos"]))
        st.subheader("Context")
        st.write(result["context"])
    else:
        st.error("Error: Unable to get a response from the server.")

# Trust elements
st.markdown("""
    <div class="trust-elements">
        <p>We value your privacy. Read our <a href="/privacy-policy">Privacy Policy</a>.</p>
        <p>For any inquiries, contact us at <a href="mailto:support@example.com">support@example.com</a>.</p>
    </div>
""", unsafe_allow_html=True)
