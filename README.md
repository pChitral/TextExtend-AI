# TextExtend AI: Amplify Your Word Documents from PDFs to Word with OpenAI

This repository contains a Python script that transforms a PDF document into a stylish, AI-enhanced Word document using OpenAI's GPT-3 language model. The primary purpose of this script is to provide a user-friendly interface for uploading PDF files, entering system names, and composing prompts. The resulting Word document can be freely edited and customized by the user. With the implementation of this script, users can transform the content in a specific form at a single click of a button without worrying about the max prompt limit.

## Table of Contents

- [TextExtend AI: Amplify Your Word Documents from PDFs to Word with OpenAI](#textextend-ai-amplify-your-word-documents-from-pdfs-to-word-with-openai)
  - [Table of Contents](#table-of-contents)
  - [Setting Up OpenAI API](#setting-up-openai-api)
  - [Main Function](#main-function)
    - [Step 1: Upload PDF and Input](#step-1-upload-pdf-and-input)
    - [Step 2: PDF Processing](#step-2-pdf-processing)
    - [Step 3: OpenAI API Calls](#step-3-openai-api-calls)
    - [Step 4: Word Document Creation](#step-4-word-document-creation)
    - [Step 5: Download the Transformed Document](#step-5-download-the-transformed-document)
  - [Usage](#usage)
  - [Contributions](#contributions)
  - [Code of Conduct](#code-of-conduct)
  - [License](#license)
  - [Conclusion](#conclusion)

The script uses the `streamlit` library to create a simple web app interface for uploading a PDF file, entering a system name and composing a prompt.

```python
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
```

## Setting Up OpenAI API

The script requires setting up an OpenAI API key. The key is stored in an environmental variable which is loaded using `load_dotenv()`. Ensure to set up the `OPENAI_API_KEY` in your environment.

```python
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
```

## Main Function

The `main` function runs the primary logic of the script.

```python
def main():
    st.title("Elegant PDF to Word Transformation")
```

### Step 1: Upload PDF and Input

The user is prompted to enter a system name and compose a prompt. The user is then able to upload a PDF document.

```python
    system = st.text_input("Enter System Name:", key="system")
    prompt = st.text_area("Compose Your Prompt:", key="prompt")
    uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
```

The upload button is only enabled when both system name and prompt are provided.

### Step 2: PDF Processing

The uploaded PDF file is processed using `PyPDF2.PdfReader`. The extracted text is cleaned and split into chunks of 1500 characters.

```python
    pdf_reader = PdfReader(uploaded_file)
    extracted_text = " ".join([page.extract_text() for page in pdf_reader.pages])
    cleaned_text = preprocess_text(extracted_text)
    text_chunks = [cleaned_text[i : i + 1500] for i in range(0, len(cleaned_text), 1500)]
```

### Step 3: OpenAI API Calls

For each chunk of text, a call is made to the OpenAI API. The response is appended to a list. The progress of this process is displayed in a progress bar.

```python
    for i, chunk in enumerate(text_chunks):
        full_prompt = f"{prompt}\nPlease elaborate on the following passage enclosed in backticks / Text: `{chunk}`"
        response = openai.Completion.create(model="text-davinci-003", prompt=full_prompt, temperature=0.8, max_tokens=1500)
        output = response.choices[0].text.strip()
        response_list.append(output)
```

### Step 4: Word Document Creation

The responses gathered from the OpenAI API calls are compiled into a Word document using `create_word_document` function from `utils.document_creation`.

```python
    doc_file_name = os.path.splitext(uploaded_file.name)[0] + "_elegant"
    create_word_document(doc_file_name, response_list)
```

### Step 5: Download the Transformed Document

The user is then able to download the transformed Word document.

```python
    with open(doc_file_name + ".docx", "rb") as docx_file:
        st.download_button("Download Elegant Document", docx_file.read(), f"{doc_file_name}.docx")
```

To run the script:

```python
if __name__ == "__main__":
    main()
```

Make sure to install the necessary dependencies as specified in the `requirements.txt` file.

## Usage

1. Run the python script in your terminal.
2. Input the System Name and Compose Prompt.
3. Upload your PDF document.
4. Click on the `Transform to Elegant Document` button.
5. Download the AI-enhanced Word document.

## Contributions

This project is open-source and contributions are more than welcome. If you wish to contribute, please adhere to the code of conduct, fork the project, make your changes and submit a pull request.

## Code of Conduct

We aim to foster an open and welcoming environment in this project. Please read our [Code of Conduct](./CODE_OF_CONDUCT.md) to understand the expected behaviors.

## License

This project is open source and available under the [MIT License](./LICENSE.md).

## Conclusion

TextExtend AI is a free tool that accepts PDF as input and outputs an AI-enhanced Word document. The Word document can be edited as per the user's needs, making it a versatile tool for a variety of applications. Please note that the source code is available on GitHub.

This tool is designed to assist you in creating polished, professional documents, not to replace your unique writing style and creativity. Use it responsibly and maximize the benefit of automation while retaining your creative control!
