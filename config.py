import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# File paths
RATES_FILE = os.path.join(DATA_DIR, 'rates', 'Rates.xlsx')
TRAINING_DATA_FILE = os.path.join(DATA_DIR, 'training_data', 'construction_data.csv')

# Realistic default rates based on your Excel
DEFAULT_RATES = {
    'cement': 400, 'bricks': 10, 'steel': 80, 'sand_river': 7500, 'sand_msand': 5250,
    'aggregate_10mm': 3000, 'aggregate_20mm': 2800, 'tiles': 60, 'paint': 300,
    'binding_wire': 90, 'shuttering_ply': 1250, 'labor_mason': 800, 'labor_helper': 575,
    'labor_steel_fixer': 850, 'labor_carpenter': 850, 'labor_plumber': 825,
    'adhesive': 525, 'curing_compound': 65, 'waterproofing': 140
}

# Create directories on import
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, 'training_data'), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, 'uploads'), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, 'raw', 'architectural'), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, 'raw', 'structural'), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, 'rates'), exist_ok=True)