"""
Simplified Shark Habitat Prediction Framework
Works with minimal dependencies - only requires Python standard library
"""

import math
import random
import json
from datetime import datetime

class SimpleSharkHabitatPredictor:
    """
    Simplified shark habitat predictor using only Python standard library
    """
    
    def __init__(self, species='great_white'):
        self.species = species
        self.species_params = self._get_species_params(species)
        
    def _get_species_params(self, species):
        """Species-specific ecological parameters"""
        params = {
            'great_white': {
                'temp_opt': 18.0,
                'temp_std': 3.0,
                'temp_range': [12, 24],
                'depth_pref': [0, 200],
                'chl_k': 0.5,
                'chl_alpha': 2.0,
                'frontal_lambda': 0.1,
                'coastal_weight': 0.3
            },
            'tiger': {
                'temp_opt': 25.0,
                'temp_std': 2.5,
                'temp_range': [20, 30],
                'depth_pref': [0, 300],
                'chl_k': 0.8,
                'chl_alpha': 1.5,
                'frontal_lambda': 0.05,
                'coastal_weight': 0.8
            },
            'bull': {
                'temp_opt': 26.0,
                'temp_std': 4.0,
                'temp_range': [18, 32],
                'depth_pref': [0, 150],
                'chl_k': 1.0,
                'chl_alpha': 1.2,
                'frontal_lambda': 0.02,
                'coastal_weight': 0.9
            }
        }
        return params.get(species, params['great_white'])

class SimpleSatelliteDataProcessor:
    """
    Simple satellite data processing functions
    """
    
    @staticmethod
    def calculate_sst_gradient(sst_grid):
        """
        Calculate simple SST gradient using finite differences
        """
        rows, cols = len(sst_grid), len(sst_grid[0])
        gradient = [[0.0 for _ in range(cols)] for _ in range(rows)]
        
        for i in range(1, rows-1):
            for j in range(1, cols-1):
                # Simple gradient calculation
                dx = sst_grid[i][j+1] - sst_grid[i][j-1]
                dy = sst_grid[i+1][j] - sst_grid[i-1][j]
                gradient[i][j] = math.sqrt(dx*dx + dy*dy) / 2.0
                
        return gradient
    
    @staticmethod
    def generate_synthetic_data(grid_size=50):
        """
        Generate synthetic environmental data for demonstration
        """
        random.seed(42)  # For reproducible results
        
        data = {
            'sst': [],
            'chlorophyll': [],
            'bathymetry': [],
            'par': []
        }
        
        for i in range(grid_size):
            sst_row = []
            chl_row = []
            depth_row = []
            par_row = []
            
            for j in range(grid_size):
                # Create some spatial patterns
                x_norm = i / grid_size
                y_norm = j / grid_size
                
                # SST with gradient (warmer in south)
                sst = 15 + 10 * (1 - x_norm) + 2 * random.random()
                
                # Chlorophyll with coastal influence
                coastal_dist = min(x_norm, y_norm, 1-x_norm, 1-y_norm)
                chl = 0.1 + 2.0 * (1 - coastal_dist) + 0.5 * random.random()
                
                # Bathymetry (deeper offshore)
                depth = 10 + 200 * coastal_dist + 50 * random.random()
                
                # PAR (photosynthetically available radiation)
                par = 25 + 15 * random.random()
                
                sst_row.append(sst)
                chl_row.append(chl)
                depth_row.append(depth)
                par_row.append(par)
            
            data['sst'].append(sst_row)
            data['chlorophyll'].append(chl_row)
            data['bathymetry'].append(depth_row)
            data['par'].append(par_row)
        
        return data

class SimpleHabitatSuitability:
    """
    Calculate habitat suitability using mathematical functions
    """
    
    @staticmethod
    def temperature_suitability(temp, temp_opt, temp_std):
        """Gaussian temperature suitability"""
        return math.exp(-((temp - temp_opt)**2) / (2 * temp_std**2))
    
    @staticmethod
    def chlorophyll_suitability(chl, k, alpha):
        """Michaelis-Menten chlorophyll suitability"""
        return (chl**alpha) / (chl**alpha + k**alpha)
    
    @staticmethod
    def depth_suitability(depth, depth_min, depth_max, sigma=50):
        """Depth preference function"""
        if depth_min <= depth <= depth_max:
            return 1.0
        elif depth < depth_min:
            return math.exp(-((depth - depth_min)**2) / (2 * sigma**2))
        else:  # depth > depth_max
            return math.exp(-((depth - depth_max)**2) / (2 * sigma**2))
    
    @staticmethod
    def frontal_suitability(gradient, lambda_param):
        """Frontal zone suitability"""
        return 1 - math.exp(-gradient / lambda_param)

class SimpleHSICalculator:
    """
    Calculate Habitat Suitability Index
    """
    
    def __init__(self, species_params):
        self.params = species_params
    
    def calculate_hsi_grid(self, environmental_data):
        """
        Calculate HSI for entire grid
        """
        sst_grid = environmental_data['sst']
        chl_grid = environmental_data['chlorophyll']
        depth_grid = environmental_data['bathymetry']
        
        # Calculate SST gradient
        gradient_grid = SimpleSatelliteDataProcessor.calculate_sst_gradient(sst_grid)
        
        rows, cols = len(sst_grid), len(sst_grid[0])
        hsi_grid = [[0.0 for _ in range(cols)] for _ in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                # Individual suitability components
                s_temp = SimpleHabitatSuitability.temperature_suitability(
                    sst_grid[i][j], self.params['temp_opt'], self.params['temp_std']
                )
                
                s_chl = SimpleHabitatSuitability.chlorophyll_suitability(
                    chl_grid[i][j], self.params['chl_k'], self.params['chl_alpha']
                )
                
                s_depth = SimpleHabitatSuitability.depth_suitability(
                    depth_grid[i][j], self.params['depth_pref'][0], self.params['depth_pref'][1]
                )
                
                s_front = SimpleHabitatSuitability.frontal_suitability(
                    gradient_grid[i][j], self.params['frontal_lambda']
                )
                
                # Combined HSI (geometric mean)
                hsi = (s_temp * s_chl * s_depth * s_front) ** 0.25
                hsi_grid[i][j] = hsi
        
        return hsi_grid, gradient_grid

def print_grid_stats(grid, name):
    """Print statistics for a 2D grid"""
    flat_values = [val for row in grid for val in row]
    min_val = min(flat_values)
    max_val = max(flat_values)
    mean_val = sum(flat_values) / len(flat_values)
    
    print(f"{name}:")
    print(f"  Min: {min_val:.3f}")
    print(f"  Max: {max_val:.3f}")
    print(f"  Mean: {mean_val:.3f}")
    print()

def print_hsi_map(hsi_grid, threshold=0.5):
    """Print a simple ASCII map of habitat suitability"""
    print("Habitat Suitability Map (H=High >0.7, M=Medium 0.4-0.7, L=Low <0.4):")
    print("=" * 52)
    
    for row in hsi_grid:
        line = ""
        for val in row:
            if val > 0.7:
                line += "H"
            elif val > 0.4:
                line += "M"
            else:
                line += "."
        print(line)
    print("=" * 52)
    
    # Calculate suitable habitat percentage
    total_cells = sum(len(row) for row in hsi_grid)
    suitable_cells = sum(1 for row in hsi_grid for val in row if val > threshold)
    percentage = (suitable_cells / total_cells) * 100
    
    print(f"Suitable habitat area (HSI > {threshold}): {percentage:.1f}%")

def save_results_to_json(results, filename="shark_habitat_results.json"):
    """Save results to JSON file"""
    # Convert grids to lists for JSON serialization
    json_results = {}
    for key, value in results.items():
        if isinstance(value, list) and isinstance(value[0], list):
            json_results[key] = value
        else:
            json_results[key] = str(value)
    
    with open(filename, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"Results saved to {filename}")

def main():
    """
    Main function to demonstrate the shark habitat prediction framework
    """
    print("=" * 60)
    print("SHARK HABITAT PREDICTION FRAMEWORK - SIMPLE VERSION")
    print("=" * 60)
    print()
    
    # Initialize predictor
    species = 'great_white'
    print(f"Initializing predictor for {species.replace('_', ' ').title()} Shark...")
    predictor = SimpleSharkHabitatPredictor(species=species)
    
    print(f"Species parameters:")
    for key, value in predictor.species_params.items():
        print(f"  {key}: {value}")
    print()
    
    # Generate synthetic environmental data
    print("Generating synthetic environmental data...")
    grid_size = 30  # Smaller grid for easier visualization
    env_data = SimpleSatelliteDataProcessor.generate_synthetic_data(grid_size)
    
    # Print environmental data statistics
    print("Environmental Data Statistics:")
    print_grid_stats(env_data['sst'], "Sea Surface Temperature (°C)")
    print_grid_stats(env_data['chlorophyll'], "Chlorophyll-a (mg/m³)")
    print_grid_stats(env_data['bathymetry'], "Bathymetry (m)")
    
    # Calculate Habitat Suitability Index
    print("Calculating Habitat Suitability Index...")
    hsi_calculator = SimpleHSICalculator(predictor.species_params)
    hsi_grid, gradient_grid = hsi_calculator.calculate_hsi_grid(env_data)
    
    # Print HSI statistics
    print_grid_stats(hsi_grid, "Habitat Suitability Index")
    print_grid_stats(gradient_grid, "SST Gradient (°C/pixel)")
    
    # Print habitat map
    print_hsi_map(hsi_grid)
    
    # Save results
    results = {
        'species': species,
        'timestamp': datetime.now().isoformat(),
        'grid_size': grid_size,
        'hsi_grid': hsi_grid,
        'environmental_data': env_data,
        'gradient_grid': gradient_grid,
        'species_params': predictor.species_params
    }
    
    save_results_to_json(results)
    
    # Identify best habitat locations
    print("\nTop 5 Habitat Locations:")
    flat_hsi = [(hsi_grid[i][j], i, j) for i in range(len(hsi_grid)) for j in range(len(hsi_grid[0]))]
    flat_hsi.sort(reverse=True)
    
    for k, (hsi_val, i, j) in enumerate(flat_hsi[:5]):
        sst = env_data['sst'][i][j]
        chl = env_data['chlorophyll'][i][j]
        depth = env_data['bathymetry'][i][j]
        print(f"  {k+1}. Location ({i:2d},{j:2d}): HSI={hsi_val:.3f}, SST={sst:.1f}°C, Chl={chl:.2f}mg/m³, Depth={depth:.0f}m")
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
