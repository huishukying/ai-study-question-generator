import PyPDF2
from PIL import Image
import pytesseract
import os

def extract_pdf(pdf_file): #PyPDF2
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        all_text = ""

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if text:
                all_text += text + "\n"

        if not all_text.strip():
            return "ERROR: Cannot extract text from the PDF."

        return all_text.strip()
    
    except Exception as e:
        return f"ERROR reading PDF: {str(e)}"


def extract_image(image_file): #Tesseract OCR
    try:
        image = Image.open(image_file)

        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')
        
        text = pytesseract.image_to_string(image, lang='eng')

        if not text.strip():
            return "ERROR: Cannot extract text from the image."

        return text.strip()

    except Exception as e:
        return f"ERROR processing image: {str(e)}"


def extract_text(file):
    file_type = file.type

    if file_type == "application/pdf":
        return extract_pdf(file)
    elif file_type.startswith("image/"):
        return extract_image(file)
    else:
        return f"ERROR: Unsupported file type: {file_type}"