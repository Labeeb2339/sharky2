# 📖 API Reference

## 🎯 Overview
Complete API reference for the NASA Shark Habitat Prediction Framework classes and methods.

---

## 🏗️ AutomaticNASAFramework Class

### Constructor
```python
AutomaticNASAFramework(jwt_token=None)
```

**Parameters:**
- `jwt_token` (str): NASA Earthdata JWT token for API authentication

**Example:**
```python
framework = AutomaticNASAFramework("eyJ0eXAiOiJKV1QiLCJvcmlnaW4...")
```

### Main Methods

#### `analyze_shark_habitat(species, bounds, date_range)`
Perform complete shark habitat analysis for specified species and region.

**Parameters:**
- `species` (str): Shark species ('great_white', 'tiger', 'bull', 'hammerhead', 'mako', 'blue')
- `bounds` (list): Geographic bounds [west, south, east, north] in decimal degrees
- `date_range` (tuple): Date range ('start_date', 'end_date') in 'YYYY-MM-DD' format

**Returns:**
- `dict`: Complete analysis results with HSI grid, statistics, and metadata

**Example:**
```python
results = framework.analyze_shark_habitat(
    species='great_white',
    bounds=[-125, 32, -117, 42],
    date_range=('2024-01-01', '2024-01-31')
)
```

#### `auto_download_nasa_data(bounds, date_range)`
Download and process real NASA satellite data for specified region and time.

**Parameters:**
- `bounds` (list): Geographic bounds [west, south, east, north]
- `date_range` (tuple): Date range ('start_date', 'end_date')

**Returns:**
- `dict`: Environmental data including SST, chlorophyll, and bathymetry

**Example:**
```python
env_data = framework.auto_download_nasa_data(
    bounds=[-125, 32, -117, 42],
    date_range=('2024-01-01', '2024-01-07')
)
```

### Data Processing Methods

#### `_download_real_sst_grid(bounds, grid_size)`
Download real NASA MODIS SST data with enhanced NetCDF processing.

**Parameters:**
- `bounds` (list): Geographic bounds
- `grid_size` (int): Grid resolution (default: 25)

**Returns:**
- `numpy.ndarray`: SST data grid or None if failed

#### `_download_real_chl_grid(bounds, grid_size)`
Download real NASA MODIS Chlorophyll data with enhanced NetCDF processing.

**Parameters:**
- `bounds` (list): Geographic bounds
- `grid_size` (int): Grid resolution (default: 25)

**Returns:**
- `numpy.ndarray`: Chlorophyll data grid or None if failed

#### `_download_real_bathymetry_data(bounds, grid_size)`
Download real NOAA ETOPO bathymetry data.

**Parameters:**
- `bounds` (list): Geographic bounds
- `grid_size` (int): Grid resolution (default: 25)

**Returns:**
- `numpy.ndarray`: Bathymetry data grid

### Enhanced NetCDF Processing

#### `_process_netcdf_granule(granule, bounds, variable_type)`
Process NASA granule with full NetCDF data extraction.

**Parameters:**
- `granule` (dict): NASA CMR granule metadata
- `bounds` (list): Geographic bounds for subsetting
- `variable_type` (str): Variable type ('sst' or 'chlorophyll')

**Returns:**
- `dict`: NetCDF data with coordinates and metadata or None if failed

#### `_apply_quality_control(data, quality_flags)`
Apply NASA-standard quality control with quality flags.

**Parameters:**
- `data` (numpy.ndarray): Raw satellite data
- `quality_flags` (numpy.ndarray): NASA quality flags

**Returns:**
- `numpy.ndarray`: Quality-controlled data with invalid values masked

### Mathematical Models

#### `_calculate_temperature_suitability(sst_grid, species)`
Calculate temperature suitability using Sharpe-Schoolfield bioenergetic model.

**Parameters:**
- `sst_grid` (numpy.ndarray): Sea surface temperature grid
- `species` (str): Shark species identifier

**Returns:**
- `numpy.ndarray`: Temperature suitability values (0-1)

#### `_calculate_productivity_suitability(chl_grid, sst_grid, species)`
Calculate productivity suitability using Eppley + Michaelis-Menten models.

**Parameters:**
- `chl_grid` (numpy.ndarray): Chlorophyll-a concentration grid
- `sst_grid` (numpy.ndarray): Sea surface temperature grid
- `species` (str): Shark species identifier

**Returns:**
- `numpy.ndarray`: Productivity suitability values (0-1)

#### `_detect_frontal_zones(sst_grid, species)`
Detect thermal frontal zones using multi-scale gradient analysis.

**Parameters:**
- `sst_grid` (numpy.ndarray): Sea surface temperature grid
- `species` (str): Shark species identifier

**Returns:**
- `numpy.ndarray`: Frontal zone suitability values (0-1)

#### `_calculate_depth_suitability(bathymetry_grid, species)`
Calculate depth suitability based on species-specific depth preferences.

**Parameters:**
- `bathymetry_grid` (numpy.ndarray): Bathymetry data grid
- `species` (str): Shark species identifier

**Returns:**
- `numpy.ndarray`: Depth suitability values (0-1)

#### `_calculate_hsi(temp_suit, prod_suit, frontal_suit, depth_suit, species)`
Calculate Habitat Suitability Index using weighted geometric mean.

**Parameters:**
- `temp_suit` (numpy.ndarray): Temperature suitability grid
- `prod_suit` (numpy.ndarray): Productivity suitability grid
- `frontal_suit` (numpy.ndarray): Frontal zone suitability grid
- `depth_suit` (numpy.ndarray): Depth suitability grid
- `species` (str): Shark species identifier

**Returns:**
- `numpy.ndarray`: HSI values (0-1)

---

## 🚀 EnhancedNASAFramework Class

### Constructor
```python
EnhancedNASAFramework(jwt_token)
```

**Parameters:**
- `jwt_token` (str): NASA Earthdata JWT token

### Main Methods

#### `get_enhanced_data(bounds, date_range, variables, quality_level=2)`
Get enhanced NASA data with full NetCDF processing and quality control.

**Parameters:**
- `bounds` (list): Geographic bounds [west, south, east, north]
- `date_range` (tuple): Date range ('start_date', 'end_date')
- `variables` (list): Variables to retrieve ['sst', 'chlorophyll']
- `quality_level` (int): Quality level (1=basic, 2=standard, 3=highest)

**Returns:**
- `dict`: Enhanced data with quality statistics and metadata

**Example:**
```python
enhanced_framework = EnhancedNASAFramework("YOUR_TOKEN")
data = enhanced_framework.get_enhanced_data(
    bounds=[-125, 32, -117, 42],
    date_range=('2024-01-01', '2024-01-07'),
    variables=['sst', 'chlorophyll'],
    quality_level=3
)
```

---

## 🌐 Streamlit Web Application

### Launch Command
```bash
streamlit run app.py
```

### Interface Components

#### Species Selection
- Dropdown menu with 6 shark species
- Species-specific parameter display
- Real-time parameter updates

#### Geographic Controls
- Latitude/longitude range sliders
- Predefined region buttons
- Interactive map display

#### Temporal Controls
- Date range picker
- Temporal resolution selection
- Real-time data toggle

#### Analysis Controls
- Grid resolution slider
- Quality level selection
- Processing options

#### Results Display
- HSI statistics table
- Habitat quality distribution
- Interactive plots and maps
- Downloadable results

---

## 🔧 Utility Functions

### Token Management
```python
def check_token_expiry(token):
    """Check if NASA JWT token is expired"""
    import jwt
    import datetime
    
    payload = jwt.decode(token, options={'verify_signature': False})
    exp_time = datetime.datetime.fromtimestamp(payload['exp'])
    return exp_time < datetime.datetime.now()
```

### Data Validation
```python
def validate_bounds(bounds):
    """Validate geographic bounds"""
    if len(bounds) != 4:
        raise ValueError("Bounds must be [west, south, east, north]")
    if bounds[0] >= bounds[2] or bounds[1] >= bounds[3]:
        raise ValueError("Invalid bounds: west < east, south < north")
    return True
```

### Grid Processing
```python
def interpolate_to_grid(data, coords, target_grid):
    """Interpolate irregular data to regular grid"""
    from scipy.interpolate import griddata
    
    points = np.column_stack((coords['lon'].flatten(), coords['lat'].flatten()))
    values = data.flatten()
    
    # Remove NaN values
    valid_mask = ~np.isnan(values)
    if np.sum(valid_mask) < 10:
        return None
    
    return griddata(
        points[valid_mask], 
        values[valid_mask], 
        target_grid, 
        method='linear'
    )
```

---

## 📊 Data Structures

### Analysis Results
```python
results = {
    'hsi_grid': numpy.ndarray,           # 2D HSI values (grid_size x grid_size)
    'mean_hsi': float,                   # Mean HSI value
    'max_hsi': float,                    # Maximum HSI value
    'std_hsi': float,                    # HSI standard deviation
    'suitable_cells': int,               # Number of suitable cells (HSI > 0.4)
    'total_cells': int,                  # Total analysis cells
    'habitat_distribution': {            # Habitat quality distribution
        'excellent': int,                # HSI > 0.8
        'good': int,                     # HSI 0.6-0.8
        'moderate': int,                 # HSI 0.4-0.6
        'poor': int,                     # HSI 0.2-0.4
        'unsuitable': int                # HSI ≤ 0.2
    },
    'environmental_data': {              # Source environmental data
        'sst': numpy.ndarray,            # Sea surface temperature
        'chlorophyll': numpy.ndarray,    # Chlorophyll-a concentration
        'bathymetry': numpy.ndarray      # Bathymetry data
    },
    'processing_metadata': {             # Processing information
        'species': str,                  # Analyzed species
        'bounds': list,                  # Geographic bounds
        'date_range': tuple,             # Analysis date range
        'grid_size': int,                # Grid resolution
        'data_sources': dict,            # Data source information
        'quality_stats': dict            # Quality control statistics
    }
}
```

### Environmental Data
```python
environmental_data = {
    'sst': {
        'data': numpy.ndarray,           # Temperature data
        'units': 'degrees_celsius',      # Data units
        'source': 'NASA MODIS Aqua',    # Data source
        'quality': float                 # Data quality percentage
    },
    'chlorophyll': {
        'data': numpy.ndarray,           # Chlorophyll data
        'units': 'mg/m^3',              # Data units
        'source': 'NASA MODIS Aqua',    # Data source
        'quality': float                 # Data quality percentage
    },
    'bathymetry': {
        'data': numpy.ndarray,           # Depth data
        'units': 'meters',               # Data units
        'source': 'NOAA ETOPO',         # Data source
        'resolution': '15_arc_second'    # Data resolution
    }
}
```

---

## ⚠️ Error Handling

### Common Exceptions
- `TokenExpiredError`: NASA JWT token has expired
- `DataNotAvailableError`: Requested data not available for date/region
- `NetworkError`: Network connectivity issues
- `ProcessingError`: Data processing failures

### Error Recovery
- Automatic fallback to metadata processing if NetCDF fails
- Retry mechanisms for network issues
- Graceful degradation for missing data
- Comprehensive error logging

---

## 🏆 Best Practices

### Performance Optimization
- Use appropriate grid resolution for study scale
- Cache frequently accessed data
- Process data in chunks for large regions
- Use quality_level=1 for faster processing

### Data Quality
- Always check quality statistics in results
- Use quality_level=3 for research applications
- Validate results against known habitat areas
- Consider temporal variability in analysis

### Token Management
- Check token expiry before long analyses
- Use environment variables for production
- Monitor API usage to avoid rate limits
- Refresh tokens proactively

**This API provides comprehensive access to NASA satellite data and advanced shark habitat modeling capabilities for competition-grade analysis.** 🛰️🦈🏆
