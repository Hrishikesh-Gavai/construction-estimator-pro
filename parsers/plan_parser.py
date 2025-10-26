import pandas as pd
from config import ARCHITECTURAL_PLAN_FILE, STRUCTURAL_PLAN_FILE

def parse_architectural_plan():
    """Parse architectural plan activities and materials"""
    activities = {}
    try:
        if os.path.exists(ARCHITECTURAL_PLAN_FILE):
            df = pd.read_excel(ARCHITECTURAL_PLAN_FILE)
            current_activity = ""
            
            for _, row in df.iterrows():
                if pd.notna(row.iloc[0]) and str(row.iloc[0]).replace('.0', '').isdigit():
                    current_activity = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
                    activities[current_activity] = []
                elif pd.notna(row.iloc[2]) and current_activity:
                    material = str(row.iloc[2]).strip()
                    if material and material not in activities[current_activity]:
                        activities[current_activity].append(material)
            
            return activities
        else:
            print("ℹ️ Architectural plan file not found, using default activities")
            return get_default_architectural_activities()
    except Exception as e:
        print(f"❌ Error parsing architectural plan: {e}")
        return get_default_architectural_activities()

def parse_structural_plan():
    """Parse structural plan activities and materials"""
    activities = {}
    try:
        if os.path.exists(STRUCTURAL_PLAN_FILE):
            df = pd.read_excel(STRUCTURAL_PLAN_FILE)
            current_section = ""
            current_activity = ""
            
            for _, row in df.iterrows():
                cell_value = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                
                if any(keyword in cell_value.lower() for keyword in ['drawing', 'plan', 'floor']):
                    current_section = cell_value
                elif cell_value.replace('.0', '').isdigit():
                    activity_name = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
                    current_activity = f"{current_section} - {activity_name}"
                    activities[current_activity] = []
                elif pd.notna(row.iloc[2]) and current_activity:
                    material = str(row.iloc[2]).strip()
                    if material and material not in activities[current_activity]:
                        activities[current_activity].append(material)
            
            return activities
        else:
            print("ℹ️ Structural plan file not found, using default activities")
            return get_default_structural_activities()
    except Exception as e:
        print(f"❌ Error parsing structural plan: {e}")
        return get_default_structural_activities()

def get_default_architectural_activities():
    """Return default architectural activities"""
    return {
        "Earthwork": ["Excavation", "Backfilling"],
        "Foundation": ["PCC", "Footings"],
        "Superstructure": ["Brickwork", "Columns", "Beams"],
        "Finishing": ["Plastering", "Painting", "Flooring"]
    }

def get_default_structural_activities():
    """Return default structural activities"""
    return {
        "Foundation Work": ["Excavation", "PCC", "Footing RCC"],
        "Column Work": ["Column RCC", "Reinforcement"],
        "Beam Work": ["Beam RCC", "Formwork"],
        "Slab Work": ["Slab RCC", "Shuttering"]
    }