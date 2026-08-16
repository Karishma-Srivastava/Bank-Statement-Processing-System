# Bank Statement Processing & Classification System

A Python-based bank statement processing system that extracts account and transaction information from both text-based and scanned/image-based PDF bank statements, validates the extracted data, classifies transactions using both rule-based and traditional machine learning approaches, and exports the results to CSV and Excel.

## Features

- Supports text-based PDF bank statements
- Supports scanned/image-based PDF statements using OCR
- Automatically detects PDF type
- Extracts account information:
  - Account holder
  - Account number
  - IFSC
  - Branch
- Extracts transaction information:
  - Date
  - Description
  - Debit
  - Credit
  - Balance
- Normalizes bank-specific transaction headers into a common schema
- Supports different transaction column naming conventions
- Coordinate-based extraction for structured text PDFs
- OCR-based extraction for scanned PDFs
- Transaction validation
- Balance consistency validation
- Transaction direction validation
- Transaction categorization using:
  - Rule-based keyword classification
  - Traditional ML classification using TF-IDF + Logistic Regression
- Classification comparison between rule-based and ML approaches
- Streamlit web interface
- CSV export
- Excel export
- Error handling for failed document processing

## Architecture

```text
                    Bank Statement PDF
                            |
                            v
                    PDF Type Detection
                       /           \
                      /             \
                     v               v
              Text-based PDF     Scanned PDF
                     |               |
                     v               v
            Text/Coordinate       OCR using
               Extraction         Tesseract
                     \               /
                      \             /
                       v           v
                    Transaction Data
                            |
                            v
                    Header Normalization
                            |
                            v
                       Validation
                            |
                            v
                 Transaction Classification
                       /             \
                      /               \
                     v                 v
              Rule-Based          Traditional ML
              Classification       TF-IDF + Logistic
                                      Regression
                     \                 /
                      \               /
                       v             v
                       Classification
                         Results
                            |
                    -------------------
                    |                 |
                    v                 v
                  CSV              Excel
                    \                 /
                     \               /
                      v             v
                       Streamlit UI




------------    Project Structure --------------

Bank_statement_project/
│
├── app.py
├── requirements.txt
├── create_bank_b_pdf.py
│
├── data/
│   └── samples/
│       ├── sample_bank_statement_text.pdf
│       ├── sample_bank_statement_scanned.pdf
│       └── bank_b_statement.pdf
│
├── src/
│   ├── __init__.py
│   ├── classifier.py
│   ├── coordinate_extractor.py
│   ├── exporter.py
│   ├── extractor.py
│   ├── normalizer.py
│   ├── pdf_detector.py
│   ├── pipeline.py
│   └── validation.py
│
└── tests/
    ├── test.py
    ├── test_bank_variation.py
    ├── test_classifier.py
    ├── test_export.py
    ├── test_normalizer.py
    ├── test_pipeline.py
    ├── test_table.py
    └── test_validation.py





Technology Stack
Programming
Python
PDF Processing
PyMuPDF
OCR
Tesseract OCR
pytesseract
PIL/Pillow
Data Processing
pandas
NumPy
Machine Learning
scikit-learn
TF-IDF Vectorization
Logistic Regression
Application
Streamlit
Export
CSV
Excel
Classification Approaches
1. Rule-Based Classification

The first approach uses deterministic keyword-based rules.

Example:

"SWIGGY FOOD ORDER"
        ↓
Keyword match: "swiggy"
        ↓
food

The rule-based approach is:

Simple
Deterministic
Explainable
Fast
2. Traditional Machine Learning

The second approach uses:

Transaction Description
        ↓
TF-IDF Vectorization
        ↓
Logistic Regression
        ↓
Transaction Category

The ML model is trained using labeled transaction descriptions.

Example:

"online marketplace payment"
        ↓
TF-IDF
        ↓
Logistic Regression
        ↓
shopping

The ML approach can identify patterns that may not exactly match the predefined rule keywords.

ML Evaluation

The prototype ML classifier was evaluated using a stratified train/test split on a small synthetic labeled dataset.

Example evaluation:

Accuracy  : 0.80
Precision : 0.8667
Recall    : 0.80
F1-score  : 0.80

These metrics are based on the synthetic development dataset and should not be interpreted as production performance. A production system would require a larger and more representative labeled transaction dataset.

Validation

The system performs multiple validation checks.

Value Validation

Checks whether transaction amounts are valid numeric values.

Balance Validation

For a transaction:

Expected Balance =
Previous Balance - Debit + Credit

The calculated balance is compared with the extracted balance.

Transaction Direction Validation

Checks whether the transaction can be identified as a debit or credit based on the extracted data.

Transactions that cannot be confidently classified can be marked for review.

PDF Processing
Text-Based PDFs

For text-based PDFs, the system can use PDF text/word coordinates to reconstruct transaction rows.

Coordinate-based extraction helps determine which amount belongs to:

Debit | Credit | Balance

based on the horizontal position of the value.

Scanned PDFs

For image-based PDFs:

PDF
 ↓
Render page as image
 ↓
OCR
 ↓
Extract text
 ↓
Parse transactions

Tesseract OCR is used to extract text from scanned pages.

Streamlit Application

Run the application using:

streamlit run app.py

The application allows the user to:

Upload a bank statement PDF
Process the statement
View account information
View detected PDF type
View extracted transactions
View validation results
Compare rule-based and ML classifications
Download CSV output
Download Excel output
Installation

Clone the repository:

git clone https://github.com/Karishma-Srivastava/Bank-Statement-Processing-System.git
cd Bank-Statement-Processing-System

Create a virtual environment:

Windows
python -m venv venv
venv\Scripts\activate
Linux/macOS
python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
OCR Requirement

Scanned PDF processing requires Tesseract OCR to be installed on the system.

After installing Tesseract, make sure the tesseract executable is available to the application.

Verify the installation with:

tesseract --version
Running the Pipeline

The processing pipeline can also be tested directly.

Example:

PYTHONPATH=. python tests/test_pipeline.py "data/samples/sample_bank_statement_text.pdf"

For a scanned statement:

PYTHONPATH=. python tests/test_pipeline.py "data/samples/sample_bank_statement_scanned.pdf"
Running the Application
streamlit run app.py

Then upload a PDF through the Streamlit interface.

Sample Data

The repository contains sample bank statements for development and testing.

The sample statements are synthetic/development data and are not intended to represent real customer banking information.

A real HDFC bank statement was also used during development/testing to identify OCR and layout-related extraction challenges.

Limitations

The current prototype has some limitations:

OCR accuracy depends on scan quality and document layout.
Different banks may use substantially different statement layouts.
The traditional ML model is trained on a small synthetic dataset.
ML performance may change on unseen real-world transaction descriptions.
Production deployment would require a larger representative labeled dataset.
More advanced table detection and bank-specific parsing could improve extraction accuracy for complex scanned statements.
Future Improvements

Possible improvements include:

Larger real-world labeled transaction dataset
More robust ML model evaluation
Additional classification models
Confidence scores for ML predictions
Better OCR preprocessing
Advanced table detection
Bank-specific parsing configurations
Improved automated test coverage
Cloud deployment
Logging and monitoring
Model versioning and retraining pipeline
Design Principles

The project separates major responsibilities into independent modules:

PDF detection
Extraction
Coordinate-based parsing
Header normalization
Validation
Classification
Pipeline orchestration
Export


Author

Karishma Srivastava
