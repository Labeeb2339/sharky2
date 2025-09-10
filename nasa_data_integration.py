"""
NASA Data Integration Module
Real-time integration with NASA satellite data APIs for shark habitat prediction
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import xml.etree.ElementTree as ET

class NASAAPIClient:
    """
    Client for accessing various NASA data APIs
    """
    
    def __init__(self):
        self.endpoints = {
            'oceancolor': 'https://oceandata.sci.gsfc.nasa.gov/api/file_search',
            'giovanni': 'https://giovanni.gsfc.nasa.gov/giovanni/daac-bin/service_manager.pl',
            'podaac': 'https://podaac.jpl.nasa.gov/ws/search/granule/',
            'earthdata': 'https://cmr.earthdata.nasa.gov/search/granules.json',
            'modis_l3': 'https://oceandata.sci.gsfc.nasa.gov/MODIS-Aqua/L3SMI/',
            'viirs_l3': 'https://oceandata.sci.gsfc.nasa.gov/VIIRS/L3SMI/'
        }
        
        # Common MODIS and VIIRS products for marine applications
        self.products = {
            'sst': {
                'modis': 'MODISA_L3m_SST_Monthly_4km_R2022.0',
                'viirs': 'VIIRSN_L3m_SST_Monthly_4km_R2022.0'
            },
            'chlorophyll': {
                'modis': 'MODISA_L3m_CHL_Monthly_4km_R2022.0', 
                'viirs': 'VIIRSN_L3m_CHL_Monthly_4km_R2022.0'
            },
            'par': {
                'modis': 'MODISA_L3m_PAR_Monthly_4km_R2022.0'
            },
            'pic': {
                'modis': 'MODISA_L3m_PIC_Monthly_4km_R2022.0'
            }
        }
    
    def search_oceancolor_files(self, sensor: str, product: str, 
                               start_date: str, end_date: str,
                               bbox: Optional[Tuple[float, float, float, float]] = None) -> List[Dict]:
        """
        Search for Ocean Color files
        
        Args:
            sensor: 'modis' or 'viirs'
            product: 'sst', 'chlorophyll', 'par', etc.
            start_date: 'YYYY-MM-DD'
            end_date: 'YYYY-MM-DD'
            bbox: (west, south, east, north) bounding box
            
        Returns:
            List of file metadata dictionaries
        """
        try:
            # Build query parameters
            params = {
                'sensor': sensor.upper(),
                'sdate': start_date,
                'edate': end_date,
                'dtype': 'L3m',  # Level 3 mapped
                'addurl': '1',
                'results_as_file': '1'
            }
            
            if product in self.products and sensor in self.products[product]:
                params['prod'] = self.products[product][sensor]
            
            if bbox:
                params['north'] = str(bbox[3])
                params['south'] = str(bbox[1]) 
                params['west'] = str(bbox[0])
                params['east'] = str(bbox[2])
            
            # Make request
            url = f"{self.endpoints['oceancolor']}?{urllib.parse.urlencode(params)}"
            
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read().decode('utf-8')
                
            # Parse response (typically returns file URLs)
            files = []
            for line in data.strip().split('\n'):
                if line.startswith('http'):
                    files.append({
                        'url': line.strip(),
                        'sensor': sensor,
                        'product': product,
                        'date_range': (start_date, end_date)
                    })
            
            return files
            
        except Exception as e:
            print(f"Error searching Ocean Color files: {e}")
            return []
    
    def query_earthdata_cmr(self, collection: str, temporal: str, 
                           spatial: Optional[str] = None) -> List[Dict]:
        """
        Query NASA Earthdata Common Metadata Repository (CMR)
        
        Args:
            collection: Collection concept ID or short name
            temporal: ISO 8601 temporal range
            spatial: Bounding box as "west,south,east,north"
            
        Returns:
            List of granule metadata
        """
        try:
            params = {
                'collection_concept_id': collection,
                'temporal': temporal,
                'page_size': 100
            }
            
            if spatial:
                params['bounding_box'] = spatial
            
            url = f"{self.endpoints['earthdata']}?{urllib.parse.urlencode(params)}"
            
            with urllib.request.urlopen(url, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            granules = []
            for entry in data.get('feed', {}).get('entry', []):
                granule = {
                    'id': entry.get('id'),
                    'title': entry.get('title'),
                    'updated': entry.get('updated'),
                    'links': [link.get('href') for link in entry.get('links', [])],
                    'summary': entry.get('summary')
                }
                granules.append(granule)
            
            return granules
            
        except Exception as e:
            print(f"Error querying CMR: {e}")
            return []
    
    def get_giovanni_data(self, variable: str, bbox: Tuple[float, float, float, float],
                         start_date: str, end_date: str) -> Optional[Dict]:
        """
        Request data from NASA Giovanni
        
        Args:
            variable: Variable name (e.g., 'MODISA_L3m_CHL_Monthly_4km_R2022_0_chlor_a')
            bbox: (west, south, east, north)
            start_date: 'YYYY-MM-DD'
            end_date: 'YYYY-MM-DD'
            
        Returns:
            Data dictionary or None if failed
        """
        try:
            params = {
                'service': 'ArAvTs',  # Area-averaged time series
                'starttime': f"{start_date}T00:00:00Z",
                'endtime': f"{end_date}T23:59:59Z",
                'bbox': f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
                'data': variable,
                'variableFacets': 'dataFieldMeasurement%3AChlorophyll%3B',
                'format': 'json'
            }
            
            url = f"{self.endpoints['giovanni']}?{urllib.parse.urlencode(params)}"
            
            with urllib.request.urlopen(url, timeout=60) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            return data
            
        except Exception as e:
            print(f"Error getting Giovanni data: {e}")
            return None

class RealTimeDataProcessor:
    """
    Process real-time NASA satellite data for shark habitat analysis
    """
    
    def __init__(self):
        self.api_client = NASAAPIClient()
        self.cache = {}  # Simple in-memory cache
    
    def get_latest_sst_data(self, bbox: Tuple[float, float, float, float],
                           days_back: int = 7) -> Optional[Dict]:
        """
        Get the latest available SST data
        
        Args:
            bbox: (west, south, east, north) bounding box
            days_back: How many days back to search
            
        Returns:
            SST data dictionary or None
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Try MODIS first, then VIIRS
        for sensor in ['modis', 'viirs']:
            files = self.api_client.search_oceancolor_files(
                sensor=sensor,
                product='sst',
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                bbox=bbox
            )
            
            if files:
                # Get the most recent file
                latest_file = files[-1]
                return self._download_and_process_file(latest_file, 'sst')
        
        return None
    
    def get_latest_chlorophyll_data(self, bbox: Tuple[float, float, float, float],
                                   days_back: int = 7) -> Optional[Dict]:
        """
        Get the latest available chlorophyll data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        for sensor in ['modis', 'viirs']:
            files = self.api_client.search_oceancolor_files(
                sensor=sensor,
                product='chlorophyll',
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                bbox=bbox
            )
            
            if files:
                latest_file = files[-1]
                return self._download_and_process_file(latest_file, 'chlorophyll')
        
        return None
    
    def _download_and_process_file(self, file_info: Dict, data_type: str) -> Dict:
        """
        Download and process a satellite data file
        
        Note: This is a simplified version. Real implementation would:
        - Handle NetCDF/HDF file formats
        - Apply quality flags and masks
        - Perform spatial/temporal interpolation
        - Handle different projections and grids
        """
        try:
            # In a real implementation, you would:
            # 1. Download the NetCDF/HDF file
            # 2. Use libraries like netCDF4, h5py, or xarray to read the data
            # 3. Extract the relevant variable (SST, chlorophyll, etc.)
            # 4. Apply quality control and masking
            # 5. Interpolate to desired grid
            
            # For now, return simulated data with realistic characteristics
            return self._simulate_realistic_data(file_info, data_type)
            
        except Exception as e:
            print(f"Error processing file {file_info.get('url', 'unknown')}: {e}")
            return None
    
    def _simulate_realistic_data(self, file_info: Dict, data_type: str) -> Dict:
        """
        Simulate realistic satellite data based on file metadata
        """
        import random
        import math
        
        # Create a realistic grid
        grid_size = 50
        data_grid = []
        
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                if data_type == 'sst':
                    # Realistic SST with spatial patterns
                    base_temp = 18 + 8 * math.sin(i * 0.1) * math.cos(j * 0.1)
                    noise = random.gauss(0, 1.5)
                    value = max(0, base_temp + noise)
                    
                elif data_type == 'chlorophyll':
                    # Log-normal distribution typical of chlorophyll
                    log_mean = -1.0 + 0.5 * math.sin(i * 0.2)
                    value = random.lognormvariate(log_mean, 0.8)
                    value = max(0.01, min(value, 50.0))  # Realistic range
                
                else:
                    value = random.random()
                
                row.append(value)
            data_grid.append(row)
        
        return {
            'data': data_grid,
            'metadata': file_info,
            'data_type': data_type,
            'grid_size': grid_size,
            'units': 'Celsius' if data_type == 'sst' else 'mg/m³',
            'timestamp': datetime.now().isoformat(),
            'quality': 'simulated'  # In real data, this would be quality flags
        }

class DataQualityController:
    """
    Quality control for satellite data
    """
    
    @staticmethod
    def apply_quality_flags(data: Dict, quality_threshold: float = 0.8) -> Dict:
        """
        Apply quality control flags to satellite data
        """
        if 'quality' not in data or data['quality'] == 'simulated':
            return data
        
        # In real implementation, this would:
        # - Check satellite quality flags
        # - Remove cloudy pixels
        # - Apply land/ice masks
        # - Flag suspicious values
        # - Interpolate missing data
        
        return data
    
    @staticmethod
    def validate_data_range(data: Dict) -> bool:
        """
        Validate that data values are within expected ranges
        """
        data_grid = data['data']
        data_type = data['data_type']
        
        flat_values = [val for row in data_grid for val in row]
        
        if data_type == 'sst':
            # SST should be between -2°C and 40°C
            return all(-2 <= val <= 40 for val in flat_values)
        elif data_type == 'chlorophyll':
            # Chlorophyll should be between 0.01 and 100 mg/m³
            return all(0.01 <= val <= 100 for val in flat_values)
        
        return True

def demonstrate_nasa_integration():
    """
    Demonstrate real NASA data integration
    """
    print("NASA Data Integration Demonstration")
    print("=" * 50)
    
    # Initialize processor
    processor = RealTimeDataProcessor()
    
    # Define study area (Monterey Bay, California)
    bbox = (-122.5, 36.0, -121.5, 37.0)  # (west, south, east, north)
    
    print(f"Study area: {bbox[1]}°N to {bbox[3]}°N, {bbox[0]}°W to {bbox[2]}°W")
    print("Searching for latest satellite data...")
    
    # Get latest SST data
    sst_data = processor.get_latest_sst_data(bbox, days_back=7)
    if sst_data:
        print(f"✓ Found SST data: {sst_data['metadata']['sensor']} sensor")
        print(f"  Grid size: {sst_data['grid_size']}x{sst_data['grid_size']}")
        print(f"  Units: {sst_data['units']}")
    else:
        print("✗ No SST data found")
    
    # Get latest chlorophyll data
    chl_data = processor.get_latest_chlorophyll_data(bbox, days_back=7)
    if chl_data:
        print(f"✓ Found Chlorophyll data: {chl_data['metadata']['sensor']} sensor")
        print(f"  Grid size: {chl_data['grid_size']}x{chl_data['grid_size']}")
        print(f"  Units: {chl_data['units']}")
    else:
        print("✗ No Chlorophyll data found")
    
    # Demonstrate API search
    print("\nDemonstrating API search capabilities...")
    api_client = NASAAPIClient()
    
    # Search for recent files
    files = api_client.search_oceancolor_files(
        sensor='modis',
        product='sst',
        start_date='2024-01-01',
        end_date='2024-01-31',
        bbox=bbox
    )
    
    print(f"Found {len(files)} MODIS SST files for January 2024")
    
    if files:
        print("Sample file info:")
        for i, file_info in enumerate(files[:3]):  # Show first 3
            print(f"  {i+1}. {file_info['url']}")
    
    print("\nNASA Data Integration demonstration complete!")

if __name__ == "__main__":
    demonstrate_nasa_integration()
