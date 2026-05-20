from pypdf import PdfReader

def extract_text(file_obj, raw_text: str) -> tuple[str, str]:
    """Extracts text from a PDF file object or returns the raw text."""
    # Priority 1: Use File if uploaded
    if file_obj is not None:
        if file_obj.name.endswith('.pdf'):
            reader = PdfReader(file_obj.name)
            text = "".join([page.extract_text() + "\n" for page in reader.pages])
            return text, file_obj.name
        else:
            with open(file_obj.name, 'r', encoding='utf-8') as f:
                return f.read(), file_obj.name
                
    # Priority 2: Use Raw Text box
    return raw_text, "Manual_Entry.txt"