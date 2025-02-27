# Image Extraction Tool

## Overview
The **Image Extraction Tool** is a command-line Python script that processes images for background removal, resizing, and edge detection. The tool is fully configurable via a **JSON configuration file**.

## Features
- **Background Removal**: Uses a reference image to determine the dominant background color and removes it, making it transparent.
- **Fallback Mechanism**: If no reference image is provided, the tool automatically detects the background color from the top-left 10% of the input image.
- **Image Resizing**: Allows resizing the image while preserving its aspect ratio using predefined sizes.
- **Edge Detection**: Extracts edges from the processed image and applies a customizable color to the contours.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Required Python libraries:
  ```sh
  pip install opencv-python numpy pillow
  ```

## Usage
### Command Line Execution
Run the tool by specifying the configuration file:
```sh
python image_extraction.py config.json
```

### Configuration File (JSON)
The tool relies on a **JSON configuration file** to specify processing steps.

Example `config.json`:
```json
{
  "background": {
    "input": "/path/to/input.jpg",
    "reference": "/path/to/background.jpg",
    "tolerance": 30
  },
  "resize": {
    "size": "M"
  },
  "styling": {
    "brightness": 200,
    "threshold1": 50,
    "threshold2": 150,
    "color": "0,255,0"
  }
}
```

## Processing Steps
### 1. Background Removal
- If a **reference image** is provided, the script extracts the dominant color and removes it.
- If the reference image is missing, the script falls back to using the **top-left 10% region** of the input image.

### 2. Resizing
- The resized image keeps its **aspect ratio** while fitting within predefined sizes:
  - **S** → 150px max width/height
  - **M** → 300px max width/height
  - **L** → 600px max width/height
  - **XL** → 1200px max width/height
  - **XXL** → 2400px max width/height

### 3. Edge Detection
- Applies **Canny edge detection** to extract the contours of objects.
- The contour color is customizable via the **JSON file** (`color`: "R,G,B").

## Output Files
- **`_transparent.png`** → Image with background removed.
- **`_resized.png`** → Resized image (if resizing is enabled).
- **`_edge.png`** → Image with detected edges.

## Error Handling
- If the reference image is missing, a **warning** is displayed, and the tool defaults to using the input image for color detection.
- If an incorrect JSON format is provided, an **error message** will be displayed.

## Future Enhancements
- Option for **manual background color selection**.
- Additional **image filtering options** (e.g., smoothing, sharpening).

## License
This tool is open-source and can be freely modified and distributed.

## Support
For issues or feature requests, please contact: `nathabee123@google.com`

