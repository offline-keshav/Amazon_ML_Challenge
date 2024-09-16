## Team: Heavy Coders
- **Pratham Bisht**      (https://github.com/Pratham216)
- **Keshav Kushwaha**    (https://github.com/offline-keshav)
- **Ritik Gupta**        (https://github.com/guptaritik17)


---

## Overview
The `main.py` file serves as the main entry point for processing images, extracting relevant text using Optical Character Recognition (OCR), and retrieving specific unit-value pairs (such as width, weight, etc.) from the extracted text. The file integrates functionalities from two other modules, `text.py` and `feat.py`, by importing their classes and functions. Additionally, it includes features for saving progress during execution to allow for resumption from the last processed row.

- **`text.py`**: Provides the `ImageProcessingPipeline` class for downloading images and extracting text using EasyOCR.
- **`feat.py`**: Provides utility functions for extracting and standardizing measurement units from text.

---

## Key Components

### Imported Functions and Classes

1. **`ImageProcessingPipeline` (from `text.py`)**:
   - A class designed to download an image from a URL and extract text using EasyOCR. It handles the entire process from fetching the image to OCR and returns the extracted text.

2. **`extract_values_with_units` (from `feat.py`)**:
   - A function that uses regular expressions to extract numerical values and corresponding units from a text string. It maps unit variants to standardized forms.

3. **`get_value_for_entity` (from `feat.py`)**:
   - A function that extracts unit-value pairs from the text based on the entity name (e.g., width, weight) and validates them using predefined mappings of valid units for each entity.

---

## Functions

### 1. `extract_values_with_units(text)` (from `feat.py`)
This function is used to extract numerical values and measurement units from the text, standardizing unit variations using regular expressions.

#### Parameters:
- **`text` (str)**: The input string containing values and measurement units.

#### Returns:
- A list of tuples where each tuple contains a numerical value and its corresponding standardized unit.

#### Example:
```python
text = "The width is 100cm and the weight is 2kg."
result = extract_values_with_units(text)
print(result)  # Output: [('100', 'centimetre'), ('2', 'kilogram')]
```

---

### 2. `get_value_for_entity(entity_name, text)` (from `feat.py`)
This function extracts valid unit-value pairs based on the specified entity (e.g., `'width'`, `'item_weight'`). It ensures that the extracted units are valid for the given entity by referencing a predefined mapping of valid units.

#### Parameters:
- **`entity_name` (str)**: The entity for which values need to be extracted (e.g., `'width'`, `'item_weight'`).
- **`text` (str)**: The input string containing values and units.

#### Returns:
- A list of valid unit-value pairs for the specified entity.

#### Example:
```python
text = "The width is 100cm and the weight is 2kg."
entity_name = "width"
result = get_value_for_entity(entity_name, text)
print(result)  # Output: ['100 centimetre']
```

---

### 3. `ImageProcessingPipeline` Class (from `text.py`)
This class is designed to download an image from a URL and extract text from the image using EasyOCR.

#### Attributes:
- **`image_url`**: The URL of the image to be processed.
- **`image`**: The downloaded image as a NumPy array (via OpenCV).
- **`extracted_text`**: The text extracted from the image using EasyOCR.

#### Methods:

1. **`__init__(self, image_url)`**: Initializes the class with the provided image URL.

```python
def __init__(self, image_url):
    self.image_url = image_url
    self.image = None
    self.extracted_text = None
```

2. **`download_image(self)`**: Downloads the image from the URL and converts it into a NumPy array using OpenCV.

```python
def download_image(self):
    response = requests.get(self.image_url)
    if response.status_code == 200:
        image_np = np.frombuffer(response.content, np.uint8)
        self.image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    else:
        raise Exception(f"Failed to download image from {self.image_url}, Status Code: {response.status_code}")
```

3. **`extract_text(self)`**: Extracts text from the image using EasyOCR, converting the image into RGB format before performing OCR.

```python
def extract_text(self):
    if self.image is None:
        raise FileNotFoundError("Image is not downloaded.")
    
    reader = easyocr.Reader(['en'])
    image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
    result = reader.readtext(image_rgb)
    self.extracted_text = ' '.join([text[1] for text in result])
```

4. **`get_extracted_text(self)`**: Returns the extracted text if OCR has been performed.

```python
def get_extracted_text(self):
    if self.extracted_text is None:
        raise RuntimeError("Text extraction not performed.")
    return self.extracted_text
```

---

### 4. `predictor(image_link, category_id, entity_name)`
This function orchestrates the process of downloading an image, extracting text using OCR, and extracting specific unit-value pairs based on the entity name. It uses the `ImageProcessingPipeline` class from `text.py` and the `get_value_for_entity` function from `feat.py`.

#### Parameters:
- **`image_link` (str)**: The URL of the image to process.
- **`category_id` (int)**: The category ID of the product.
- **`entity_name` (str)**: The entity (e.g., width, item weight) for which the value needs to be extracted.

#### Returns:
- The first matched unit-value pair for the entity, or `None` if no valid pairs are found.

#### Example:
```python
row = {
    'image_link': 'https://example.com/sample_image.jpg',
    'group_id': 123,
    'entity_name': 'width'
}
result = predictor(row['image_link'], row['group_id'], row['entity_name'])
print(result)  # Output: '100 centimetre'
```

---

### 5. `save_progress(df, output_filename)`
This function saves the intermediate progress to a CSV file, allowing the program to resume from the last processed row in case of an interruption.

#### Parameters:
- **`df` (DataFrame)**: The dataframe containing the processed rows so far.
- **`output_filename` (str)**: The filename to save the intermediate progress.

#### Example:
```python
processed_test = pd.DataFrame(columns=['index', 'prediction'])
save_progress(processed_test, './dataset/prediction_1.csv')
```

---

## Main Program

### Workflow
1. The program loads a dataset (`1.csv`) that contains rows with image URLs, group IDs, and entity names.
2. It checks if there's a previously saved output file (`prediction_1.csv`). If so, it resumes processing from the last processed row; otherwise, it starts from the beginning.
3. For each row, the program calls the `predictor` function to:
   - Download the image and extract text using OCR.
   - Extract unit-value pairs for the specified entity (e.g., width, item weight) from the text.
   - Store the index and predicted value in an output CSV file (`prediction_1.csv`).

4. The program saves progress after every 10 rows, or at the end of processing, to ensure minimal data loss in case of interruption.

5. **Output CSV Structure**:
   - **Index**: The index of the row from the original dataset.
   - **Prediction**: The extracted value for the entity (e.g., weight, width).

#### Example of Output CSV:
```csv
Index | Prediction
1     | 100 centimetre
2     | 200 grams
```

### Example of Main Execution:
```python
if __name__ == "__main__":
    DATASET_FOLDER = './dataset/'
    output_filename = os.path.join(DATASET_FOLDER, 'prediction_1.csv')

    test = pd.read_csv(os.path.join(DATASET_FOLDER, '1.csv'))

    # Check if there's a previously saved file to resume from
    if os.path.exists(output_filename):
        processed_test = pd.read_csv(output_filename)
        start_index = len(processed_test)
        test = test.iloc[start_index:]  # Skip already processed rows
        print(f"Resuming from row {start_index} in saved file.")
    else:
        processed_test = pd.DataFrame(columns=['index', 'prediction'])  # Initialize empty DataFrame
        start_index = 0

    for i, row in tqdm(test.iterrows(), total=len(test), desc="Processing rows"):
        prediction = predictor(row['image_link'], row['group_id'], row['entity_name'])
        new_row = pd.DataFrame({'index': [row['index']], 'prediction': [prediction]})
        processed_test = pd.concat([processed_test, new_row], ignore_index=True)

        if i % 10 == 0 or i == len(test) - 1:
            save_progress(processed_test, output_filename)

    # Final save
    save_progress(processed_test, output_filename)
    print("Processing complete.")
```

This ensures that predictions for various entities are saved, and the program can resume from where it left off in case of any interruption.
