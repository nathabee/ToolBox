
from PIL import Image, ImageDraw

# Create a transparent image (RGBA mode)
img_size = 200  # Width and height of the image
border_width = 4  # Thickness of the border

# Create a blank transparent image
img = Image.new("RGBA", (img_size, img_size), (255, 255, 255, 0))

# Create a draw object to add shapes to the image
draw = ImageDraw.Draw(img)

# Draw a square outline (border only)
draw.rectangle(
    [(border_width // 2, border_width // 2), (img_size - border_width // 2 - 1, img_size - border_width // 2 - 1)],
    outline="red",
    width=border_width,
)

# Save the image as a PNG file
output_path = "/mnt/data/transparent_border_square.png"
img.save(output_path)

output_path
