import os
import random
import pandas as pd
import requests
import easyocr
import cv2
import numpy as np
import re
import csv
from tqdm import tqdm

# files import
from modules.text import *
from modules.feat import *

def predictor(image_link, category_id, entity_name):
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

def save_progress(df, output_filename):
    """Save intermediate progress to a CSV file"""
    df.to_csv(output_filename, index=False)
    print(f"Progress saved to {output_filename}")

if __name__ == "__main__":
    DATASET_FOLDER = './data/'
    # Ouput file
    output_filename = os.path.join(DATASET_FOLDER, 'test_out.csv')

    # Input file
    test = pd.read_csv(os.path.join(DATASET_FOLDER, 'test.csv'))

    # Check if there's a previously saved file to resume from
    if os.path.exists(output_filename):
        processed_test = pd.read_csv(output_filename)
        start_index = len(processed_test)
        test = test.iloc[start_index:]  # Skip already processed rows
        print(f"Resuming from row {start_index} in saved file.")
    else:
        processed_test = pd.DataFrame(columns=['index', 'prediction'])  # Initialize empty DataFrame
        start_index = 0

    # Wrapping iterrows() with tqdm to show the progress bar
    for i, row in tqdm(test.iterrows(), total=len(test), desc="Processing rows"):
        try:
            prediction = predictor(row['image_link'], row['group_id'], row['entity_name'])
            new_row = pd.DataFrame({'index': [row['index']], 'prediction': [prediction]})

            # Use pd.concat instead of append
            processed_test = pd.concat([processed_test, new_row], ignore_index=True)
            
            # Save after every row or at certain intervals (e.g., every 10 rows)
            if i % 10 == 0 or i == len(test) - 1:
                save_progress(processed_test, output_filename)

        except Exception as e:
            print(f"Error processing row {i}: {e}")
            continue  # Skip this row and move on

    # Final save
    save_progress(processed_test, output_filename)
    print("Processing complete.")
