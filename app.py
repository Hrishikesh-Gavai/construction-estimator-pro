from flask import Flask, request, render_template, jsonify
import os
import time
from config import DATA_DIR
from parsers.dxf_parser import DXFAnalyzer
from estimators.architectural_estimator import ArchitecturalEstimator
from estimators.structural_estimator import StructuralEstimator

app = Flask(__name__)

dxf_analyzer = DXFAnalyzer()
arch_estimator = ArchitecturalEstimator()
struct_estimator = StructuralEstimator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('result.html', error="No file uploaded")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('result.html', error="No file selected")
    
    if not file.filename.lower().endswith('.dxf'):
        return render_template('result.html', error="Please upload a DXF file")
    
    # Save uploaded file
    upload_path = os.path.join(DATA_DIR, 'uploads', file.filename)
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    file.save(upload_path)
    
    try:
        print(f"📁 Processing file: {file.filename}")
        print(f"📁 File size: {os.path.getsize(upload_path)} bytes")
        
        # Detect plan type and analyze
        plan_type = dxf_analyzer.detect_plan_type(upload_path)
        print(f"📋 Detected plan type: {plan_type}")
        
        if plan_type == 'architectural':
            features = dxf_analyzer.analyze_architectural(upload_path)
            estimate = arch_estimator.estimate(features)
        else:
            features = dxf_analyzer.analyze_structural(upload_path)
            estimate = struct_estimator.estimate(features)
        
        estimate['file_name'] = file.filename
        print(f"💰 Final estimate: ₹{estimate['total_cost']:,.2f}")
        
        return render_template('result.html', estimate=estimate, error=None)
        
    except Exception as e:
        print(f"❌ Error processing file: {str(e)}")
        return render_template('result.html', error=f"Error processing file: {str(e)}")

@app.route('/api/process', methods=['POST'])
def api_process():
    """API endpoint for AJAX processing"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    # Process file and return JSON response
    
    return jsonify({'status': 'processing', 'progress': 50})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')