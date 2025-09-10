"""
NASA Satellite Data Downloader
Real NASA MODIS/VIIRS data download for shark habitat prediction
"""

import requests
import os
from datetime import datetime, timedelta
import json

class NASADataDownloader:
    """Download real NASA satellite files"""
    
    def __init__(self, username=None, password=None):
        """
        Initialize with NASA Earthdata credentials
        Get free account at: https://urs.earthdata.nasa.gov/
        """
        self.username = username or "your_nasa_username"
        self.password = password or "your_nasa_password"
        
        # NASA data URLs
        self.urls = {
            'oceancolor': 'https://oceandata.sci.gsfc.nasa.gov/api/file_search',
            'direct_download': 'https://oceandata.sci.gsfc.nasa.gov/cgi/getfile',
            'opendap': 'https://oceandata.sci.gsfc.nasa.gov/opendap'
        }
        
        # NASA product codes
        self.products = {
            'modis_sst_daily': 'MODISA_L3m_SST_Daily_4km_R2022.0',
            'modis_chl_daily': 'MODISA_L3m_CHL_Daily_4km_R2022.0',
            'modis_sst_monthly': 'MODISA_L3m_SST_Monthly_4km_R2022.0',
            'modis_chl_monthly': 'MODISA_L3m_CHL_Monthly_4km_R2022.0',
            'viirs_sst_daily': 'VIIRSN_L3m_SST_Daily_4km_R2022.0',
            'viirs_chl_daily': 'VIIRSN_L3m_CHL_Daily_4km_R2022.0'
        }
    
    def search_files(self, product, start_date, end_date, region=None):
        """
        Search for NASA files
        
        Args:
            product: Product name (e.g., 'modis_sst_daily')
            start_date: Start date 'YYYY-MM-DD'
            end_date: End date 'YYYY-MM-DD'
            region: Optional bounding box [west, south, east, north]
        
        Returns:
            List of available files
        """
        
        if product not in self.products:
            raise ValueError(f"Unknown product: {product}")
        
        # Build search parameters
        params = {
            'sensor': 'modis' if 'modis' in product else 'viirs',
            'dtype': 'L3m',
            'prod': 'SST' if 'sst' in product else 'CHL',
            'resolution': '4km',
            'period': 'DAY' if 'daily' in product else 'MO',
            'start': start_date,
            'end': end_date,
            'format': 'json'
        }
        
        if region:
            params.update({
                'north': region[3],
                'south': region[1], 
                'east': region[2],
                'west': region[0]
            })
        
        try:
            print(f"🔍 Searching NASA files for {product}...")
            response = requests.get(
                self.urls['oceancolor'],
                params=params,
                auth=(self.username, self.password),
                timeout=30
            )
            
            if response.status_code == 200:
                files = response.json()
                print(f"✅ Found {len(files)} files")
                return files
            else:
                print(f"❌ Search failed: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def download_file(self, filename, output_dir="nasa_data"):
        """
        Download a specific NASA file
        
        Args:
            filename: NASA filename (e.g., 'A20240101.L3m_DAY_SST_sst_4km.nc')
            output_dir: Local directory to save file
        
        Returns:
            Path to downloaded file or None if failed
        """
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Build download URL
        download_url = f"{self.urls['direct_download']}/{filename}"
        output_path = os.path.join(output_dir, filename)
        
        # Skip if already exists
        if os.path.exists(output_path):
            print(f"✅ File already exists: {filename}")
            return output_path
        
        try:
            print(f"⬇️ Downloading {filename}...")
            
            response = requests.get(
                download_url,
                auth=(self.username, self.password),
                stream=True,
                timeout=300  # 5 minutes
            )
            
            if response.status_code == 200:
                # Download with progress
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if total_size > 0:
                                percent = (downloaded / total_size) * 100
                                print(f"\r   Progress: {percent:.1f}%", end='', flush=True)
                
                print(f"\n✅ Downloaded: {filename}")
                return output_path
                
            else:
                print(f"❌ Download failed: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Download error: {e}")
            return None
    
    def download_shark_habitat_data(self, start_date, end_date, region=None):
        """
        Download complete dataset for shark habitat analysis
        
        Args:
            start_date: Start date 'YYYY-MM-DD'
            end_date: End date 'YYYY-MM-DD'
            region: Bounding box [west, south, east, north]
        
        Returns:
            Dictionary with downloaded file paths
        """
        
        print("🦈 Downloading NASA data for shark habitat analysis...")
        
        # Default to California coast if no region specified
        if region is None:
            region = [-125.0, 32.0, -115.0, 42.0]  # [west, south, east, north]
        
        downloaded_files = {
            'sst_files': [],
            'chl_files': []
        }
        
        # Download SST data (MODIS daily)
        print("\n📊 Downloading Sea Surface Temperature data...")
        sst_files = self.search_files('modis_sst_daily', start_date, end_date, region)
        
        for file_info in sst_files[:5]:  # Limit to 5 files for demo
            filename = file_info.get('name', '')
            if filename:
                path = self.download_file(filename)
                if path:
                    downloaded_files['sst_files'].append(path)
        
        # Download Chlorophyll data (MODIS daily)
        print("\n🌱 Downloading Chlorophyll-a data...")
        chl_files = self.search_files('modis_chl_daily', start_date, end_date, region)
        
        for file_info in chl_files[:5]:  # Limit to 5 files for demo
            filename = file_info.get('name', '')
            if filename:
                path = self.download_file(filename)
                if path:
                    downloaded_files['chl_files'].append(path)
        
        return downloaded_files

def demo_nasa_download():
    """Demo NASA data download"""
    
    print("🚀 NASA Data Download Demo")
    print("=" * 50)
    
    # Initialize downloader (you need real credentials)
    downloader = NASADataDownloader(
        username="your_nasa_username",  # Replace with your NASA username
        password="your_nasa_password"   # Replace with your NASA password
    )
    
    # Download recent data for California coast
    start_date = "2024-01-01"
    end_date = "2024-01-07"
    california_coast = [-125.0, 32.0, -115.0, 42.0]  # [west, south, east, north]
    
    try:
        files = downloader.download_shark_habitat_data(
            start_date=start_date,
            end_date=end_date,
            region=california_coast
        )
        
        print(f"\n✅ Download Complete!")
        print(f"   SST files: {len(files['sst_files'])}")
        print(f"   Chlorophyll files: {len(files['chl_files'])}")
        
        # Show file info
        for category, file_list in files.items():
            if file_list:
                print(f"\n{category.upper()}:")
                for file_path in file_list:
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    print(f"   📁 {os.path.basename(file_path)} ({size_mb:.1f} MB)")
        
        return files
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return None

# Alternative: Direct file URLs (if you know specific files)
def download_specific_files():
    """Download specific NASA files by direct URL"""
    
    # Example NASA file URLs (these are real URLs but need authentication)
    example_files = {
        'sst_file': 'https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20240101.L3m_DAY_SST_sst_4km.nc',
        'chl_file': 'https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20240101.L3m_DAY_CHL_chlor_a_4km.nc'
    }
    
    print("📥 Alternative: Direct file download")
    print("You can download specific files if you know their URLs:")
    
    for name, url in example_files.items():
        print(f"\n{name}:")
        print(f"  URL: {url}")
        print(f"  Command: wget --user=USERNAME --password=PASSWORD '{url}'")

if __name__ == "__main__":
    print("🛰️ NASA Satellite Data Downloader")
    print("=" * 60)
    print()
    print("SETUP REQUIRED:")
    print("1. Get free NASA Earthdata account: https://urs.earthdata.nasa.gov/")
    print("2. Replace 'your_nasa_username' and 'your_nasa_password' with real credentials")
    print("3. Install required packages: pip install requests")
    print()
    
    # Show what the demo would do
    print("DEMO WOULD DOWNLOAD:")
    print("- MODIS Aqua Sea Surface Temperature (daily, 4km)")
    print("- MODIS Aqua Chlorophyll-a (daily, 4km)")
    print("- California coast region (32°N-42°N, 125°W-115°W)")
    print("- Date range: 2024-01-01 to 2024-01-07")
    print()
    
    # Show alternative methods
    download_specific_files()
    
    print("\n💡 TIP: Start with monthly composites (less files, better coverage)")
    print("💡 TIP: Use NASA Giovanni for quick data visualization first")
    print("💡 TIP: Check NASA Worldview for data availability before downloading")
