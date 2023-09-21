
from barcode import generate
from barcode.writer import ImageWriter

from reportlab.lib.pagesizes import A6
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
import datetime 
import os

def generete_barcode(barcode_string, app_path):

    # Generate the barcode
    current_date = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    barcode_image_output = os.path.join(app_path, 'barcodes\images', 'barcode_image'+ current_date)
    barcode_image = generate('code39', barcode_string, writer=ImageWriter(), output=barcode_image_output)


    # Create a PDF with A6 page size
    barcode_pdf_output = os.path.join(app_path, 'barcodes\pdfs', 'barcode_palette'+ current_date + '.pdf')
    doc = SimpleDocTemplate(barcode_pdf_output, pagesize=A6)

    # Load the barcode image and adjust its size
    barcode_img_path = barcode_image_output+'.png'
    barcode_width = 2.2 * inch
    barcode_height = 0.375 * inch

    # Create instances of Image for each barcode
    top_row_barcodes = [Image(barcode_img_path, width=barcode_width, height=barcode_height) for _ in range(6)]
    bottom_barcode = Image(barcode_img_path, width=4*inch, height=0.75*inch)

    # Create a list to store the content for the PDF
    pdf_content = []

    # Add the top row of barcodes
    top_row_story = [barcode for barcode in top_row_barcodes]
    pdf_content.extend(top_row_story)

    # Add some space between the top and bottom barcodes
    pdf_content.append(Spacer(0.2, 0.65*inch))

    # Add the bottom horizontal barcode
    pdf_content.append(bottom_barcode)

    # Build the PDF
    doc.build(pdf_content)

