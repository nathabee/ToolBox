#Python code that uses Pillow to handle the image and reportlab to generate a PDF. 
#This code reads a square image in WEBP format and creates a PDF in A4 size
#with customizable margins and text positioning above and below the image.
import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

def create_pdf_with_image_and_text(
        image_path, 
        top_text="Top Text", bottom_text="Bottom Text", 
        top_text_font_size=12, bottom_text_font_size=12, 
        top_margin=30, bottom_margin=20, side_margin=20,
        add_double_underline=True, add_symbols=True, symbol="★"):
    
    # Generate the PDF path by appending ".pdf" to the image path
    pdf_path = f"{os.path.splitext(image_path)[0]}.pdf"
    
    # Open the image
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Define A4 page size
    page_width, page_height = A4
    
    # Calculate image placement (centered on page)
    image_width_on_page = page_width - 2 * side_margin * mm
    image_height_on_page = image_width_on_page  # since the image is square

    # Define the PDF canvas
    c = canvas.Canvas(pdf_path, pagesize=A4)
    
    # Calculate positions
    top_text_y = page_height - top_margin * mm
    image_y = top_text_y - top_text_font_size * mm - image_height_on_page
    bottom_text_y = image_y - bottom_text_font_size * mm
    
    # Add symbols at the beginning and end of the top text
    if add_symbols:
        top_text = f"{symbol} {top_text} {symbol}"
    
    # Draw top text
    c.setFont("Helvetica", top_text_font_size)
    c.drawCentredString(page_width / 2, top_text_y, top_text)

    # Add double underline if enabled
    if add_double_underline:
        underline_y = top_text_y - top_text_font_size * 0.25  # First line
        c.line((page_width - image_width_on_page) / 2, underline_y, 
               (page_width + image_width_on_page) / 2, underline_y)
        
        underline_y2 = underline_y - 1.5  # Second line slightly below
        c.line((page_width - image_width_on_page) / 2, underline_y2, 
               (page_width + image_width_on_page) / 2, underline_y2)
    
    # Resize and draw the image
    img = img.resize((int(image_width_on_page), int(image_height_on_page)))
    img_temp_path = "/tmp/temp_image.jpg"  # Temporary save as JPG for compatibility
    img.save(img_temp_path, format="JPEG")
    c.drawImage(img_temp_path, side_margin * mm, image_y, width=image_width_on_page, height=image_height_on_page)

    # Draw bottom text
    c.setFont("Helvetica", bottom_text_font_size)
    c.drawCentredString(page_width / 2, bottom_text_y, bottom_text)

    # Save the PDF
    c.showPage()
    c.save()
    print(f"PDF created successfully: {pdf_path}")

# Example usage:
create_pdf_with_image_and_text(
    image_path="/home/nathalie/Downloads/tmp/badzimmer3.webp", 
    top_text="SHOW MOM SOME LOVE",
    bottom_text="Don’t Let the Pipes Clog!",
    top_text_font_size=40,
    bottom_text_font_size=40,
    top_margin=30,
    bottom_margin=30,
    side_margin=20,
    add_double_underline=True,
    #add_symbols=True,
    #symbol="⚠️"
)


   # image_path="/home/nathalie/Downloads/tmp/badzimmer2.webp", 
   # top_text="CLEAN UP",
   # bottom_text="or Face the Toilet Troll!",
   # top_text_font_size=50,
   # bottom_text_font_size=30,


   # image_path="/home/nathalie/Downloads/tmp/badzimmer1.webp", 
   # top_text="NEVER AGAIN",
   # bottom_text="START CLEANING THE BATHROOM",
   # top_text_font_size=50,
   # bottom_text_font_size=30,