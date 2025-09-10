#!/usr/bin/env python3
"""
🦈 TEMPORAL ANALYSIS DEMONSTRATION
Multi-Species Shark Habitat Analysis Across Time Periods
"""

from automatic_nasa_framework import AutomaticNASAFramework

def run_temporal_demo():
    """Demonstrate temporal analysis capabilities"""
    
    print("🦈 TEMPORAL ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    # Initialize framework
    framework = AutomaticNASAFramework('great_white')
    
    # Define study area
    study_area = {
        'name': 'California Coast Temporal Study',
        'bounds': [-125.0, 32.0, -115.0, 42.0],
        'description': 'Multi-season shark habitat analysis'
    }
    
    # Define temporal periods
    date_ranges = {
        'Winter 2023': ['2023-12-01', '2024-02-28'],
        'Spring 2024': ['2024-03-01', '2024-05-31'],
        'Summer 2024': ['2024-06-01', '2024-08-31'],
        'Fall 2024': ['2024-09-01', '2024-11-30']
    }
    
    # Species to analyze
    species_list = ['great_white', 'mako', 'blue_shark']
    
    print(f"\n📅 Analyzing {len(species_list)} species across {len(date_ranges)} time periods...")
    
    # Run temporal analysis
    temporal_results, temporal_analysis = framework.temporal_habitat_analysis(
        study_area, 
        date_ranges, 
        species_list
    )
    
    # Display results
    print("\n📊 TEMPORAL ANALYSIS RESULTS")
    print("=" * 50)
    
    for species, analysis in temporal_analysis.items():
        print(f"\n🦈 {analysis['species_name']}:")
        print(f"   📈 HSI Trend: {analysis['hsi_trend']:+.4f}")
        print(f"   📊 Area Trend: {analysis['area_trend']:+.1f} cells")
        print(f"   🌊 Seasonal Variation: {analysis['seasonal_variation']:.3f}")
        print(f"   🏆 Best Period: {analysis['best_period']}")
        print(f"   📉 Worst Period: {analysis['worst_period']}")
        print(f"   📏 HSI Range: {analysis['mean_hsi_range'][0]:.3f} - {analysis['mean_hsi_range'][1]:.3f}")
    
    print(f"\n✅ Temporal analysis complete!")
    print(f"📊 Analyzed {len(species_list)} species × {len(date_ranges)} periods = {len(species_list) * len(date_ranges)} total analyses")
    
    return temporal_results, temporal_analysis

if __name__ == "__main__":
    results = run_temporal_demo()
