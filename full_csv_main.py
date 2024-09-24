import streamlit as st
import pandas as pd
import os
from io import BytesIO


# files import
from modules.text import *
from modules.feat import *

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
