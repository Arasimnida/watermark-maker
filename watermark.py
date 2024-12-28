import sys
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os
from tkinter import Tk, filedialog, simpledialog, messagebox

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
    root = Tk()
    root.withdraw()

    input_pdf = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not input_pdf:
        messagebox.showerror("Error", "No file selected. The operation has been cancelled.")
        return

    watermark_text = simpledialog.askstring("Watermark text", "Enter the watermark text :")
    if not watermark_text:
        messagebox.showerror("Error", "No watermark text provided. The operation has been cancelled.")
        return

    temp_watermark_file = "temp_watermark.pdf"
    output_pdf = os.path.splitext(input_pdf)[0] + "-watermarked.pdf"

    try:
        create_watermark(watermark_text, temp_watermark_file)
        add_watermark(input_pdf, temp_watermark_file, output_pdf)
        messagebox.showinfo("Sucess", f"Watermarked file created : {output_pdf}")
    except Exception as e:
        messagebox.showerror("Error", f"An error has occurred: {e}")
    finally:
        if os.path.exists(temp_watermark_file):
            os.remove(temp_watermark_file)

if __name__ == "__main__":
    main()