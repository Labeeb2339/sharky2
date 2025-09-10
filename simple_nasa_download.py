"""
Simple NASA Data Download Test
Download one real NASA file to test your credentials
"""

import requests
import os

def test_nasa_download():
    """Test downloading one NASA file"""
    
    print("🛰️ Testing NASA Data Download")
    print("=" * 40)
    
    # Your NASA credentials (replace with real ones)
    username = "labeeb2339"  # Your NASA username
    password = "YOUR_NASA_PASSWORD"  # Replace with your actual password
    
    # Test file URL (real NASA file)
    test_file_url = "https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20240101.L3m_MO_SST_sst_4km.nc"
    output_filename = "test_nasa_sst.nc"
    
    print(f"📥 Attempting to download test file...")
    print(f"   URL: {test_file_url}")
    print(f"   Output: {output_filename}")
    
    try:
        # Make request with authentication
        response = requests.get(
            test_file_url,
            auth=(username, password),
            stream=True,
            timeout=60
        )
        
        if response.status_code == 200:
            # Download file
            with open(output_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Check file size
            file_size = os.path.getsize(output_filename)
            print(f"✅ SUCCESS! Downloaded {file_size:,} bytes")
            print(f"   File saved as: {output_filename}")
            
            # Basic file info
            if file_size > 1000000:  # > 1MB
                print(f"   File size: {file_size / 1024 / 1024:.1f} MB")
                print("   This looks like a real NASA NetCDF file! 🎉")
                return True
            else:
                print("   ⚠️ File seems small - might be an error page")
                return False
                
        elif response.status_code == 401:
            print("❌ Authentication failed - check your NASA username/password")
            return False
        elif response.status_code == 404:
            print("❌ File not found - the URL might be incorrect")
            return False
        else:
            print(f"❌ Download failed: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def list_available_files():
    """Show examples of available NASA files"""
    
    print("\n📋 Available NASA Files (Examples):")
    print("=" * 50)
    
    examples = {
        "Monthly SST (4km)": [
            "A20240101.L3m_MO_SST_sst_4km.nc",
            "A20240201.L3m_MO_SST_sst_4km.nc",
            "A20240301.L3m_MO_SST_sst_4km.nc"
        ],
        "Monthly Chlorophyll (4km)": [
            "A20240101.L3m_MO_CHL_chlor_a_4km.nc",
            "A20240201.L3m_MO_CHL_chlor_a_4km.nc",
            "A20240301.L3m_MO_CHL_chlor_a_4km.nc"
        ],
        "Daily SST (4km)": [
            "A20240101.L3m_DAY_SST_sst_4km.nc",
            "A20240102.L3m_DAY_SST_sst_4km.nc",
            "A20240103.L3m_DAY_SST_sst_4km.nc"
        ]
    }
    
    for category, files in examples.items():
        print(f"\n{category}:")
        for file in files:
            url = f"https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/{file}"
            print(f"  📁 {file}")
            print(f"     {url}")

def show_nasa_websites():
    """Show the correct NASA websites to visit"""
    
    print("\n🌐 NASA Websites You Can Actually Use:")
    print("=" * 50)
    
    websites = {
        "NASA Giovanni (Easiest)": {
            "url": "https://giovanni.gsfc.nasa.gov/giovanni/",
            "description": "Interactive data selection and download"
        },
        "NASA Worldview": {
            "url": "https://worldview.earthdata.nasa.gov/",
            "description": "Visual satellite data browser"
        },
        "NASA Ocean Color": {
            "url": "https://oceancolor.gsfc.nasa.gov/",
            "description": "MODIS/VIIRS ocean data portal"
        },
        "NASA Earthdata Search": {
            "url": "https://search.earthdata.nasa.gov/",
            "description": "Search all NASA datasets"
        },
        "Direct Data Access": {
            "url": "https://oceandata.sci.gsfc.nasa.gov/MODIS-Aqua/",
            "description": "Browse MODIS files directly"
        }
    }
    
    for name, info in websites.items():
        print(f"\n🔗 {name}")
        print(f"   URL: {info['url']}")
        print(f"   Use: {info['description']}")

if __name__ == "__main__":
    print("🚀 NASA Data Download Helper")
    print("=" * 60)
    
    print("\n⚠️  SETUP REQUIRED:")
    print("1. Replace 'YOUR_NASA_PASSWORD' with your actual NASA password")
    print("2. Make sure you have a NASA Earthdata account")
    print("3. Run this script to test your connection")
    
    # Show available options
    show_nasa_websites()
    list_available_files()
    
    print("\n" + "=" * 60)
    print("💡 RECOMMENDATION: Start with NASA Giovanni - it's the easiest!")
    print("   Just go to: https://giovanni.gsfc.nasa.gov/giovanni/")
    print("   No programming required! 🎯")
