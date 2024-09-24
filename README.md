# CSV and Image Text Extraction App

**Developed by:**
- **Pratham Bisht** [GitHub](https://github.com/Pratham216)
- **Keshav Kushwaha** [GitHub](https://github.com/offline-keshav)
- **Ritik Gupta** [GitHub](https://github.com/guptaritik17)

Welcome to the **CSV and Image Text Extraction App**! This project is designed to perform two main tasks:

1. **Text Extraction from Images**: Using Optical Character Recognition (OCR) to extract meaningful text from product images.
2. **CSV Prediction**: Automatically identify key unit-value pairs like width, weight, and more, based on product images provided through URLs.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Image Text Extraction](#image-text-extraction)
  - [CSV Prediction](#csv-prediction)
- [Technologies](#technologies)
- [License](#license)

## Project Overview

This application leverages **EasyOCR** for image-to-text extraction and processes CSV files to predict specific units and values from product data.

The app is designed for ease of use. You can upload product images for text extraction or upload CSV files with image URLs for unit-value prediction.

## Features

- **Image Processing Pipeline**: Downloads images from URLs and uses **EasyOCR** to extract text.
- **Unit Extraction**: Detects and standardizes units (e.g., cm, kg) from the extracted text.
- **Entity-Specific Prediction**: Identifies relevant unit-value pairs like "100 cm width".
- **Progress Tracking**: Real-time progress updates for both image and CSV processing.

## Installation

Follow these steps to set up and run the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install the required dependencies**:
   Install the dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

   If you are missing EasyOCR's dependencies (like `torch` and `opencv-python`), you can install them manually:
   ```bash
   pip install easyocr torch opencv-python-headless
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

## Usage

### Image Text Extraction

1. Navigate to the **Image Text Extraction** page on the app.
2. Upload an image file in **JPEG**, **PNG**, or **JPG** format.
3. The app will process the image and display the extracted text.

### CSV Prediction

1. Navigate to the **CSV Prediction** page on the app.
2. Upload a **CSV** file that contains two columns: 
   - `image_link`: URL of the image.
   - `entity_name`: Name of the entity (like width, height, weight, etc.).
3. The app will process the CSV file and generate unit-value predictions.

## Example CSV Format

Your CSV file should have the following structure:

| index | image_link                                  | entity_name      |
|-------|---------------------------------------------|------------------|
| 1     | https://example.com/image1.jpg              | width            |
| 2     | https://example.com/image2.jpg              | item_weight      |

## Technologies

- **Streamlit**: Used for building the web interface.
- **EasyOCR**: Used for Optical Character Recognition to extract text from images.
- **Pandas**: To process CSV files and handle tabular data.
- **OpenCV**: For image handling and preprocessing.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
