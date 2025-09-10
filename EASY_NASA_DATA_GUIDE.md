# 🛰️ **Easy Guide: How to Download Real NASA Satellite Data**

## 🎯 **Quick Start (5 Minutes)**

### **Method 1: NASA Giovanni (Easiest - No Programming!)**

1. **Go to**: https://giovanni.gsfc.nasa.gov/giovanni/
2. **Select Data**:
   - **Variables**: Sea Surface Temperature, Chlorophyll-a
   - **Satellite**: MODIS-Aqua
   - **Time Range**: Pick your dates
   - **Region**: Draw box on map (California coast: 32°N-42°N, 125°W-115°W)
3. **Click "Plot Data"**
4. **Download**: Click "Data Download" → Get NetCDF files
5. **Done!** ✅

### **Method 2: NASA Worldview (Visual Selection)**

1. **Go to**: https://worldview.earthdata.nasa.gov/
2. **Add Layers**: Sea Surface Temperature, Chlorophyll-a
3. **Set Date**: Use time slider
4. **Select Area**: Draw rectangle
5. **Download**: Click "Download" → Get image or data files

---

## 🔑 **Method 3: Direct API Download (Your JWT Token)**

You already have a working NASA JWT token! Here's how to use it:

### **Step 1: Simple Python Script**

```python
import requests

# Your working JWT token
JWT_TOKEN = "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6ImxhYmVlYjIzMzkiLCJleHAiOjE3NjI3MzI3OTksImlhdCI6MTc1NzUwMTI1MSwiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292IiwiaWRlbnRpdHlfcHJvdmlkZXIiOiJlZGxfb3BzIiwiYWNyIjoiZWRsIiwiYXNzdXJhbmNlX2xldmVsIjozfQ.PIg6AGXJRSs4ql-VOnIAQaOE-v-Y18uSwk-OWPBYM7_AiItzkXbdtInGpStAcOhCqa9NooTXVonhC-DbttTzlGAMjTOvrlOx0lGQkUP8aEwnsC3yTlI6QC6fQ7O5AuAvpcjVR1Tgh8frdRl7aUZuVSEjZtrlmJgl-TZXkctmO9izbH0M5rCxCLaTjAbEkvruv7XcRTYxzrMyhLIUeNqDUBJvxhpWFjXkcBW6Rla6rm_aWKk1TXY-S6NrGBTtcYime3IW6cdBlV65gX2Qbg2F6oqDzPUrNfSk2I_I7RB22esLq6-jBJDBAibg2qJtLo3EeXfJNU8FwJubVVQTjIA_8w"

headers = {
    'Authorization': f'Bearer {JWT_TOKEN}',
    'Accept': 'application/json'
}

# Search for files
search_url = "https://cmr.earthdata.nasa.gov/search/granules.json"
params = {
    'collection_concept_id': 'C1200034768-OB_DAAC',  # MODIS SST
    'temporal': '2024-01-01T00:00:00Z,2024-01-07T23:59:59Z',
    'bounding_box': '-125,32,-115,42',  # California coast
    'page_size': 5
}

response = requests.get(search_url, params=params, headers=headers)
files = response.json()

print(f"Found {len(files.get('feed', {}).get('entry', []))} files")
```

### **Step 2: Download Files**

```python
# Download a specific file
file_url = "https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20240101.L3m_DAY_SST_sst_4km.nc"

response = requests.get(file_url, headers=headers, stream=True)

if response.status_code == 200:
    with open("nasa_sst_data.nc", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("✅ Downloaded NASA file!")
```

---

## 📊 **What Files to Download**

### **For Shark Habitat Prediction:**

#### **Sea Surface Temperature (SST):**
- **Product**: MODIS Aqua Level 3 SST
- **Resolution**: 4km daily or 9km 8-day
- **Format**: NetCDF (.nc)
- **Variables**: `sst` (sea surface temperature)

#### **Chlorophyll-a (Ocean Color):**
- **Product**: MODIS Aqua Level 3 Ocean Color
- **Resolution**: 4km daily or 9km 8-day  
- **Format**: NetCDF (.nc)
- **Variables**: `chlor_a` (chlorophyll-a concentration)

### **File Naming Convention:**
```
A20240101.L3m_DAY_SST_sst_4km.nc
│ │      │   │   │   │   │
│ │      │   │   │   │   └── Resolution
│ │      │   │   │   └────── Variable
│ │      │   │   └────────── Product type
│ │      │   └────────────── Temporal (DAY/8D/MO)
│ │      └────────────────── Processing level
│ └───────────────────────── Date (YYYYMMDD)
└─────────────────────────── Satellite (A=Aqua, T=Terra)
```

---

## 🌍 **Popular Study Areas**

### **Coordinates for Your Framework:**

```python
study_areas = {
    'california_coast': [-125.0, 32.0, -115.0, 42.0],
    'florida_keys': [-82.0, 24.0, -80.0, 26.0],
    'great_barrier_reef': [142.0, -24.0, 154.0, -10.0],
    'south_africa': [15.0, -35.0, 32.0, -30.0],
    'hawaii': [-161.0, 18.0, -154.0, 22.5]
}
```

---

## 🔧 **Processing NASA Files**

### **Read NetCDF Files (Python):**

```python
import xarray as xr
import numpy as np

# Open NASA NetCDF file
ds = xr.open_dataset('nasa_sst_data.nc')

# Extract data
sst_data = ds['sst'].values  # Temperature data
lats = ds['lat'].values      # Latitudes  
lons = ds['lon'].values      # Longitudes

# Basic info
print(f"Data shape: {sst_data.shape}")
print(f"Temperature range: {np.nanmin(sst_data):.1f} to {np.nanmax(sst_data):.1f}°C")
print(f"Coverage: {lats.min():.1f}°N to {lats.max():.1f}°N")
```

---

## 💡 **Pro Tips**

### **Start Small:**
1. **Download 1-2 files first** to test your processing
2. **Use monthly composites** (less files, better coverage)
3. **Check data quality flags** in NetCDF files

### **Avoid Common Issues:**
- ❌ **Don't download too many files at once** (NASA has rate limits)
- ❌ **Don't ignore cloud masking** (use quality flags)
- ❌ **Don't mix different processing versions** (stick to R2022.0)

### **Best Practices:**
- ✅ **Use 8-day composites** for better spatial coverage
- ✅ **Download both day and night SST** for complete coverage
- ✅ **Check NASA status page** before bulk downloads
- ✅ **Store files organized by date/product**

---

## 🚀 **Quick Commands**

### **Using wget (Command Line):**
```bash
# Download with your credentials
wget --user=labeeb2339 --password=YOUR_PASSWORD \
  "https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20240101.L3m_DAY_SST_sst_4km.nc"
```

### **Using curl:**
```bash
curl -u labeeb2339:YOUR_PASSWORD \
  "https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20240101.L3m_DAY_SST_sst_4km.nc" \
  -o nasa_sst_data.nc
```

---

## 🎯 **For Your NASA Competition**

### **Recommended Approach:**

1. **Use Giovanni** to explore data and identify good files
2. **Download 5-10 files** covering your study period
3. **Process with your mathematical framework**
4. **Show real NASA data integration** in your presentation

### **Competition Advantage:**
- ✅ **Real NASA data** (not synthetic)
- ✅ **Proper data citations** (NASA MODIS/VIIRS)
- ✅ **Quality control** (using NASA flags)
- ✅ **Professional approach** (following NASA standards)

---

## 📞 **Need Help?**

- **NASA Giovanni Support**: https://giovanni.gsfc.nasa.gov/giovanni/doc/UsersManualworkingdocument.html
- **NASA Earthdata Forum**: https://forum.earthdata.nasa.gov/
- **MODIS Ocean Color**: https://oceancolor.gsfc.nasa.gov/

**Your JWT token is working - you're ready to download real NASA data!** 🛰️🦈
