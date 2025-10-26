import pandas as pd
import re
from config import RATES_FILE, DEFAULT_RATES

def parse_material_rates():
    """Parse material rates from Excel file with improved parsing"""
    try:
        df = pd.read_excel(RATES_FILE)
        rates = {}
        
        for _, row in df.iterrows():
            # Process material column (first column)
            if pd.notna(row.iloc[0]):
                material = str(row.iloc[0]).strip()
                if material and '₹' not in material and not any(keyword in material.lower() for keyword in ['mason', 'helper', 'labor', 'fixer', 'carpenter', 'electrician', 'plumber', 'painter', 'supervisor', 'waterman']):
                    # Extract rate from second column if available
                    if pd.notna(row.iloc[1]):
                        rate_text = str(row.iloc[1])
                        rate = extract_rate_from_text(rate_text)
                        if rate > 0:
                            rates[material.lower()] = rate
                    
                    # Also parse labor rates from third column
                    if len(row) > 2 and pd.notna(row.iloc[2]):
                        labor_text = str(row.iloc[2])
                        labor_rate = extract_rate_from_text(labor_text)
                        if labor_rate > 0:
                            labor_name = material.lower().replace(' ', '_')
                            rates[f"labor_{labor_name}"] = labor_rate
        
        # Enhanced categorization
        categorized_rates = categorize_rates(rates)
        
        # Add defaults for missing categories
        for category, default_rate in DEFAULT_RATES.items():
            if category not in categorized_rates:
                categorized_rates[category] = default_rate
                
        print(f"✅ Parsed {len(categorized_rates)} material rates")
        return categorized_rates
        
    except Exception as e:
        print(f"❌ Error parsing rates: {e}")
        return DEFAULT_RATES

def extract_rate_from_text(rate_text):
    """Extract numeric rate from text like '₹385 – ₹415'"""
    try:
        # Find all numbers in the text
        numbers = re.findall(r'₹?\s*(\d+(?:,\d+)?(?:\.\d+)?)', str(rate_text))
        if numbers:
            # Clean and convert to float
            values = [float(num.replace(',', '')) for num in numbers if num]
            # Return average for ranges, or single value
            return sum(values) / len(values)
        return 0
    except:
        return 0

def categorize_rates(rates_dict):
    """Categorize materials into standard categories"""
    categorized = {}
    
    material_mapping = {
        # Cement & Binders
        'cement': ['cement', 'opc', 'ppc'],
        'adhesive': ['adhesive', 'grout'],
        'binding_wire': ['binding wire'],
        
        # Bricks & Blocks
        'bricks': ['bricks', 'fly ash', 'clay'],
        
        # Aggregates & Sand
        'aggregate_10mm': ['coarse aggregate 10mm', 'aggregate 10mm'],
        'aggregate_20mm': ['coarse aggregate 20mm', 'aggregate 20mm'],
        'sand_river': ['sand river', 'river sand'],
        'sand_msand': ['sand m-sand', 'm-sand', 'msand'],
        
        # Tiles & Finishes
        'tiles': ['ceramic tiles', 'tiles'],
        'curing_compound': ['curing compounds'],
        'waterproofing': ['waterproofing chemicals'],
        
        # Structural
        'shuttering_ply': ['shuttering ply'],
        
        # Labor
        'labor_mason': ['mason'],
        'labor_helper': ['helper', 'labourer'],
        'labor_steel_fixer': ['steel fixer', 'bar bender'],
        'labor_carpenter': ['shuttering carpenter', 'carpenter'],
        'labor_plumber': ['plumber'],
        'labor_painter': ['painter']
    }
    
    for material, rate in rates_dict.items():
        for category, keywords in material_mapping.items():
            if any(keyword in material for keyword in keywords):
                categorized[category] = rate
                break
        else:
            # If no category found, keep the original name
            categorized[material] = rate
    
    return categorized

def get_material_rates():
    """Get current material rates"""
    return parse_material_rates()