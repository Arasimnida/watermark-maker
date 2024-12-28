import sys
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

def create_watermark(text, output_watermark_file):
    """Creates a PDF containing the watermark text diagonally across the page with good spacing."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 30)
    can.setFillColorRGB(0.8, 0.8, 0.8, alpha=0.5)
    can.rotate(45)
    width, height = map(int, letter)

    text_width = can.stringWidth(text, "Helvetica", 30)
    horizontal_spacing = int(text_width + 50)
    vertical_spacing = 100
    for x in range(-width, width * 2, horizontal_spacing):
        for y in range(-height, height * 2, vertical_spacing):
            can.drawString(x, y, text)
    
    can.save()
    packet.seek(0)
    with open(output_watermark_file, "wb") as f:
        f.write(packet.getbuffer())


def add_watermark(input_pdf, watermark_pdf, output_pdf):
    """Adds a watermark to an existing PDF."""
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    watermark = PdfReader(watermark_pdf).pages[0]
    
    for page in reader.pages:
        page.merge_page(watermark)
        writer.add_page(page)
    
    with open(output_pdf, "wb") as f:
        writer.write(f)

def main():
    if (len(sys.argv) != 3):
        print("\033[31m==> Error : Incorrect number of argument.\033[31m")
        print("==> Usage: python3 watermark.py <file.pdf> <watermark text>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    watermark_text = sys.argv[2]
    output_pdf = os.path.splitext(input_pdf)[0] + "-watermarked.pdf"

    if not os.path.exists(input_pdf):
        print(f"\033[31m==> Error : The file '{input_pdf}' does not exist. Check if the path to the file is correct.\033[31m")
        sys.exit(1)

    temp_watermark_file = "temp_watermark.pdf"

    print(f"==> Création du filigrane avec le texte : {watermark_text}")
    create_watermark(watermark_text, temp_watermark_file)
    print("==> Done.")
    print(f"==> Ajout du filigrane au fichier : {input_pdf}... ")
    add_watermark(input_pdf, temp_watermark_file, output_pdf)
    print("==> Done.")

    os.remove(temp_watermark_file)

    print(f"==> Fichier final généré : {output_pdf}")

if __name__ == "__main__":
    main()