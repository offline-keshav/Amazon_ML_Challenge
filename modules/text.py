import requests
import easyocr
import cv2
import numpy as np

class ImageProcessingPipeline:
    def __init__(self, image_url):
        self.image_url = image_url
        self.image = None
        self.extracted_text = None
    
    def download_image(self):
        """Download the image from the URL and store it as an OpenCV image."""
        response = requests.get(self.image_url)
        if response.status_code == 200:
            # Convert the image bytes to a NumPy array
            image_np = np.frombuffer(response.content, np.uint8)
            # Decode the NumPy array into an image
            self.image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        else:
            raise Exception(f"Failed to download image from {self.image_url}, Status Code: {response.status_code}")
    
    def extract_text(self):
        """Extract text from the image using EasyOCR."""
        if self.image is None:
            raise FileNotFoundError("Image is not downloaded.")
        
        # Initialize the EasyOCR reader (supports multiple languages, here we use English)
        reader = easyocr.Reader(['en'])
        
        # Convert the image to RGB as EasyOCR expects RGB input
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
        # Perform OCR using EasyOCR
        result = reader.readtext(image_rgb)
        
        # Extract the text from the result
        self.extracted_text = ' '.join([text[1] for text in result])
    
    def get_extracted_text(self):
        """Return the extracted text."""
        if self.extracted_text is None:
            raise RuntimeError("Text extraction not performed.")
        return self.extracted_text

# Example usage
# image_url = "https://m.media-amazon.com/images/I/61cMeogK8gL.jpg"
# pipeline = ImageProcessingPipeline(image_url)

# Run the pipeline
# pipeline.download_image()
# pipeline.extract_text()
# extracted_text = pipeline.get_extracted_text()

# print("Extracted Text:\n", extracted_text)
