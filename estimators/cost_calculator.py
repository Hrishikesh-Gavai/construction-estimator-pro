from parsers.rates_parser import parse_material_rates

class CostCalculator:
    def __init__(self):
        self.material_rates = parse_material_rates()
        print("🔍 LOADED RATES FOR DEBUGGING:")
        for material, rate in sorted(self.material_rates.items()):
            print(f"  {material}: ₹{rate}")
    
    def calculate_material_cost(self, material_type, quantity):
        """Calculate cost for a specific material"""
        rate = self.material_rates.get(material_type, 0)
        cost = quantity * rate
        return round(cost, 2)
    
    def estimate_architectural_costs(self, features):
        """Estimate costs for architectural project with accurate calculations"""
        area = features.get('total_area', 1000)  # in sq.ft
        rooms = features.get('num_rooms', 3)
        wall_length = features.get('wall_length', 100)
        openings = features.get('openings', 8)
        
        # Convert area to sq.m for material calculations
        area_sqm = area * 0.0929
        
        # Accurate material quantities based on construction standards
        quantities = {
            'cement_bags': max(200, area_sqm * 0.8),  # 0.8 bags per sq.m
            'bricks_pieces': max(5000, wall_length * 60),  # 60 bricks per meter wall
            'sand_cum': max(8, area_sqm * 0.03),  # 0.03 cum per sq.m
            'tiles_sqm': max(80, area_sqm * 1.1),  # 10% wastage
            'paint_liters': max(80, area_sqm * 0.15),  # 0.15 liters per sq.m
        }
        
        costs = {
            'Cement': self.calculate_material_cost('cement', quantities['cement_bags']),
            'Bricks': self.calculate_material_cost('bricks', quantities['bricks_pieces']),
            'Sand': self.calculate_material_cost('sand_river', quantities['sand_cum']),
            'Tiles': self.calculate_material_cost('tiles', quantities['tiles_sqm']),
            'Paint': self.calculate_material_cost('paint', quantities['paint_liters']),
            'Adhesive': self.calculate_material_cost('adhesive', area_sqm * 0.1),
            'Fixtures': openings * 3500,  # Doors/windows fixtures
            'Mason_Labor': self.calculate_material_cost('labor_mason', area_sqm * 0.8),
            'Helper_Labor': self.calculate_material_cost('labor_helper', area_sqm * 1.2),
            'Miscellaneous': area_sqm * 800
        }
        
        return {k: round(v, 2) for k, v in costs.items() if v > 0}
    
    def estimate_structural_costs(self, features):
        """Estimate costs for structural project with accurate calculations"""
        concrete_volume = features.get('concrete_volume', 0)  # in m³
        steel_kg = features.get('steel_quantity', 0)  # in kg
        formwork_area = features.get('formwork_area', 0)  # in m²
        footing_count = features.get('footing_count', 0)
        column_count = features.get('column_count', 0)
        
        # Accurate material quantities based on construction standards
        quantities = {
            'concrete_volume': concrete_volume,
            'steel_kg': steel_kg,
            'cement_bags': concrete_volume * 4.5,  # 4.5 bags per m³ concrete
            'aggregate_cum': concrete_volume * 0.9,  # 0.9 m³ aggregate per m³ concrete
            'sand_cum': concrete_volume * 0.45,  # 0.45 m³ sand per m³ concrete
            'binding_wire_kg': steel_kg * 0.005,  # 0.5% of steel weight
            'formwork_area': formwork_area
        }
        
        costs = {
            'Cement': self.calculate_material_cost('cement', quantities['cement_bags']),
            'Steel': self.calculate_material_cost('steel', quantities['steel_kg']),
            'Binding_Wire': self.calculate_material_cost('binding_wire', quantities['binding_wire_kg']),
            'Aggregate_10mm': self.calculate_material_cost('aggregate_10mm', quantities['aggregate_cum'] * 0.5),
            'Aggregate_20mm': self.calculate_material_cost('aggregate_20mm', quantities['aggregate_cum'] * 0.5),
            'Sand': self.calculate_material_cost('sand_msand', quantities['sand_cum']),
            'Formwork_Material': self.calculate_material_cost('shuttering_ply', formwork_area * 0.15),
            'Formwork_Labor': formwork_area * 450,  # Labor cost for formwork
            'Concreting_Labor': concrete_volume * 1200,
            'Steel_Fixing_Labor': self.calculate_material_cost('labor_steel_fixer', steel_kg * 0.015),
            'Carpenter_Labor': self.calculate_material_cost('labor_carpenter', formwork_area * 0.2),
            'Miscellaneous': concrete_volume * 500
        }
        
        return {k: round(v, 2) for k, v in costs.items() if v > 0}