# Enhanced Shark Habitat Prediction Framework

A comprehensive mathematical framework for identifying sharks and predicting their foraging habitats using NASA satellite data.

## 🦈 Overview

This framework combines advanced oceanographic modeling, species-specific ecological parameters, and real-time NASA satellite data to predict shark habitat suitability. It's designed for marine biologists, conservation scientists, and fisheries managers.

## 🚀 Features

### Core Capabilities
- **Species-Specific Models**: Detailed ecological parameters for Great White, Tiger, and Bull sharks
- **NASA Data Integration**: Real-time access to MODIS and VIIRS satellite data
- **Advanced Habitat Modeling**: Multi-factor habitat suitability calculations
- **Comprehensive Analysis**: Statistical analysis with spatial metrics
- **ASCII Visualization**: Terminal-based habitat maps and reports

### Mathematical Models
- **Temperature Suitability**: Asymmetric Gaussian with species-specific tolerances
- **Productivity Assessment**: Prey-based energy transfer through food webs
- **Frontal Zone Detection**: Thermal gradient analysis for feeding opportunities
- **Spatial Connectivity**: Patch analysis and fragmentation metrics

## 📁 Project Structure

```
sharky/
├── enhanced_shark_framework.py      # Main framework with advanced models
├── nasa_data_integration.py         # Real NASA API integration
├── shark_analysis_visualization.py  # Analysis tools and reporting
├── shark_habitat_simple.py         # Simple working version
├── shark_habitat_implementation.py # Original complex version
├── requirements.txt                 # Python dependencies
└── README.md                       # This file
```

## 🛠️ Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install numpy pandas scipy scikit-learn matplotlib tensorflow xarray
   ```
3. **Run the framework**:
   ```bash
   python enhanced_shark_framework.py
   ```

## 🔬 Usage Examples

### Basic Habitat Prediction
```python
from enhanced_shark_framework import PredictionEngine

# Initialize for Great White Shark
engine = PredictionEngine(species='great_white')

# Define study area (California coast)
lat_range = (32.0, 42.0)
lon_range = (-125.0, -115.0)
date_range = ('2024-01-01', '2024-01-31')

# Get environmental data and predict habitat
environmental_data = {
    'sst': engine.data_fetcher.fetch_modis_sst(lat_range, lon_range, date_range),
    'chlorophyll': engine.data_fetcher.fetch_modis_chlorophyll(lat_range, lon_range, date_range)
}

results = engine.predict_habitat_suitability(environmental_data)
```

### Advanced Analysis
```python
from shark_analysis_visualization import ReportGenerator

# Generate comprehensive report
report_gen = ReportGenerator()
report = report_gen.generate_habitat_report(results, 'great_white')
print(report)
```

### NASA Data Integration
```python
from nasa_data_integration import RealTimeDataProcessor

# Get latest satellite data
processor = RealTimeDataProcessor()
bbox = (-122.5, 36.0, -121.5, 37.0)  # Monterey Bay

sst_data = processor.get_latest_sst_data(bbox, days_back=7)
chl_data = processor.get_latest_chlorophyll_data(bbox, days_back=7)
```

## 🧮 Mathematical Framework

### Habitat Suitability Index (HSI)
The framework calculates HSI using a weighted geometric mean:

```
HSI = (T^w1 × P^w2 × F^w3 × D^w4)
```

Where:
- **T**: Temperature suitability (weight: 0.30)
- **P**: Productivity suitability (weight: 0.25)
- **F**: Frontal zone suitability (weight: 0.25)
- **D**: Depth suitability (weight: 0.20)

### Temperature Model
```
T(temp) = exp(-((temp - T_opt)²) / (2σ²))
```
With asymmetric tolerance for warm/cold preferences.

### Productivity Model
Based on energy transfer through marine food webs:
```
P(chl, sst) = E_available / (E_available + K_half)
```
Where `E_available = chl × exp(0.0633 × sst) × η^(TL-1)`

## 📊 Output Examples

### Habitat Quality Distribution
```
Excellent (HSI > 0.8):      11 cells (  2.8%)
Good (HSI 0.6-0.8):         46 cells ( 11.5%)
Moderate (HSI 0.4-0.6):    101 cells ( 25.2%)
Poor (HSI 0.2-0.4):        105 cells ( 26.2%)
Unsuitable (HSI ≤ 0.2):    137 cells ( 34.2%)
```

### ASCII Habitat Map
```
█ Excellent  ▓ Good  ▒ Moderate  ░ Poor  · Unsuitable

░░░▒░·░░░░░▒░░··░▒░░
▒·░▒▒░░░▒·░····░░·░·
▒▒▒▓▒▒▒▒···░·▒···░·░
█▒░▒▓░▒░░░░▒········
▒▓░▒▒▒▓░░░░░······░·
```

## 🌊 Species Profiles

### Great White Shark (*Carcharodon carcharias*)
- **Optimal Temperature**: 18°C (±3.5°C tolerance)
- **Trophic Level**: 4.5
- **Depth Range**: 0-250m (optimal: 50m)
- **Frontal Zone Affinity**: High (0.9)

### Tiger Shark (*Galeocerdo cuvier*)
- **Optimal Temperature**: 25°C (±4.0°C tolerance)
- **Trophic Level**: 4.2
- **Depth Range**: 0-350m (optimal: 100m)
- **Coastal Affinity**: Very High (0.9)

### Bull Shark (*Carcharhinus leucas*)
- **Optimal Temperature**: 27°C (±5.0°C tolerance)
- **Trophic Level**: 4.0
- **Depth Range**: 0-150m (optimal: 30m)
- **Productivity Response**: Strong

## 🛰️ NASA Data Sources

### Supported Satellites
- **MODIS-Aqua**: Sea Surface Temperature, Chlorophyll-a
- **VIIRS**: Sea Surface Temperature, Chlorophyll-a
- **MODIS-Terra**: Photosynthetically Available Radiation

### Data Products
- **SST**: 4km resolution, daily/monthly composites
- **Chlorophyll**: 4km resolution, Level 3 mapped
- **PAR**: Photosynthetically Available Radiation
- **PIC**: Particulate Inorganic Carbon

## 📈 Analysis Features

### Spatial Metrics
- **Moran's I**: Spatial autocorrelation analysis
- **Patch Analysis**: Connected habitat identification
- **Connectivity Index**: Habitat network assessment
- **Fragmentation Index**: Landscape fragmentation

### Statistical Analysis
- **Percentile Distributions**: Habitat quality quantiles
- **Patch Metrics**: Size, connectivity, centroids
- **Quality Classification**: 5-tier habitat ranking

## 🔧 Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **NASA API Access**
   - Some APIs require authentication
   - Check network connectivity
   - Verify API endpoints are accessible

3. **Memory Issues**
   - Reduce grid resolution for large areas
   - Process data in smaller chunks

### Performance Tips
- Use background processing for large datasets
- Cache frequently accessed data
- Optimize grid resolution based on study scale

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📚 References

- NASA Ocean Color: https://oceancolor.gsfc.nasa.gov/
- MODIS Data: https://modis.gsfc.nasa.gov/
- Marine Ecology Principles: Begon et al. (2006)
- Shark Ecology: Carrier et al. (2012)

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- NASA Ocean Color Team for satellite data
- Marine biology research community
- Open source Python ecosystem

---

**Built with 🦈 for marine conservation**
