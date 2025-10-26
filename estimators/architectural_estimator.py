import joblib
import pandas as pd
import os
from config import MODELS_DIR
from estimators.cost_calculator import CostCalculator

class ArchitecturalEstimator:
    def __init__(self):
        self.model_path = os.path.join(MODELS_DIR, 'architectural_model.pkl')
        self.features_path = os.path.join(MODELS_DIR, 'architectural_features.pkl')
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
                print("✅ Architectural model loaded")
            else:
                print("ℹ️ No trained architectural model found, using rule-based estimation")
        except Exception as e:
            print(f"❌ Error loading architectural model: {e}")
    
    def estimate(self, dxf_features):
        """Generate detailed architectural estimate with accurate quantities"""
        # Extract features
        area = dxf_features.get('total_area', 1000)  # sq.ft
        rooms = dxf_features.get('num_rooms', 3)
        wall_length = dxf_features.get('wall_length', 100)
        openings = dxf_features.get('openings', 8)
        
        # Convert area to sq.m for material calculations
        area_sqm = area * 0.0929
        
        # Accurate material quantities
        quantities = {
            'Cement (bags)': max(200, round(area_sqm * 0.8, 2)),
            'Bricks (pieces)': max(5000, round(wall_length * 60, 2)),
            'Sand (cubic meters)': max(8, round(area_sqm * 0.03, 2)),
            'Tiles (sqm)': max(80, round(area_sqm * 1.1, 2)),
            'Paint (liters)': max(80, round(area_sqm * 0.15, 2)),
            'Doors (units)': max(3, rooms * 2),
            'Windows (units)': max(4, rooms * 3)
        }
        
        # Calculate costs
        costs = self.cost_calculator.estimate_architectural_costs(dxf_features)
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
            'plan_type': 'architectural',
            'quantities': quantities,
            'costs': costs,
            'total_cost': total_cost,
            'features': dxf_features,
            'estimation_method': 'ML-enhanced' if self.model else 'Rule-based'
        }