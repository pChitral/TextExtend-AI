import streamlit as st
from utils.text_processing import preprocess_text
from utils.document_creation import create_word_document
from utils.random_messages import random_messages
from docx import Document
from PyPDF2 import PdfReader
import openai
import os
import random
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def main():
    st.title("TextExtend AI: Amplify Your Word Documents from PDFs to Word with OpenAI")

    # User Input Section
    st.header("Step 1: Upload PDF and Input")
    system = st.text_input("Enter System Name:", key="system")
    prompt = st.text_area("Compose Your Prompt:", key="prompt")

    # Add input fields for temperature and max_tokens
    temperature = st.slider("Select Creativity Level", 0.0, 1.0, 0.8, 0.01)
    max_tokens = st.slider("Select Max Tokens", 1, 2048, 1500)

    # Upload PDF File
    uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])

    # Enable/Disable Upload Button
    if system and prompt:
        st.success("Both system and prompt provided. Ready for transformation.")
        upload_button_disabled = False
    else:
        st.warning("Please provide system and prompt to enable the upload button.")
        upload_button_disabled = True

    # PDF Processing
    if uploaded_file is not None:
        with st.spinner("Processing PDF..."):
            pdf_reader = PdfReader(uploaded_file)
            extracted_text = " ".join(
                [page.extract_text() for page in pdf_reader.pages]
            )
            cleaned_text = preprocess_text(extracted_text)
            text_chunks = [
                cleaned_text[i : i + 1500] for i in range(0, len(cleaned_text), 1500)
            ]

    # OpenAI API Calls
    if st.button("Increase Word Count", disabled=upload_button_disabled):
        progress_bar = st.progress(0)
        response_list = []

        # Set OpenAI API Key
        openai.api_key = OPENAI_API_KEY

        for i, chunk in enumerate(text_chunks):
            # Randomly select a message to display
            random_message = random.choice(random_messages)
            st.text(random_message)

            # Construct Prompt
            full_prompt = f"{prompt}\nPlease elaborate on the following passage enclosed in backticks / Text: `{chunk}`"

            # Chat Completion
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=full_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            output = response.choices[0].text.strip()
            response_list.append(output)

            # Update Progress
            progress_percentage = int(((i + 1) / len(text_chunks)) * 100)
            progress_bar.progress(progress_percentage)

        # Word Document Creation
        doc_file_name = os.path.splitext(uploaded_file.name)[0] + "_elegant"
        create_word_document(doc_file_name, response_list)

        # Display and Download Word Document
        with open(doc_file_name + ".docx", "rb") as docx_file:
            st.download_button(
                "Download",
                docx_file.read(),
                f"{doc_file_name}.docx",
            )


if __name__ == "__main__":
    main()
