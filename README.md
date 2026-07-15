# Digitup Technical Test – Intelligent Document Analysis  
**Candidate: Dalia Manel Akkouchi**

This repository contains an intelligent document analysis application designed for administrative documents.  
It integrates OCR (Arabic/French), signature detection, ID photo detection, checkbox analysis, multimodal fusion, and a demo interface built with Streamlit.

---

![Aperçu du projet](ocr.png)


##  Main Features

###  1. Multimodal OCR (EasyOCR)
- Recognition of printed and handwritten text.
- Supports **Arabic + French**.
- Automatic preprocessing (binarization, noise reduction, light normalization).
- Outputs extracted text + average confidence score.

---

### 2. Signature Analysis
- Automatic detection of the signature zone (heuristic: bottom 30% of the page).
- Ink detection via adaptive thresholding.
- Computes an ink-based score for basic fraud detection.

---

###  3. ID Photo Detection
- Detects a probable facial region.
- Based on Haar Cascades or heuristic face detection.
- Returns: `photo_found = True / False`.

---

###  4. Checkbox Recognition
- Detects square checkbox regions.
- Computes `fill_ratio` (percentage of ink).
- Returns each checkbox with:
  - position  
  - fill ratio  

---

###  5. Multimodal Fusion
A dedicated module merges all results:
- OCR text + confidence  
- Signature presence + ink score  
- ID photo detection  
- Checkboxes + fill ratios  
- **Global reliability score**

---

## Project Structure

```
digitup-test-manel/
│
├── app/
│ ├── app.py # Main Streamlit interface
│ ├── ocr.py # EasyOCR module
│ ├── signature.py # Signature analysis
│ ├── face_detector.py # ID photo detection
│ ├── checkbox.py # Checkbox detection
│ └── fusion.py # Multimodal fusion logic
│
├── src/
│ └── pipeline.py # Global processing pipeline
│
├── notebooks/
│ └── digitup-experiments-ipynb # Research & experiments
│
├── requirements.txt
└── README.md
```


---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Dalia-Manel/digitup-test-manel.git
cd digitup-test-manel
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note:** PDF support relies on **Poppler** (used by `pdf2image`).
> - Ubuntu/Debian: `sudo apt-get install poppler-utils`
> - Windows: download Poppler and add its `bin/` folder to the PATH.

(Optional) Install PyTorch if GPU is available:
```
pip install torch
```

Run the Application
```
streamlit run app/app.py
```

This launches the full demo interface.

### Technical Architecture

Fully modular: each component can be upgraded independently.

Clear pipeline structure (pipeline.py).

Easy extensibility:

Replace EasyOCR with a Transformer-based OCR

Add forgery detection modules

Connect to a database or online API

Improve signature localization with segmentation models (U-Net)

### Future Improvements

Fine-tuning EasyOCR on Algerian administrative documents

Arabic post-processing using a language model

Texture-based forgery detection (Siamese networks)

Better signature segmentation with deep learning

Synthetic data generation for training/validation

---

## Author
**Dalia Manel Akkouchi**  
Master's Graduate in Software Engineering and Information Processing  

