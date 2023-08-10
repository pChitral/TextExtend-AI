from docx import Document

def create_word_document(file_name, response_list):
    doc = Document()
    for i, generated_text in enumerate(response_list):
        doc.add_paragraph(generated_text)

    doc.save(file_name + ".docx")
