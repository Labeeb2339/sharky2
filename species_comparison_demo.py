#!/usr/bin/env python3
"""
🦈 SPECIES COMPARISON DEMONSTRATION
Compare All 6 Shark Species in Same Habitat
"""

from automatic_nasa_framework import AutomaticNASAFramework

def run_species_comparison():
    """Compare all 6 shark species in the same habitat"""
    
    print("🦈 MULTI-SPECIES HABITAT COMPARISON")
    print("=" * 60)
    
    # Define study area
    study_area = {
        'name': 'California Coast Multi-Species Study',
        'bounds': [-125.0, 32.0, -115.0, 42.0],
        'description': 'Comparative habitat analysis for 6 shark species'
    }
    
    date_range = ['2024-06-01', '2024-06-30']  # Summer period
    
    # All available species
    all_species = ['great_white', 'tiger_shark', 'bull_shark', 'hammerhead', 'mako', 'blue_shark']
    
    species_results = {}
    
    print(f"\n🔬 Analyzing {len(all_species)} species in same habitat...")
    
    for species in all_species:
        print(f"\n🦈 Analyzing {species.replace('_', ' ').title()}...")
        
        # Initialize framework for this species
        framework = AutomaticNASAFramework(species)
        
        # Get environmental data
        env_data, real_data = framework.auto_download_nasa_data(study_area, date_range)
        
        # Run habitat prediction
        results = framework.advanced_habitat_prediction(env_data)
        
        # Store results
        species_results[species] = {
            'name': framework.shark_params['name'],
            'scientific': framework.shark_params['scientific'],
            'mean_hsi': results['statistics']['mean_hsi'],
            'max_hsi': results['statistics']['max_hsi'],
            'suitable_cells': results['statistics']['suitable_cells'],
            'optimal_temp': framework.shark_params['optimal_temp'],
            'habitat_type': framework.shark_params['habitat_specificity'],
            'hunting_strategy': framework.shark_params['hunting_strategy']
        }
    
    # Display comparison results
    print("\n📊 SPECIES COMPARISON RESULTS")
    print("=" * 60)
    
    # Sort by mean HSI
    sorted_species = sorted(species_results.items(), key=lambda x: x[1]['mean_hsi'], reverse=True)
    
    print(f"🏆 HABITAT SUITABILITY RANKING (California Coast, Summer 2024):")
    print("-" * 60)
    
    for rank, (species_key, data) in enumerate(sorted_species, 1):
        print(f"{rank}. {data['name']} ({data['scientific']})")
        print(f"   📊 Mean HSI: {data['mean_hsi']:.3f}")
        print(f"   🎯 Max HSI: {data['max_hsi']:.3f}")
        print(f"   🌊 Suitable Cells: {data['suitable_cells']}")
        print(f"   🌡️ Optimal Temp: {data['optimal_temp']}°C")
        print(f"   🏠 Habitat: {data['habitat_type']}")
        print(f"   🎯 Strategy: {data['hunting_strategy']}")
        print()
    
    # Ecological insights
    print("🔬 ECOLOGICAL INSIGHTS:")
    print("-" * 30)
    
    # Temperature preferences
    temp_sorted = sorted(species_results.items(), key=lambda x: x[1]['optimal_temp'])
    print("🌡️ Temperature Preference Gradient:")
    for species_key, data in temp_sorted:
        print(f"   {data['optimal_temp']}°C - {data['name']}")
    
    # Habitat specialization
    print("\n🏠 Habitat Specialization:")
    coastal_species = [data['name'] for data in species_results.values() if 'coastal' in data['habitat_type']]
    pelagic_species = [data['name'] for data in species_results.values() if 'pelagic' in data['habitat_type'] or 'ocean' in data['habitat_type']]
    
    print(f"   Coastal Specialists: {', '.join(coastal_species)}")
    print(f"   Pelagic Specialists: {', '.join(pelagic_species)}")
    
    print(f"\n✅ Species comparison complete!")
    print(f"📊 Analyzed {len(all_species)} species with full ecological differentiation")
    
    return species_results

if __name__ == "__main__":
    results = run_species_comparison()
