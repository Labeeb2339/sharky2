"""
Shark Habitat Analysis and Visualization Module
Advanced analysis tools and visualization capabilities for shark habitat predictions
"""

import json
import math
import statistics
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class HabitatAnalyzer:
    """
    Advanced analysis tools for shark habitat predictions
    """
    
    def __init__(self):
        self.analysis_cache = {}
    
    def calculate_habitat_statistics(self, hsi_grid: List[List[float]]) -> Dict:
        """
        Calculate comprehensive habitat statistics
        """
        flat_hsi = [val for row in hsi_grid for val in row]
        
        stats = {
            'basic_stats': {
                'mean': statistics.mean(flat_hsi),
                'median': statistics.median(flat_hsi),
                'std_dev': statistics.stdev(flat_hsi) if len(flat_hsi) > 1 else 0,
                'min': min(flat_hsi),
                'max': max(flat_hsi),
                'range': max(flat_hsi) - min(flat_hsi)
            },
            'percentiles': {
                'p25': self._percentile(flat_hsi, 25),
                'p75': self._percentile(flat_hsi, 75),
                'p90': self._percentile(flat_hsi, 90),
                'p95': self._percentile(flat_hsi, 95),
                'p99': self._percentile(flat_hsi, 99)
            },
            'habitat_quality': {
                'excellent': sum(1 for val in flat_hsi if val > 0.8),
                'good': sum(1 for val in flat_hsi if 0.6 < val <= 0.8),
                'moderate': sum(1 for val in flat_hsi if 0.4 < val <= 0.6),
                'poor': sum(1 for val in flat_hsi if 0.2 < val <= 0.4),
                'unsuitable': sum(1 for val in flat_hsi if val <= 0.2)
            },
            'spatial_metrics': self._calculate_spatial_metrics(hsi_grid)
        }
        
        # Convert counts to percentages
        total_cells = len(flat_hsi)
        quality_keys = list(stats['habitat_quality'].keys())
        for quality in quality_keys:
            stats['habitat_quality'][quality + '_percent'] = (
                stats['habitat_quality'][quality] / total_cells * 100
            )
        
        return stats
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of data"""
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))
    
    def _calculate_spatial_metrics(self, hsi_grid: List[List[float]]) -> Dict:
        """
        Calculate spatial metrics like connectivity and fragmentation
        """
        rows, cols = len(hsi_grid), len(hsi_grid[0])
        
        # Calculate spatial autocorrelation (simplified Moran's I)
        autocorr = self._calculate_spatial_autocorrelation(hsi_grid)
        
        # Calculate patch metrics for high-quality habitat (HSI > 0.6)
        high_quality_patches = self._identify_patches(hsi_grid, threshold=0.6)
        
        # Calculate connectivity index
        connectivity = self._calculate_connectivity_index(hsi_grid)
        
        return {
            'spatial_autocorrelation': autocorr,
            'num_high_quality_patches': len(high_quality_patches),
            'largest_patch_size': max([patch['size'] for patch in high_quality_patches]) if high_quality_patches else 0,
            'mean_patch_size': statistics.mean([patch['size'] for patch in high_quality_patches]) if high_quality_patches else 0,
            'connectivity_index': connectivity,
            'fragmentation_index': 1 - connectivity if connectivity > 0 else 1
        }
    
    def _calculate_spatial_autocorrelation(self, hsi_grid: List[List[float]]) -> float:
        """
        Calculate spatial autocorrelation (simplified Moran's I)
        """
        rows, cols = len(hsi_grid), len(hsi_grid[0])
        
        # Calculate global mean
        flat_values = [val for row in hsi_grid for val in row]
        global_mean = statistics.mean(flat_values)
        
        numerator = 0
        denominator = 0
        weight_sum = 0
        
        for i in range(rows):
            for j in range(cols):
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols:
                            weight = 1.0  # Simple binary weights
                            numerator += weight * (hsi_grid[i][j] - global_mean) * (hsi_grid[ni][nj] - global_mean)
                            weight_sum += weight
                
                denominator += (hsi_grid[i][j] - global_mean) ** 2
        
        if denominator == 0 or weight_sum == 0:
            return 0
        
        return (len(flat_values) / weight_sum) * (numerator / denominator)
    
    def _identify_patches(self, hsi_grid: List[List[float]], threshold: float) -> List[Dict]:
        """
        Identify connected patches of high-quality habitat
        """
        rows, cols = len(hsi_grid), len(hsi_grid[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        patches = []
        
        def flood_fill(start_i, start_j):
            """Flood fill to identify connected patch"""
            stack = [(start_i, start_j)]
            patch_cells = []
            
            while stack:
                i, j = stack.pop()
                if (i < 0 or i >= rows or j < 0 or j >= cols or 
                    visited[i][j] or hsi_grid[i][j] <= threshold):
                    continue
                
                visited[i][j] = True
                patch_cells.append((i, j))
                
                # Add neighbors
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    stack.append((i+di, j+dj))
            
            return patch_cells
        
        for i in range(rows):
            for j in range(cols):
                if not visited[i][j] and hsi_grid[i][j] > threshold:
                    patch_cells = flood_fill(i, j)
                    if patch_cells:
                        # Calculate patch metrics
                        patch_hsi_values = [hsi_grid[pi][pj] for pi, pj in patch_cells]
                        patches.append({
                            'size': len(patch_cells),
                            'cells': patch_cells,
                            'mean_hsi': statistics.mean(patch_hsi_values),
                            'max_hsi': max(patch_hsi_values),
                            'centroid': (
                                statistics.mean([pi for pi, pj in patch_cells]),
                                statistics.mean([pj for pi, pj in patch_cells])
                            )
                        })
        
        return patches
    
    def _calculate_connectivity_index(self, hsi_grid: List[List[float]]) -> float:
        """
        Calculate habitat connectivity index
        """
        rows, cols = len(hsi_grid), len(hsi_grid[0])
        
        # Calculate average HSI of neighboring cells for each cell
        connectivity_sum = 0
        total_cells = 0
        
        for i in range(rows):
            for j in range(cols):
                if hsi_grid[i][j] > 0.4:  # Only consider moderate+ quality habitat
                    neighbor_hsi = []
                    
                    # Check 8-connected neighbors
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < rows and 0 <= nj < cols:
                                neighbor_hsi.append(hsi_grid[ni][nj])
                    
                    if neighbor_hsi:
                        # Connectivity is the product of cell HSI and mean neighbor HSI
                        connectivity_sum += hsi_grid[i][j] * statistics.mean(neighbor_hsi)
                        total_cells += 1
        
        return connectivity_sum / total_cells if total_cells > 0 else 0

class SimpleVisualizer:
    """
    Simple ASCII-based visualization for habitat data
    """
    
    @staticmethod
    def create_ascii_map(hsi_grid: List[List[float]], title: str = "Habitat Suitability Map") -> str:
        """
        Create ASCII visualization of habitat suitability
        """
        symbols = {
            'excellent': '█',  # >0.8
            'good': '▓',       # 0.6-0.8
            'moderate': '▒',   # 0.4-0.6
            'poor': '░',       # 0.2-0.4
            'unsuitable': '·'  # <=0.2
        }
        
        lines = [title, "=" * len(title)]
        
        # Add legend
        lines.append("Legend:")
        lines.append(f"  {symbols['excellent']} Excellent (>0.8)")
        lines.append(f"  {symbols['good']} Good (0.6-0.8)")
        lines.append(f"  {symbols['moderate']} Moderate (0.4-0.6)")
        lines.append(f"  {symbols['poor']} Poor (0.2-0.4)")
        lines.append(f"  {symbols['unsuitable']} Unsuitable (≤0.2)")
        lines.append("")
        
        # Create map
        for row in hsi_grid:
            line = ""
            for val in row:
                if val > 0.8:
                    line += symbols['excellent']
                elif val > 0.6:
                    line += symbols['good']
                elif val > 0.4:
                    line += symbols['moderate']
                elif val > 0.2:
                    line += symbols['poor']
                else:
                    line += symbols['unsuitable']
            lines.append(line)
        
        return "\n".join(lines)
    
    @staticmethod
    def create_contour_map(hsi_grid: List[List[float]], levels: List[float] = None) -> str:
        """
        Create simple ASCII contour map
        """
        if levels is None:
            levels = [0.2, 0.4, 0.6, 0.8]
        
        rows, cols = len(hsi_grid), len(hsi_grid[0])
        contour_map = [['·' for _ in range(cols)] for _ in range(rows)]
        
        # Mark contour lines
        for i in range(rows-1):
            for j in range(cols-1):
                current = hsi_grid[i][j]
                right = hsi_grid[i][j+1]
                down = hsi_grid[i+1][j]
                
                # Check for level crossings
                for level in levels:
                    if ((current <= level < right) or (right <= level < current) or
                        (current <= level < down) or (down <= level < current)):
                        
                        if level >= 0.8:
                            contour_map[i][j] = '█'
                        elif level >= 0.6:
                            contour_map[i][j] = '▓'
                        elif level >= 0.4:
                            contour_map[i][j] = '▒'
                        else:
                            contour_map[i][j] = '░'
                        break
        
        lines = ["Habitat Suitability Contours", "=" * 30]
        for row in contour_map:
            lines.append(''.join(row))
        
        return "\n".join(lines)

class ReportGenerator:
    """
    Generate comprehensive analysis reports
    """
    
    def __init__(self):
        self.analyzer = HabitatAnalyzer()
        self.visualizer = SimpleVisualizer()
    
    def generate_habitat_report(self, results: Dict, species: str) -> str:
        """
        Generate comprehensive habitat analysis report
        """
        hsi_grid = results['hsi']
        components = results.get('components', {})
        
        # Calculate statistics
        stats = self.analyzer.calculate_habitat_statistics(hsi_grid)
        
        # Generate report sections
        report_sections = []
        
        # Header
        report_sections.append(self._generate_header(species))
        
        # Executive Summary
        report_sections.append(self._generate_executive_summary(stats))
        
        # Detailed Statistics
        report_sections.append(self._generate_detailed_statistics(stats))
        
        # Spatial Analysis
        report_sections.append(self._generate_spatial_analysis(stats))
        
        # Habitat Quality Distribution
        report_sections.append(self._generate_habitat_distribution(stats))
        
        # ASCII Visualization
        report_sections.append(self._generate_visualization(hsi_grid))
        
        # Component Analysis
        if components:
            report_sections.append(self._generate_component_analysis(components))
        
        # Recommendations
        report_sections.append(self._generate_recommendations(stats, species))
        
        return "\n\n".join(report_sections)
    
    def _generate_header(self, species: str) -> str:
        """Generate report header"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
SHARK HABITAT SUITABILITY ANALYSIS REPORT
{'=' * 50}
Species: {species.replace('_', ' ').title()}
Analysis Date: {timestamp}
Framework Version: Enhanced v2.0
"""
    
    def _generate_executive_summary(self, stats: Dict) -> str:
        """Generate executive summary"""
        basic = stats['basic_stats']
        quality = stats['habitat_quality']
        spatial = stats['spatial_metrics']
        
        return f"""
EXECUTIVE SUMMARY
{'-' * 20}
Overall Habitat Quality: {self._classify_overall_quality(basic['mean'])}
Mean Habitat Suitability Index: {basic['mean']:.3f}
Habitat Variability: {basic['std_dev']:.3f} (std dev)

Key Findings:
• {quality['excellent_percent']:.1f}% of area shows excellent habitat quality (HSI > 0.8)
• {quality['good_percent']:.1f}% shows good habitat quality (HSI 0.6-0.8)
• {spatial['num_high_quality_patches']} distinct high-quality habitat patches identified
• Spatial connectivity index: {spatial['connectivity_index']:.3f}
• Habitat fragmentation level: {self._classify_fragmentation(spatial['fragmentation_index'])}
"""
    
    def _generate_detailed_statistics(self, stats: Dict) -> str:
        """Generate detailed statistics section"""
        basic = stats['basic_stats']
        percentiles = stats['percentiles']
        
        return f"""
DETAILED STATISTICS
{'-' * 20}
Basic Statistics:
  Mean HSI: {basic['mean']:.4f}
  Median HSI: {basic['median']:.4f}
  Standard Deviation: {basic['std_dev']:.4f}
  Minimum HSI: {basic['min']:.4f}
  Maximum HSI: {basic['max']:.4f}
  Range: {basic['range']:.4f}

Percentile Distribution:
  25th percentile: {percentiles['p25']:.4f}
  75th percentile: {percentiles['p75']:.4f}
  90th percentile: {percentiles['p90']:.4f}
  95th percentile: {percentiles['p95']:.4f}
  99th percentile: {percentiles['p99']:.4f}
"""
    
    def _generate_spatial_analysis(self, stats: Dict) -> str:
        """Generate spatial analysis section"""
        spatial = stats['spatial_metrics']
        
        return f"""
SPATIAL ANALYSIS
{'-' * 20}
Patch Analysis:
  Number of high-quality patches: {spatial['num_high_quality_patches']}
  Largest patch size: {spatial['largest_patch_size']} cells
  Mean patch size: {spatial['mean_patch_size']:.1f} cells

Connectivity Metrics:
  Spatial autocorrelation (Moran's I): {spatial['spatial_autocorrelation']:.4f}
  Connectivity index: {spatial['connectivity_index']:.4f}
  Fragmentation index: {spatial['fragmentation_index']:.4f}

Interpretation:
  {self._interpret_spatial_metrics(spatial)}
"""
    
    def _generate_habitat_distribution(self, stats: Dict) -> str:
        """Generate habitat quality distribution"""
        quality = stats['habitat_quality']
        
        return f"""
HABITAT QUALITY DISTRIBUTION
{'-' * 30}
Excellent (HSI > 0.8):    {quality['excellent']:4d} cells ({quality['excellent_percent']:5.1f}%)
Good (HSI 0.6-0.8):       {quality['good']:4d} cells ({quality['good_percent']:5.1f}%)
Moderate (HSI 0.4-0.6):   {quality['moderate']:4d} cells ({quality['moderate_percent']:5.1f}%)
Poor (HSI 0.2-0.4):       {quality['poor']:4d} cells ({quality['poor_percent']:5.1f}%)
Unsuitable (HSI ≤ 0.2):   {quality['unsuitable']:4d} cells ({quality['unsuitable_percent']:5.1f}%)
"""
    
    def _generate_visualization(self, hsi_grid: List[List[float]]) -> str:
        """Generate ASCII visualization"""
        return f"""
HABITAT VISUALIZATION
{'-' * 22}
{self.visualizer.create_ascii_map(hsi_grid)}
"""
    
    def _generate_component_analysis(self, components: Dict) -> str:
        """Generate component analysis if available"""
        return f"""
COMPONENT ANALYSIS
{'-' * 20}
Individual habitat suitability components:
(Component analysis would show temperature, productivity, 
frontal zones, and depth suitability contributions)
"""
    
    def _generate_recommendations(self, stats: Dict, species: str) -> str:
        """Generate management recommendations"""
        basic = stats['basic_stats']
        spatial = stats['spatial_metrics']
        
        recommendations = []
        
        if basic['mean'] > 0.6:
            recommendations.append("• High overall habitat quality - consider for protection priority")
        elif basic['mean'] < 0.3:
            recommendations.append("• Low habitat quality - investigate environmental stressors")
        
        if spatial['fragmentation_index'] > 0.7:
            recommendations.append("• High fragmentation - focus on connectivity corridors")
        
        if spatial['num_high_quality_patches'] < 3:
            recommendations.append("• Few high-quality patches - protect existing hotspots")
        
        return f"""
MANAGEMENT RECOMMENDATIONS
{'-' * 28}
Based on the habitat analysis for {species.replace('_', ' ')}:

{chr(10).join(recommendations) if recommendations else "• Standard monitoring protocols recommended"}

• Continue regular monitoring to track habitat changes
• Integrate with fisheries management and marine protected area planning
• Consider seasonal variations in habitat suitability
"""
    
    def _classify_overall_quality(self, mean_hsi: float) -> str:
        """Classify overall habitat quality"""
        if mean_hsi > 0.7:
            return "Excellent"
        elif mean_hsi > 0.5:
            return "Good"
        elif mean_hsi > 0.3:
            return "Moderate"
        else:
            return "Poor"
    
    def _classify_fragmentation(self, frag_index: float) -> str:
        """Classify fragmentation level"""
        if frag_index > 0.7:
            return "High"
        elif frag_index > 0.4:
            return "Moderate"
        else:
            return "Low"
    
    def _interpret_spatial_metrics(self, spatial: Dict) -> str:
        """Interpret spatial metrics"""
        autocorr = spatial['spatial_autocorrelation']
        connectivity = spatial['connectivity_index']
        
        interpretation = []
        
        if autocorr > 0.3:
            interpretation.append("Strong spatial clustering of habitat quality")
        elif autocorr < -0.3:
            interpretation.append("Checkerboard pattern in habitat quality")
        else:
            interpretation.append("Random spatial distribution of habitat quality")
        
        if connectivity > 0.6:
            interpretation.append("Well-connected habitat patches")
        elif connectivity < 0.3:
            interpretation.append("Poorly connected, isolated habitat patches")
        else:
            interpretation.append("Moderately connected habitat network")
        
        return ". ".join(interpretation) + "."

def demonstrate_analysis():
    """
    Demonstrate the analysis and visualization capabilities
    """
    # Create sample data
    import random
    random.seed(42)
    
    grid_size = 20
    hsi_grid = []
    
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            # Create realistic habitat pattern
            base = 0.3 + 0.4 * math.sin(i * 0.3) * math.cos(j * 0.2)
            noise = random.gauss(0, 0.15)
            hsi = max(0, min(1, base + noise))
            row.append(hsi)
        hsi_grid.append(row)
    
    # Create sample results
    results = {
        'hsi': hsi_grid,
        'species': 'great_white'
    }
    
    # Generate report
    report_gen = ReportGenerator()
    report = report_gen.generate_habitat_report(results, 'great_white')
    
    print(report)

if __name__ == "__main__":
    demonstrate_analysis()
