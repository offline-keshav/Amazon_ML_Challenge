import streamlit as st
from PIL import Image
import cv2
import numpy as np
import easyocr

# Your image processing class
class ImageProcessingPipeline:
    def _init_(self, image=None):
        self.image = image
        self.extracted_text = None
    
    def load_image_from_file(self, uploaded_file):
        """Load the uploaded image into OpenCV format."""
        image_bytes = uploaded_file.read()
        image_np = np.frombuffer(image_bytes, np.uint8)
        self.image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    
    def extract_text(self):
        """Extract text from the image using EasyOCR."""
        if self.image is None:
            raise FileNotFoundError("Image is not loaded.")
        
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

# Streamlit UI
st.title("Image to Text Extractor")

# Drag-and-drop file uploader
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

# Process the uploaded image when a file is provided
if uploaded_file is not None:
    try:
        # Initialize the processing pipeline with the uploaded file
        pipeline = ImageProcessingPipeline()
        
        # Load the uploaded image into the pipeline
        pipeline.load_image_from_file(uploaded_file)
        
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        
        # Extract text
        if st.button("Extract Text"):
            pipeline.extract_text()
            extracted_text = pipeline.get_extracted_text()
            
            # Display the extracted text
            st.write("Extracted Text:")
            st.write(extracted_text)
    
    except Exception as e:
        st.error(f"Error: {e}")