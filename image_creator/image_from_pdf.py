from pdf2image import convert_from_path
from PIL import Image

def pdf_to_png(pdf_path, output_folder, target_height_cm=20):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Convert cm to pixels (assuming 300 DPI)
    target_height_px = int((target_height_cm / 2.54) * 300)
    
    for idx, img in enumerate(images):
        # Get the original size of the image
        img_width, img_height = img.size

        # Calculate the target width to maintain aspect ratio
        aspect_ratio = img_width / img_height
        target_width_px = int(target_height_px * aspect_ratio)

        # Resize the image to the new dimensions (20cm height, maintaining aspect ratio)
        resized_img = img.resize((target_width_px, target_height_px))
        
        # Save the image as PNG in the specified output folder
        output_path = f"{output_folder}/page_{idx + 1}.png"
        resized_img.save(output_path, "PNG")
        print(f"Saved: {output_path}")

# Example usage
if __name__ == "__main__":
    pdf_path = "/home/nathalie/Downloads/Cartedevisite.pdf"  # Path to the PDF
    output_folder = "/home/nathalie/Downloads/png"       # Folder to save PNG files
    
    pdf_to_png(pdf_path, output_folder)
