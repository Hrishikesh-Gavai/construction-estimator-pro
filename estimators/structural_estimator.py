import joblib
import pandas as pd
import os
from config import MODELS_DIR
from estimators.cost_calculator import CostCalculator

class StructuralEstimator:
    def __init__(self):
        self.model_path = os.path.join(MODELS_DIR, 'structural_model.pkl')
        self.features_path = os.path.join(MODELS_DIR, 'structural_features.pkl')
        self.cost_calculator = CostCalculator()
        self.model = None
        self.feature_columns = None
        self.load_model()
    
    def load_model(self):
        """Load trained model"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.feature_columns = joblib.load(self.features_path)
                print("✅ Structural model loaded")
            else:
                print("ℹ️ No trained structural model found, using rule-based estimation")
        except Exception as e:
            print(f"❌ Error loading structural model: {e}")
    
    def estimate(self, dxf_features):
        """Generate detailed structural estimate with accurate quantities"""
        # Extract features
        concrete_volume = dxf_features.get('concrete_volume', 50)
        steel_kg = dxf_features.get('steel_quantity', 4000)
        formwork_area = dxf_features.get('formwork_area', 200)
        footing_count = dxf_features.get('footing_count', 10)
        column_count = dxf_features.get('column_count', 12)
        
        # Accurate material quantities based on construction standards
        quantities = {
            'Concrete (cubic meters)': round(concrete_volume, 2),
            'Steel (kg)': round(steel_kg, 2),
            'Cement (bags)': round(concrete_volume * 4.5, 2),  # 4.5 bags per m³
            'Aggregate (cubic meters)': round(concrete_volume * 0.9, 2),
            'Sand (cubic meters)': round(concrete_volume * 0.45, 2),
            'Binding Wire (kg)': round(steel_kg * 0.005, 2),
            'Formwork (sqm)': round(formwork_area, 2),
            'Columns (units)': column_count,
            'Footings (units)': footing_count
        }
        
        # Calculate costs using the cost calculator
        costs = self.cost_calculator.estimate_structural_costs(dxf_features)
        total_cost = sum(costs.values())
        
        # If ML model is available, use it for more accurate prediction
        if self.model and self.feature_columns:
            try:
                # Prepare features for model prediction
                feature_df = pd.DataFrame([dxf_features])[self.feature_columns]
                ml_prediction = self.model.predict(feature_df)[0]
                # Blend ML prediction with rule-based (70% ML, 30% rule-based)
                total_cost = (ml_prediction * 0.7) + (total_cost * 0.3)
            except Exception as e:
                print(f"⚠️ ML prediction failed, using rule-based: {e}")
        
        return {
            'plan_type': 'structural',
            'quantities': quantities,
            'costs': costs,
            'total_cost': total_cost,
            'features': dxf_features,
            'estimation_method': 'ML-enhanced' if self.model else 'Rule-based'
        }