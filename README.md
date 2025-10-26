# Construction Estimator Pro

## 📖 Overview

Construction Estimator Pro is a Flask-based application that analyzes DXF architectural and structural plans to generate detailed construction cost estimates and material quantities. It combines **rule-based calculations** with **machine learning models** for improved accuracy.

## ⚙️ Features

* Upload and process DXF plans (architectural & structural).
* Automatic plan type detection and feature extraction.
* Material quantity and cost estimation.
* Rule-based fallback when ML models are unavailable.
* Training pipeline for ML models to improve accuracy.
* Web interface with charts and downloadable reports.

## 📽️ Demo



## 📂 Project Structure

```
├── app.py                # Flask main application
├── config.py             # Configuration & default rates
├── data_preparer.py      # Generate training datasets from DXF
├── train_models.py       # Train ML models
├── parsers/              # DXF, plan, and rate parsers
├── estimators/           # Estimation and cost calculation modules
├── templates/            # HTML templates for web interface
├── data/                 # Data storage (uploads, rates, training data)
└── models/               # Saved ML models
```

## 🚀 Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/construction-estimator-pro.git
cd construction-estimator-pro
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Prepare Data

* Place **DXF files** inside `data/raw/architectural` or `data/raw/structural`.
* Place **Rates.xlsx** inside `data/rates/`.
* Place **Architectural Plan.xlsx** and **Structural Plan.xlsx** inside `data/plans/`.

### 4. Generate Training Data

```bash
python data_preparer.py
```

### 5. Train Models

```bash
python train_models.py
```

### 6. Run Application

```bash
python app.py
```

Access the app at: `http://127.0.0.1:5000`

## 📊 Workflow

1. Upload DXF file through web UI.
2. Plan analyzed → features extracted.
3. Estimation performed (rule-based + ML + rates).
4. Results displayed with charts and cost breakdown.
5. Option to export/download report.

## 🛠️ Tech Stack

* **Backend**: Flask, Python
* **ML Models**: scikit-learn (Random Forest)
* **Data Processing**: pandas
* **Frontend**: HTML

## ⌚ Work In Progress...
