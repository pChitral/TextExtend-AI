from docx import Document

def create_word_document(file_name, response_list):
    doc = Document()
    
    for generated_text in response_list:
        paragraph = doc.add_paragraph(generated_text)
        paragraph.alignment = 0  # Left alignment
    
    doc.save(file_name + ".docx")
