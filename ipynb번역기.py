import streamlit as st
import nbformat
from openai import OpenAI
import os
# dot env
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()  # OpenAI 클라이언트 초기화

def translate_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a translator. Translate the given text from English to Korean."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def process_notebook(file):
    # Read the notebook
    with open(file, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Process each cell
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            # Translate markdown content
            cell.source = translate_text(cell.source)

    # Save the translated notebook
    output_file = os.path.splitext(file)[0] + '_ko.ipynb'
    with open(output_file, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    return output_file

def main():
    st.title('IPYNB Markdown Translator')

    # API 키 입력
    api_key = st.text_input("Enter your OpenAI API key", type="password")
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        client.api_key = api_key

    # File uploader
    uploaded_file = st.file_uploader("Choose an IPYNB file", type=['ipynb'])

    if uploaded_file is not None and api_key:
        # Save the uploaded file temporarily
        with open("temp.ipynb", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process the notebook
        output_file = process_notebook("temp.ipynb")

        # Provide download link
        with open(output_file, "rb") as f:
            st.download_button(
                label="Download translated notebook",
                data=f,
                file_name=output_file,
                mime="application/x-ipynb+json"
            )

        # Clean up
        os.remove("temp.ipynb")
        os.remove(output_file)

if __name__ == '__main__':
    main()