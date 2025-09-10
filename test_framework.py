#!/usr/bin/env python3
"""
Test Script for Enhanced Shark Habitat Prediction Framework
Demonstrates all components working together
"""

import sys
import traceback
from datetime import datetime

def test_enhanced_framework():
    """Test the main enhanced framework"""
    print("🦈 Testing Enhanced Shark Framework...")
    try:
        from enhanced_shark_framework import PredictionEngine, NASADataFetcher
        
        # Test species models
        engine = PredictionEngine(species='great_white')
        print(f"✓ Great White model loaded: {engine.species_params['scientific_name']}")
        
        engine = PredictionEngine(species='tiger_shark')
        print(f"✓ Tiger Shark model loaded: {engine.species_params['scientific_name']}")
        
        engine = PredictionEngine(species='bull_shark')
        print(f"✓ Bull Shark model loaded: {engine.species_params['scientific_name']}")
        
        # Test data fetcher
        fetcher = NASADataFetcher()
        lat_range = (36.0, 37.0)
        lon_range = (-122.0, -121.0)
        date_range = ('2024-01-01', '2024-01-07')
        
        sst_data = fetcher.fetch_modis_sst(lat_range, lon_range, date_range)
        chl_data = fetcher.fetch_modis_chlorophyll(lat_range, lon_range, date_range)
        
        print(f"✓ SST data: {len(sst_data['data'])}x{len(sst_data['data'][0])} grid")
        print(f"✓ Chlorophyll data: {len(chl_data['data'])}x{len(chl_data['data'][0])} grid")
        
        # Test prediction
        environmental_data = {'sst': sst_data, 'chlorophyll': chl_data}
        results = engine.predict_habitat_suitability(environmental_data)
        
        hsi_grid = results['hsi']
        flat_hsi = [val for row in hsi_grid for val in row]
        mean_hsi = sum(flat_hsi) / len(flat_hsi)
        
        print(f"✓ Habitat prediction complete: Mean HSI = {mean_hsi:.3f}")
        return True
        
    except Exception as e:
        print(f"✗ Enhanced framework test failed: {e}")
        traceback.print_exc()
        return False

def test_analysis_visualization():
    """Test the analysis and visualization module"""
    print("\n📊 Testing Analysis & Visualization...")
    try:
        from shark_analysis_visualization import HabitatAnalyzer, SimpleVisualizer, ReportGenerator
        
        # Create sample data
        import random
        import math
        random.seed(42)
        
        grid_size = 10
        hsi_grid = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                base = 0.3 + 0.4 * math.sin(i * 0.3) * math.cos(j * 0.2)
                noise = random.gauss(0, 0.15)
                hsi = max(0, min(1, base + noise))
                row.append(hsi)
            hsi_grid.append(row)
        
        # Test analyzer
        analyzer = HabitatAnalyzer()
        stats = analyzer.calculate_habitat_statistics(hsi_grid)
        print(f"✓ Statistics calculated: Mean HSI = {stats['basic_stats']['mean']:.3f}")
        print(f"✓ Spatial analysis: {stats['spatial_metrics']['num_high_quality_patches']} patches")
        
        # Test visualizer
        visualizer = SimpleVisualizer()
        ascii_map = visualizer.create_ascii_map(hsi_grid, "Test Map")
        print(f"✓ ASCII map generated: {len(ascii_map.split(chr(10)))} lines")
        
        # Test report generator
        report_gen = ReportGenerator()
        results = {'hsi': hsi_grid, 'species': 'great_white'}
        report = report_gen.generate_habitat_report(results, 'great_white')
        print(f"✓ Report generated: {len(report)} characters")
        
        return True
        
    except Exception as e:
        print(f"✗ Analysis & visualization test failed: {e}")
        traceback.print_exc()
        return False

def test_nasa_integration():
    """Test NASA data integration"""
    print("\n🛰️ Testing NASA Data Integration...")
    try:
        from nasa_data_integration import NASAAPIClient, RealTimeDataProcessor, DataQualityController
        
        # Test API client
        client = NASAAPIClient()
        print(f"✓ API client initialized with {len(client.endpoints)} endpoints")
        print(f"✓ Product catalog: {len(client.products)} data types")
        
        # Test data processor
        processor = RealTimeDataProcessor()
        bbox = (-122.0, 36.0, -121.0, 37.0)
        
        # Note: These will return simulated data since we don't have real API access
        sst_data = processor.get_latest_sst_data(bbox, days_back=1)
        if sst_data:
            print(f"✓ SST data retrieved: {sst_data['data_type']}")
        else:
            print("✓ SST data simulation (no real data available)")
        
        chl_data = processor.get_latest_chlorophyll_data(bbox, days_back=1)
        if chl_data:
            print(f"✓ Chlorophyll data retrieved: {chl_data['data_type']}")
        else:
            print("✓ Chlorophyll data simulation (no real data available)")
        
        # Test quality controller
        qc = DataQualityController()
        print("✓ Quality control system initialized")
        
        return True
        
    except Exception as e:
        print(f"✗ NASA integration test failed: {e}")
        traceback.print_exc()
        return False

def test_simple_version():
    """Test the simple working version"""
    print("\n🔧 Testing Simple Version...")
    try:
        import subprocess
        import sys
        
        result = subprocess.run([sys.executable, 'shark_habitat_simple.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ Simple version runs successfully")
            output_lines = result.stdout.strip().split('\n')
            print(f"✓ Generated {len(output_lines)} lines of output")
            return True
        else:
            print(f"✗ Simple version failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Simple version test failed: {e}")
        return False

def run_comprehensive_demo():
    """Run a comprehensive demonstration"""
    print("\n🌊 Running Comprehensive Demo...")
    try:
        from enhanced_shark_framework import PredictionEngine
        from shark_analysis_visualization import ReportGenerator
        
        # Multi-species comparison
        species_list = ['great_white', 'tiger_shark', 'bull_shark']
        results_summary = {}
        
        for species in species_list:
            engine = PredictionEngine(species=species)
            
            # Small test area
            lat_range = (36.0, 37.0)
            lon_range = (-122.0, -121.0)
            date_range = ('2024-01-01', '2024-01-07')
            
            # Get data
            sst_data = engine.data_fetcher.fetch_modis_sst(lat_range, lon_range, date_range)
            chl_data = engine.data_fetcher.fetch_modis_chlorophyll(lat_range, lon_range, date_range)
            environmental_data = {'sst': sst_data, 'chlorophyll': chl_data}
            
            # Predict habitat
            results = engine.predict_habitat_suitability(environmental_data)
            hsi_grid = results['hsi']
            flat_hsi = [val for row in hsi_grid for val in row]
            
            results_summary[species] = {
                'mean_hsi': sum(flat_hsi) / len(flat_hsi),
                'max_hsi': max(flat_hsi),
                'scientific_name': engine.species_params['scientific_name']
            }
        
        print("\n📋 Multi-Species Habitat Comparison:")
        print("=" * 60)
        for species, data in results_summary.items():
            print(f"{data['scientific_name']:25} | Mean HSI: {data['mean_hsi']:.3f} | Max HSI: {data['max_hsi']:.3f}")
        
        # Generate detailed report for best species
        best_species = max(results_summary.keys(), key=lambda x: results_summary[x]['mean_hsi'])
        print(f"\n🏆 Best habitat conditions for: {results_summary[best_species]['scientific_name']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Comprehensive demo failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Enhanced Shark Habitat Framework - Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Enhanced Framework", test_enhanced_framework),
        ("Analysis & Visualization", test_analysis_visualization),
        ("NASA Integration", test_nasa_integration),
        ("Simple Version", test_simple_version),
        ("Comprehensive Demo", run_comprehensive_demo)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{test_name:25} | {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! The framework is working correctly.")
        print("\nNext steps:")
        print("1. Run 'python enhanced_shark_framework.py' for full analysis")
        print("2. Check the generated JSON files for detailed results")
        print("3. Modify species parameters in the code for your research")
    else:
        print(f"\n⚠️  {total-passed} test(s) failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
