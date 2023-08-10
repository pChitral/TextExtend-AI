def preprocess_text(text):
    # Normalize line breaks to '\n'
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace consecutive line breaks with a single line break
    text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])

    return text
