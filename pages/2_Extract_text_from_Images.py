import streamlit as st
from PIL import Image
import cv2
import numpy as np
import easyocr
import time
import re

st.set_page_config(
    page_title="Image Text Extraction App",
    layout="centered",
)

# Define unit mappings and entity-unit mappings
unit_mapping = {
    'cm': 'centimetre', 'centimetre': 'centimetre', 'centimeters': 'centimetre',
    'foot': 'foot', 'feet': 'foot', 'ft': 'foot',
    'inch': 'inch', 'inches': 'inch', 'in': 'inch',
    'metre': 'metre', 'meters': 'metre', 'm': 'metre',
    'kl': 'kiloleter',
    'millimetre': 'millimetre', 'millimeters': 'millimetre', 'mm': 'millimetre',
    'yard': 'yard', 'yards': 'yard', 'yd': 'yard',
    'gram': 'gram', 'g': 'gram', 'gm': 'gram', 'grams': 'gram', 'gramme': 'gram', 'gms': 'gram',
    'kilogram': 'kilogram', 'kg': 'kilogram', 'kgs': 'kilogram', 'kilos': 'kilogram', 'kilograms': 'kilogram',
    'microgram': 'microgram', 'µg': 'microgram', 'micrograms': 'microgram',
    'milligram': 'milligram', 'mg': 'milligram', 'milligrams': 'milligram',
    'ounce': 'ounce', 'oz': 'ounce', 'ounces': 'ounce',
    'pound': 'pound', 'lb': 'pound', 'lbs': 'pound', 'pounds': 'pound',
    'ton': 'ton', 'tons': 'ton', 'tonnes': 'ton', 't': 'ton',
    'kilovolt': 'kilovolt', 'kv': 'kilovolt', 'kilovolts': 'kilovolt',
    'millivolt': 'millivolt', 'mv': 'millivolt', 'millivolts': 'millivolt',
    'volt': 'volt', 'v': 'volt', 'volts': 'volt',
    'watt': 'watt', 'w': 'watt', 'watts': 'watt',
    'kilowatt': 'kilowatt', 'kw': 'kilowatt', 'kilowatts': 'kilowatt',
    'centilitre': 'centilitre', 'cl': 'centilitre', 'centilitres': 'centilitre',
    'cubic foot': 'cubic foot', 'ft³': 'cubic foot', 'cubic feet': 'cubic foot',
    'cubic inch': 'cubic inch', 'in³': 'cubic inch', 'cubic inches': 'cubic inch',
    'cup': 'cup', 'c': 'cup', 'cups': 'cup',
    'decilitre': 'decilitre', 'dl': 'decilitre', 'decilitres': 'decilitre',
    'fluid ounce': 'fluid ounce', 'fl oz': 'fluid ounce', 'fluid ounces': 'fluid ounce',
    'gallon': 'gallon', 'gal': 'gallon', 'gallons': 'gallon',
    'imperial gallon': 'imperial gallon', 'imp gal': 'imperial gallon', 'imperial gallons': 'imperial gallon',
    'litre': 'litre', 'l': 'litre', 'litres': 'litre', 'liters': 'litre',
    'microlitre': 'microlitre', 'µl': 'microlitre', 'microlitres': 'microlitre',
    'millilitre': 'millilitre', 'ml': 'millilitre', 'millilitres': 'millilitre',
    'pint': 'pint', 'pt': 'pint', 'pints': 'pint',
    'quart': 'quart', 'qt': 'quart', 'quarts': 'quart'
}

entity_unit_map = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'item_weight': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'maximum_weight_recommendation': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre', 'cubic foot', 'cubic inch', 'cup', 'decilitre', 'fluid ounce', 'gallon', 'imperial gallon', 'litre', 'microlitre', 'millilitres', 'pint', 'quart'}
}

# Your image processing class with updated methods
class ImageProcessingPipeline:
    def __init__(self, image=None):
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
    
    def extract_values_with_units(self, text):
        """Extract numeric values with units from the given text."""
        pattern = r'(\d+\.?\d*)\s*(centimetre|centimeters?|cm|foot|feet|ft|inch|inches?|in|millivolt|mv|millilitre|ml|milligram|mg|millimeter|millimeters?|mm|metre|meters?|m|yard|yards?|yd|gallon|gal|gallons?|gram?|g|grams?|gms?|gramme|kiloleter?|kl|kilowatt|kw|kilogram|kg|kgs?|kilos?|kilograms?|kilo|microgram|µg|ounce|ounces?|oz|pound|pounds?|lbs?|lb|ton|tons?|tonnes?|t|kilovolt|kv|volt|volts?|v|watt|watts?|w|centilitre|cl|centilitres?|cubic\s*foot|ft³|cubic\s*feet?|cubic\s*inch|in³|cup|cups?|c|decilitre|dl|decilitres?|fluid\s*ounce|fl\s*oz|fluid\s*ounces?|imperial\s*gallon|imp\s*gal|litre|litres?|l|liters?|microlitre|µl|pint|pints?|pt|quart|quarts?|qt)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        extracted_info = []
        for value, unit in matches:
            full_unit = unit_mapping.get(unit.lower(), unit)
            extracted_info.append(f"{value} {full_unit}")
        return extracted_info

# Streamlit application layout
st.title("Entity Text Extraction Application")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image_processing_pipeline = ImageProcessingPipeline()
    image_processing_pipeline.load_image_from_file(uploaded_file)

    # Show the image preview
    st.image(image_processing_pipeline.image, caption="Uploaded Image", use_column_width=True)

    # Extract text with a progress bar
    with st.spinner("Extracting text..."):
        progress_bar = st.progress(0)
        image_processing_pipeline.extract_text(progress_callback=lambda p: progress_bar.progress(p))
    
    # Display extracted text
    extracted_text = image_processing_pipeline.get_extracted_text()
    st.subheader("Extracted Text")
    st.write(extracted_text)

    # User selects an entity
    selected_entity = st.selectbox("Select an entity", list(entity_unit_map.keys()))
    
    # Display relevant values based on the selected entity
    if selected_entity:
        extracted_values = image_processing_pipeline.extract_values_with_units(extracted_text)
        relevant_values = [value for value in extracted_values if any(unit in value for unit in entity_unit_map[selected_entity])]
        
        if relevant_values:
            st.subheader(f"Relevant Values for {selected_entity.capitalize()}")
            for value in relevant_values:
                st.write(value)
        else:
            st.write(f"No relevant values found for {selected_entity}.")
