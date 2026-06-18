# services/parser.py
import fitz  # PyMuPDF
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts raw text content from uploaded PDF byte streams.
    """
    try:
        # Open the PDF directly from the byte stream
        pdf_stream = io.BytesIO(file_bytes)
        doc = fitz.open(stream=pdf_stream, filetype="pdf")
        
        extracted_text = []
        for page in doc:
            extracted_text.append(page.get_text())
            
        doc.close()
        return "\n".join(extracted_text).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF document: {str(e)}")