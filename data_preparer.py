import pandas as pd
import os
from config import DATA_DIR, TRAINING_DATA_FILE
from parsers.dxf_parser import DXFAnalyzer
from estimators.cost_calculator import CostCalculator

def prepare_training_data():
    """Prepare training data from all available DXF files"""
    dxf_analyzer = DXFAnalyzer()
    cost_calculator = CostCalculator()
    
    records = []
    
    # Process architectural files
    arch_folder = os.path.join(DATA_DIR, 'raw', 'architectural')
    if os.path.exists(arch_folder):
        for dxf_file in os.listdir(arch_folder):
            if dxf_file.endswith('.dxf'):
                file_path = os.path.join(arch_folder, dxf_file)
                try:
                    features = dxf_analyzer.analyze_architectural(file_path)
                    costs = cost_calculator.estimate_architectural_costs(features)
                    
                    record = features.copy()
                    record.update({
                        'file_type': 'architectural',
                        'filename': dxf_file,
                        'total_cost': sum(costs.values()),
                        **{f'cost_{k.lower()}': v for k, v in costs.items()}
                    })
                    records.append(record)
                    print(f"✅ Processed architectural: {dxf_file}")
                except Exception as e:
                    print(f"❌ Error processing {dxf_file}: {e}")
    
    # Process structural files
    struct_folder = os.path.join(DATA_DIR, 'raw', 'structural')
    if os.path.exists(struct_folder):
        for project_folder in os.listdir(struct_folder):
            project_path = os.path.join(struct_folder, project_folder)
            if os.path.isdir(project_path):
                # Process each DXF in the project folder
                for dxf_file in os.listdir(project_path):
                    if dxf_file.endswith('.dxf'):
                        file_path = os.path.join(project_path, dxf_file)
                        try:
                            features = dxf_analyzer.analyze_structural(file_path)
                            costs = cost_calculator.estimate_structural_costs(features)
                            
                            record = features.copy()
                            record.update({
                                'file_type': 'structural',
                                'project_id': project_folder,
                                'filename': dxf_file,
                                'total_cost': sum(costs.values()),
                                **{f'cost_{k.lower()}': v for k, v in costs.items()}
                            })
                            records.append(record)
                            print(f"✅ Processed structural: {project_folder}/{dxf_file}")
                        except Exception as e:
                            print(f"❌ Error processing {project_folder}/{dxf_file}: {e}")
    
    if records:
        df = pd.DataFrame(records)
        
        # Add some realistic sample data if we don't have enough DXF files
        if len(df) < 10:
            df = add_sample_data(df)
        
        df.to_csv(TRAINING_DATA_FILE, index=False)
        print(f"🎉 Training data prepared: {len(records)} records saved to {TRAINING_DATA_FILE}")
        print(f"📊 Data summary:\n{df[['file_type', 'total_cost']].describe()}")
        return df
    else:
        print("❌ No DXF files found for training data")
        return add_sample_data(pd.DataFrame())  # Return sample data

def add_sample_data(df):
    """Add realistic sample data for training"""
    sample_architectural = [
        {
            'file_type': 'architectural', 'total_area': 1200, 'num_rooms': 4, 
            'wall_length': 120, 'perimeter': 100, 'complexity': 5.5, 'openings': 12,
            'total_cost': 2850000, 'filename': 'sample_house_1.dxf'
        },
        {
            'file_type': 'architectural', 'total_area': 800, 'num_rooms': 3, 
            'wall_length': 90, 'perimeter': 80, 'complexity': 4.2, 'openings': 8,
            'total_cost': 1950000, 'filename': 'sample_house_2.dxf'
        },
        {
            'file_type': 'architectural', 'total_area': 2000, 'num_rooms': 5, 
            'wall_length': 180, 'perimeter': 150, 'complexity': 7.8, 'openings': 16,
            'total_cost': 4200000, 'filename': 'sample_house_3.dxf'
        }
    ]
    
    sample_structural = [
        {
            'file_type': 'structural', 'concrete_volume': 65, 'steel_quantity': 5200,
            'formwork_area': 350, 'footing_count': 12, 'column_count': 15, 
            'beam_length': 95, 'slab_area': 120, 'structure_complexity': 6.2,
            'total_cost': 1850000, 'filename': 'sample_struct_1.dxf'
        },
        {
            'file_type': 'structural', 'concrete_volume': 45, 'steel_quantity': 3600,
            'formwork_area': 250, 'footing_count': 8, 'column_count': 10, 
            'beam_length': 70, 'slab_area': 85, 'structure_complexity': 4.8,
            'total_cost': 1250000, 'filename': 'sample_struct_2.dxf'
        },
        {
            'file_type': 'structural', 'concrete_volume': 95, 'steel_quantity': 7600,
            'formwork_area': 520, 'footing_count': 18, 'column_count': 22, 
            'beam_length': 130, 'slab_area': 180, 'structure_complexity': 8.1,
            'total_cost': 2850000, 'filename': 'sample_struct_3.dxf'
        }
    ]
    
    sample_df = pd.DataFrame(sample_architectural + sample_structural)
    
    if not df.empty:
        return pd.concat([df, sample_df], ignore_index=True)
    else:
        return sample_df

if __name__ == '__main__':
    prepare_training_data()