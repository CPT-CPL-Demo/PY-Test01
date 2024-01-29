import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os
import re

def pdf_to_images(pdf_path, image_folder):
    os.environ['TESSDATA_PREFIX'] = r'C:\Program Files (x86)\Tesseract-OCR'
    doc = fitz.open(pdf_path)

    # Create output folder if it doesn't exist
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    for page_number in range(doc.page_count):
        page = doc[page_number]

        # Convert PDF page to image
        image = page.get_pixmap()

        # Convert PyMuPDF pixmap to PIL Image
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Save the PIL Image to the output folder
        image_path = os.path.join(image_folder, f"page_{page_number + 1}.png")
        pil_image.save(image_path)

        # Perform OCR on the image
        text = pytesseract.image_to_string(pil_image)

        # Print extracted text
        print(f"Text from page {page_number + 1}:\n{text}\n")

        # Process the extracted text to find signatures and dates
        signatures, dates = extract_signatures_and_dates(text)

        # Print results
        print(f"Signatures: {signatures}")
        print(f"Dates: {dates}\n")

    doc.close()

def extract_signatures_and_dates(text):
    signatures = re.findall(r'\b(signature|sign|approved)\b', text, flags=re.IGNORECASE)
    dates = re.findall(r'\b\d{1,2}/\d{1,2}/\d{4}\b', text)  # Example: MM/DD/YYYY

    return signatures, dates

# Example usage
pdf_file = 'sigdate.pdf'
output_folder = 'resimage'

pdf_to_images(pdf_file, output_folder)
