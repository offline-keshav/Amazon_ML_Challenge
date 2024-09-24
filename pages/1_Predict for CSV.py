import streamlit as st
import pandas as pd
from io import BytesIO
import re
import requests
import easyocr
import cv2
import numpy as np


# # files import
# from modules.text import *
# from modules.feat import *

st.set_page_config(
    page_title="CSV Text Extraction App",
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
    'item_volume': {'centilitre', 'cubic foot', 'cubic inch', 'cup', 'decilitre', 'fluid ounce', 'gallon', 'imperial gallon', 'litre', 'microlitre', 'millilitre', 'pint', 'quart'}
}

def extract_values_with_units(text):
    pattern = r'(\d+\.?\d*)\s*(centimetre|centimeters?|cm|foot|feet|ft|inch|inches?|in|millivolt|mv|millilitre|ml|milligram|mg|millimeter|millimeters?|mm|metre|meters?|m|yard|yards?|yd|gallon|gal|gallons?|gram?|g|grams?|gms?|gramme|kiloleter?|kl|kilowatt|kw|kilogram|kg|kgs?|kilos?|kilograms?|kilo|microgram|µg|ounce|ounces?|oz|pound|pounds?|lbs?|lb|ton|tons?|tonnes?|t|kilovolt|kv|volt|volts?|v|watt|watts?|w|centilitre|cl|centilitres?|cubic\s*foot|ft³|cubic\s*feet?|cubic\s*inch|in³|cup|cups?|c|decilitre|dl|decilitres?|fluid\s*ounce|fl\s*oz|fluid\s*ounces?|imperial\s*gallon|imp\s*gal|litre|litres?|l|liters?|microlitre|µl|pint|pints?|pt|quart|quarts?|qt)'


    matches = re.findall(pattern, text, re.IGNORECASE)
    extracted_info = []
    for value, unit in matches:
        full_unit = unit_mapping.get(unit.lower(), unit)
        extracted_info.append(f"{value} {full_unit}")
    return extracted_info

def get_value_for_entity(entity_name, text):
    if entity_name not in entity_unit_map:
        return []

    extracted_values = extract_values_with_units(text)
    valid_units = entity_unit_map[entity_name]
    
    for item in extracted_values:
        value, unit = item.split(maxsplit=1)
        if unit.lower() in valid_units:
            return [item]
    
    return []


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

# Dummy implementation for the predictor function
# Replace it with your actual implementation
def predictor(image_link, entity_name):
    '''
    Call your model/approach here
    '''
    try:
        pipeline = ImageProcessingPipeline(image_link)
        pipeline.download_image()
        pipeline.extract_text()
        extracted_text = pipeline.get_extracted_text()
        result = get_value_for_entity(entity_name, extracted_text)
        return result[0] if result else None
    except Exception as e:
        print(f"Error processing {image_link}: {e}")
        return None

# Function to process the input CSV and generate predictions with descriptive progress
def process_csv(input_df):
    processed_data = []
    progress_bar = st.progress(0)  # Initialize progress bar
    status_text = st.empty()  # Placeholder for status text

    total_rows = len(input_df)

    # Iterate through each row in the DataFrame
    for index, row in input_df.iterrows():
        prediction = predictor(row['image_link'], row['entity_name'])
        processed_data.append([row['index'], prediction])

        # Update progress bar and status text
        progress_percentage = int((index + 1) / total_rows * 100)
        progress_bar.progress(progress_percentage)
        status_text.text(f"Processing row {index + 1} of {total_rows}")

    # Convert results to DataFrame
    output_df = pd.DataFrame(processed_data, columns=['index', 'prediction'])

    # Clear status text after completion
    status_text.text("Processing complete!")
    return output_df

# Streamlit UI
def main():
    st.title("CSV Prediction App")

    # File upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file
        input_df = pd.read_csv(uploaded_file)
        st.write("Uploaded CSV file:")
        st.dataframe(input_df)

        # Process the CSV file and generate predictions
        if st.button('Run Predictions'):
            output_df = process_csv(input_df)
            st.write("Processed Results:")
            st.dataframe(output_df)

            # Download processed CSV
            csv = output_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='predictions.csv',
                mime='text/csv'
            )

if __name__ == "__main__":
    main()
