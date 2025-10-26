import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from config import TRAINING_DATA_FILE, MODELS_DIR

def train_architectural_model(df):
    """Train model for architectural estimates"""
    # Filter architectural data
    arch_data = df[df['file_type'] == 'architectural']
    
    if len(arch_data) < 3:
        print("❌ Not enough architectural data for training")
        return None
    
    # Feature columns
    feature_cols = ['total_area', 'num_rooms', 'wall_length', 'perimeter', 'complexity', 'openings']
    target_cols = ['total_cost']
    
    # Prepare data
    X = arch_data[feature_cols]
    y = arch_data[target_cols]
    
    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train.values.ravel())
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"🏠 Architectural Model - MAE: ₹{mae:,.2f}, R²: {r2:.3f}")
    print(f"   Features: {feature_cols}")
    print(f"   Training samples: {len(X_train)}, Test samples: {len(X_test)}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(f"   Feature importance:\n{feature_importance}")
    
    # Save model
    joblib.dump(model, os.path.join(MODELS_DIR, 'architectural_model.pkl'))
    joblib.dump(feature_cols, os.path.join(MODELS_DIR, 'architectural_features.pkl'))
    
    return model

def train_structural_model(df):
    """Train model for structural estimates"""
    # Filter structural data
    struct_data = df[df['file_type'] == 'structural']
    
    if len(struct_data) < 3:
        print("❌ Not enough structural data for training")
        return None
    
    # Feature columns
    feature_cols = ['concrete_volume', 'steel_quantity', 'formwork_area', 'footing_count', 
                   'column_count', 'beam_length', 'slab_area', 'structure_complexity']
    target_cols = ['total_cost']
    
    # Prepare data
    X = struct_data[feature_cols]
    y = struct_data[target_cols]
    
    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train.values.ravel())
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"🏗️ Structural Model - MAE: ₹{mae:,.2f}, R²: {r2:.3f}")
    print(f"   Features: {feature_cols}")
    print(f"   Training samples: {len(X_train)}, Test samples: {len(X_test)}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(f"   Feature importance:\n{feature_importance}")
    
    # Save model
    joblib.dump(model, os.path.join(MODELS_DIR, 'structural_model.pkl'))
    joblib.dump(feature_cols, os.path.join(MODELS_DIR, 'structural_features.pkl'))
    
    return model

def train_models():
    """Train both architectural and structural models"""
    if not os.path.exists(TRAINING_DATA_FILE):
        print("❌ Training data not found. Run data_preparer.py first.")
        return
    
    df = pd.read_csv(TRAINING_DATA_FILE)
    print(f"📊 Training models with {len(df)} records")
    print(f"   Architectural: {len(df[df['file_type'] == 'architectural'])}")
    print(f"   Structural: {len(df[df['file_type'] == 'structural'])}")
    
    arch_model = train_architectural_model(df)
    struct_model = train_structural_model(df)
    
    if arch_model or struct_model:
        print("🎉 Model training completed!")
        print("📁 Models saved in:", MODELS_DIR)
    else:
        print("⚠️ Models could not be trained due to insufficient data")

if __name__ == '__main__':
    train_models()