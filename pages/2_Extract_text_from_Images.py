import streamlit as st
from PIL import Image
import cv2
import numpy as np
import easyocr
import time


st.set_page_config(
    page_title="Image Text Extraction App",
    layout="centered",
)

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
    
    def extract_text(self, progress_callback=None):
        """Extract text from the image using EasyOCR with progress tracking."""
        if self.image is None:
            raise FileNotFoundError("Image is not loaded.")
        
        # Initialize the EasyOCR reader (supports multiple languages, here we use English)
        reader = easyocr.Reader(['en'])

        # Update progress for reader initialization
        if progress_callback:
            progress_callback(20)  # Progress at 20%

        # Convert the image to RGB as EasyOCR expects RGB input
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        # Update progress for image preprocessing
        if progress_callback:
            progress_callback(40)  # Progress at 40%

        # Simulate further stages of the process for better progress visualization
        time.sleep(1)  # Simulate processing time
        if progress_callback:
            progress_callback(60)  # Progress at 60%

        # Perform OCR using EasyOCR
        result = reader.readtext(image_rgb)

        # Update progress for OCR extraction
        if progress_callback:
            progress_callback(80)  # Progress at 80%

        # Extract the text from the result
        self.extracted_text = ' '.join([text[1] for text in result])

        # Update progress to 100% when done
        if progress_callback:
            progress_callback(100)  # Progress at 100%
    
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
            # Create a progress bar object and a text placeholder for percentage
            progress_bar = st.progress(0)
            progress_text = st.empty()
            
            # Callback function to update both progress bar and percentage text
            def update_progress(percentage):
                progress_bar.progress(percentage)
                progress_text.text(f"Progress: {percentage}%")
            
            # Run the text extraction with the progress bar callback
            pipeline.extract_text(progress_callback=update_progress)
            
            # Get and display the extracted text
            extracted_text = pipeline.get_extracted_text()
            
            st.write("Extracted Text:")
            st.write(extracted_text)
    
    except Exception as e:
        st.error(f"Error: {e}")