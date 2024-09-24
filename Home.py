import streamlit as st

st.set_page_config(
    page_title="CSV and Image Text Extraction App",
    layout="centered",
)

st.title("Welcome to the CSV Prediction and Image Text Extraction App")
st.sidebar.success("Select a page above.")

st.write("""### Project Overview: Image-to-Text Extraction and Unit-Value Prediction

**Developed by:**
- **Pratham Bisht** [GitHub](https://github.com/Pratham216)
- **Keshav Kushwaha** [GitHub](https://github.com/offline-keshav)
- **Ritik Gupta** [GitHub](https://github.com/guptaritik17)

Welcome to **Heavy Coders'** image processing project! This application leverages **Optical Character Recognition (OCR)** to extract text from product images and automatically identify key unit-value pairs such as width, weight, and more.

### Key Features:
- **Image Processing Pipeline:** Downloads images from URLs and uses EasyOCR to extract text.
- **Unit Extraction:** Detects and standardizes units (e.g., cm, kg) from extracted text.
- **Entity-Specific Prediction:** Identifies relevant unit-value pairs (e.g., "100 cm width").
- **Progress Saving:** Ensures intermediate results are saved, allowing the program to resume if interrupted.

Upload product images and let the model predict dimensions and weights with ease!
""")