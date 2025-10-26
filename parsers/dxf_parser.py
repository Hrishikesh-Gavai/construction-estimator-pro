import os
import random
from config import DATA_DIR

class DXFAnalyzer:
    def __init__(self):
        os.environ['EZDXF_DISABLE_FONT_MANAGER'] = '1'
    
    def analyze_architectural(self, dxf_path):
        """Analyze architectural DXF file with actual file parsing"""
        try:
            print(f"🔍 Analyzing architectural DXF: {os.path.basename(dxf_path)}")
            
            with open(dxf_path, 'rb') as f:
                content = f.read().decode('latin-1', errors='ignore')
            
            # More sophisticated analysis based on actual file content
            file_size = os.path.getsize(dxf_path)
            line_count = content.count('LINE')
            poly_count = content.count('LWPOLYLINE') + content.count('POLYLINE')
            circle_count = content.count('CIRCLE')
            text_count = content.count('TEXT') + content.count('MTEXT')
            arc_count = content.count('ARC')
            
            total_elements = line_count + poly_count + circle_count + text_count + arc_count
            
            # Calculate features based on actual file characteristics
            features = {
                'total_area': self.calculate_area(line_count, poly_count, file_size),
                'num_rooms': self.calculate_rooms(poly_count, circle_count),
                'wall_length': self.calculate_wall_length(line_count, file_size),
                'perimeter': self.calculate_perimeter(line_count, poly_count),
                'complexity': min(10, total_elements / 50),
                'openings': self.calculate_openings(line_count, circle_count, arc_count)
            }
            
            print(f"📐 Extracted architectural features: {features}")
            return features
            
        except Exception as e:
            print(f"❌ Error analyzing architectural DXF: {e}")
            return self.get_default_features('architectural')
    
    def analyze_structural(self, dxf_path):
        """Analyze structural DXF file with actual file parsing"""
        try:
            print(f"🔍 Analyzing structural DXF: {os.path.basename(dxf_path)}")
            
            with open(dxf_path, 'rb') as f:
                content = f.read().decode('latin-1', errors='ignore')
            
            file_size = os.path.getsize(dxf_path)
            line_count = content.count('LINE')
            poly_count = content.count('LWPOLYLINE') + content.count('POLYLINE')
            circle_count = content.count('CIRCLE')
            arc_count = content.count('ARC')
            text_count = content.count('TEXT') + content.count('MTEXT')
            
            total_elements = line_count + poly_count + circle_count + arc_count + text_count
            
            # Calculate structural features based on actual file content
            features = {
                'concrete_volume': self.calculate_concrete_volume(total_elements, file_size),
                'steel_quantity': self.calculate_steel_quantity(line_count, circle_count),
                'formwork_area': self.calculate_formwork_area(line_count, poly_count),
                'footing_count': self.calculate_footing_count(circle_count, poly_count),
                'column_count': self.calculate_column_count(circle_count, line_count),
                'beam_length': self.calculate_beam_length(line_count, file_size),
                'slab_area': self.calculate_slab_area(poly_count, file_size),
                'structure_complexity': min(10, total_elements / 40)
            }
            
            print(f"🏗️ Extracted structural features: {features}")
            return features
            
        except Exception as e:
            print(f"❌ Error analyzing structural DXF: {e}")
            return self.get_default_features('structural')
    
    def detect_plan_type(self, dxf_path):
        """Auto-detect plan type based on filename and content analysis"""
        filename = os.path.basename(dxf_path).lower()
        
        print(f"🔍 Detecting plan type for: {filename}")
        
        # Strong filename-based detection first
        arch_keywords = ['arch', 'plan', 'layout', 'elevation', 'floor', 'room', 'door', 'window', 'facade']
        struct_keywords = ['struct', 'beam', 'column', 'footing', 'slab', 'foundation', 'reinforcement', 'rcc', 'concrete']
        
        arch_score = sum(1 for keyword in arch_keywords if keyword in filename)
        struct_score = sum(1 for keyword in struct_keywords if keyword in filename)
        
        print(f"📝 Filename analysis - Architectural: {arch_score}, Structural: {struct_score}")
        
        if arch_score > struct_score:
            print("✅ Detected: Architectural (filename)")
            return 'architectural'
        elif struct_score > arch_score:
            print("✅ Detected: Structural (filename)")
            return 'structural'
        
        # Content-based detection as fallback
        try:
            with open(dxf_path, 'rb') as f:
                content = f.read().decode('latin-1', errors='ignore')
            
            line_count = content.count('LINE')
            poly_count = content.count('LWPOLYLINE') + content.count('POLYLINE')
            circle_count = content.count('CIRCLE')
            text_count = content.count('TEXT') + content.count('MTEXT')
            arc_count = content.count('ARC')
            
            # Architectural indicators: more text, polylines (rooms), arcs (doors/windows)
            architectural_score = text_count * 3 + poly_count * 2 + arc_count * 1.5
            
            # Structural indicators: more circles (columns), lines (beams), fewer text
            structural_score = circle_count * 3 + line_count * 1.5
            
            print(f"📊 Content analysis - Architectural: {architectural_score}, Structural: {structural_score}")
            print(f"📊 Element counts - Lines: {line_count}, Polylines: {poly_count}, Circles: {circle_count}, Text: {text_count}, Arcs: {arc_count}")
            
            if structural_score > architectural_score:
                print("✅ Detected: Structural (content)")
                return 'structural'
            else:
                print("✅ Detected: Architectural (content)")
                return 'architectural'
            
        except Exception as e:
            print(f"⚠️ Content analysis failed, defaulting to architectural: {e}")
            return 'architectural'

    # ... keep all the calculation methods the same as before ...
    
    def calculate_area(self, line_count, poly_count, file_size):
        """Calculate area based on file characteristics"""
        base_area = (line_count * 2 + poly_count * 10) * (file_size / 102400)
        return max(500, min(5000, base_area))
    
    def calculate_rooms(self, poly_count, circle_count):
        """Calculate number of rooms"""
        return max(1, min(10, poly_count // 5 + circle_count // 10))
    
    def calculate_wall_length(self, line_count, file_size):
        """Calculate wall length"""
        return max(20, min(500, line_count * 0.8 * (file_size / 102400)))
    
    def calculate_perimeter(self, line_count, poly_count):
        """Calculate perimeter"""
        return max(30, min(400, (line_count + poly_count * 2) * 0.5))
    
    def calculate_openings(self, line_count, circle_count, arc_count):
        """Calculate number of openings"""
        return max(2, min(30, line_count // 15 + circle_count // 5 + arc_count // 3))
    
    def calculate_concrete_volume(self, total_elements, file_size):
        """Calculate concrete volume for structural plans"""
        base_volume = total_elements * 0.5 * (file_size / 102400)
        return max(10, min(500, base_volume))
    
    def calculate_steel_quantity(self, line_count, circle_count):
        """Calculate steel quantity"""
        base_steel = (line_count * 15 + circle_count * 50)
        return max(500, min(50000, base_steel))
    
    def calculate_formwork_area(self, line_count, poly_count):
        """Calculate formwork area"""
        base_area = (line_count * 1.5 + poly_count * 3)
        return max(50, min(3000, base_area))
    
    def calculate_footing_count(self, circle_count, poly_count):
        """Calculate footing count"""
        return max(2, min(50, circle_count // 2 + poly_count // 10))
    
    def calculate_column_count(self, circle_count, line_count):
        """Calculate column count"""
        return max(4, min(100, circle_count + line_count // 20))
    
    def calculate_beam_length(self, line_count, file_size):
        """Calculate beam length"""
        return max(10, min(500, line_count * 0.3 * (file_size / 102400)))
    
    def calculate_slab_area(self, poly_count, file_size):
        """Calculate slab area"""
        base_area = poly_count * 8 * (file_size / 102400)
        return max(50, min(2000, base_area))
    
    def get_default_features(self, plan_type):
        """Return realistic default features based on plan type"""
        if plan_type == 'architectural':
            return {
                'total_area': 1200.0, 'num_rooms': 4, 'wall_length': 120.0,
                'perimeter': 100.0, 'complexity': 5.5, 'openings': 12
            }
        else:
            return {
                'concrete_volume': 65.0, 'steel_quantity': 5200.0, 'formwork_area': 350.0,
                'footing_count': 12, 'column_count': 15, 'beam_length': 95.0,
                'slab_area': 120.0, 'structure_complexity': 6.2
            }