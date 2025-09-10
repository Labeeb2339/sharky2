# 🦈 SharkTracker Pro - NASA Satellite Shark Habitat Prediction

## 🌊 Discover Shark Habitats with NASA Satellite Technology

**SharkTracker Pro** is a cutting-edge marine biology tool that uses real NASA satellite data to predict and analyze shark habitats worldwide. Perfect for marine biologists, researchers, conservationists, and ocean enthusiasts.

## ✨ Powerful Features

### 🛰️ **Real NASA Satellite Data**
- Live sea surface temperature from MODIS and VIIRS satellites
- Ocean color and chlorophyll-a concentration data
- Global bathymetry and depth information
- Updated within hours of satellite passes

### 🦈 **Multi-Species Shark Analysis**
Analyze habitats for 6 major shark species:
- **Great White Shark** - Apex coastal predator
- **Tiger Shark** - Tropical generalist hunter
- **Bull Shark** - Estuarine opportunist
- **Great Hammerhead** - Specialized ray hunter
- **Shortfin Mako** - High-speed oceanic predator
- **Blue Shark** - Long-distance ocean wanderer

### 🧠 **Intelligent Habitat Modeling**
- **Temperature Preferences** - Species-specific thermal requirements
- **Prey Availability** - Food web and productivity analysis
- **Ocean Fronts** - Thermal boundaries where sharks hunt
- **Depth Preferences** - Bathymetric habitat modeling
- **Seasonal Patterns** - Temporal habitat changes

## 🚀 Quick Start Guide

### Step 1: Install SharkTracker Pro
```bash
pip install -r requirements.txt
```

### Step 2: Get Your Free NASA Access
1. Create a free NASA Earthdata account at: https://urs.earthdata.nasa.gov/users/new
2. Generate your access token (see [Token Setup Guide](NASA_TOKEN_SETUP.md))
3. Add your token to the framework

### Step 3: Start Analyzing
```bash
# Run habitat analysis
python automatic_nasa_framework.py

# Launch interactive web interface
streamlit run app.py
```

### Step 4: Explore Results
- View habitat suitability maps
- Compare different shark species
- Analyze seasonal patterns
- Export results for research

## 📖 User Guides
- **[Getting Started](USER_GUIDE.md)** - Complete beginner's guide
- **[NASA Token Setup](NASA_TOKEN_SETUP.md)** - Free NASA account setup
- **[Species Guide](SPECIES_GUIDE.md)** - Detailed shark species information
- **[Web App Tutorial](WEB_APP_GUIDE.md)** - Interactive interface guide

## 🦈 Shark Species Profiles

### 🔥 **Great White Shark** (*Carcharodon carcharias*)
- **Habitat**: Temperate coastal waters (12-24°C)
- **Hunting**: Ambush predator targeting seals and large fish
- **Behavior**: Highly migratory, follows thermal fronts
- **Best Locations**: California, South Africa, Australia

### 🌴 **Tiger Shark** (*Galeocerdo cuvier*)
- **Habitat**: Tropical coastal waters (20-30°C)
- **Hunting**: Generalist predator, eats almost anything
- **Behavior**: Coastal wanderer, active at night
- **Best Locations**: Hawaii, Caribbean, Indo-Pacific

### 🏞️ **Bull Shark** (*Carcharhinus leucas*)
- **Habitat**: Estuaries and shallow coastal waters (22-32°C)
- **Hunting**: Opportunistic, tolerates fresh water
- **Behavior**: Aggressive, territorial
- **Best Locations**: Gulf of Mexico, river mouths, shallow bays

### 🔨 **Great Hammerhead** (*Sphyrna mokarran*)
- **Habitat**: Tropical pelagic waters (21-27°C)
- **Hunting**: Specialized ray hunter with unique head shape
- **Behavior**: Schooling, highly migratory
- **Best Locations**: Bahamas, Red Sea, Indo-Pacific

### ⚡ **Shortfin Mako** (*Isurus oxyrinchus*)
- **Habitat**: Open ocean waters (15-25°C)
- **Hunting**: High-speed pursuit of tuna and billfish
- **Behavior**: Fastest shark, deep diving
- **Best Locations**: Atlantic, Pacific open ocean

### 🌊 **Blue Shark** (*Prionace glauca*)
- **Habitat**: Cool open ocean waters (10-22°C)
- **Hunting**: Opportunistic, feeds on squid and small fish
- **Behavior**: Extremely migratory, follows ocean currents
- **Best Locations**: North Atlantic, North Pacific

## 🛰️ NASA Satellite Data Sources
- **VIIRS**: Latest high-resolution ocean data (750m)
- **MODIS**: Reliable global coverage (1km resolution)
- **Historical Data**: 40+ years of climate records
- **Real-time Updates**: Fresh data every few hours

## 🎯 Key Applications

### 🔬 **Marine Research**
- Track shark migration patterns
- Study climate change impacts on marine life
- Analyze seasonal habitat shifts
- Identify critical conservation areas

### 🏛️ **Conservation & Management**
- Design marine protected areas
- Monitor shark population trends
- Assess fishing impact zones
- Plan conservation strategies

### 🎓 **Education & Outreach**
- Interactive classroom demonstrations
- Public aquarium displays
- Citizen science projects
- Marine biology education

## 🎮 How to Use SharkTracker Pro

### 🖥️ **Interactive Web Interface (Recommended)**
Perfect for beginners and visual analysis:
```bash
streamlit run app.py
```
- **Point and click** interface
- **Real-time maps** and visualizations
- **No coding required**
- **Perfect for education** and presentations

### 💻 **Command Line Analysis**
For researchers and advanced users:
```bash
python automatic_nasa_framework.py
```
- **Automated analysis** of California coast
- **Detailed scientific output**
- **Customizable parameters**
- **Perfect for research** and batch processing

### 🔬 **Custom Analysis (Python)**
For developers and scientists:
```python
from automatic_nasa_framework import AutomaticNASAFramework

# Initialize SharkTracker Pro
framework = AutomaticNASAFramework()

# Analyze any location for any species
results = framework.analyze_shark_habitat(
    species='great_white',
    bounds=[-125, 32, -117, 42],  # California coast
    date_range=('2024-01-01', '2024-01-31')
)

# Results include habitat maps, statistics, and environmental data
print(f"Best habitat areas found: {results['suitable_cells']} locations")
```

## 🧠 How SharkTracker Pro Works

### 🔬 **The Science Behind the Magic**

SharkTracker Pro combines multiple environmental factors to predict where sharks are most likely to be found:

#### 🌡️ **Water Temperature**
- Each shark species has preferred temperature ranges
- We use NASA satellite data to map ocean temperatures
- Thermal fronts (temperature boundaries) are shark highways

#### 🐟 **Food Availability**
- Sharks follow the food chain
- Chlorophyll levels indicate plankton → fish → sharks
- Ocean productivity drives the entire ecosystem

#### 🌊 **Ocean Features**
- Upwelling zones bring nutrients to the surface
- Ocean currents create migration routes
- Seamounts and drop-offs concentrate marine life

#### 🏔️ **Depth & Seafloor**
- Different species prefer different depths
- Continental shelves are shark hunting grounds
- Underwater topography affects water flow and prey

### 🎯 **Habitat Suitability Scoring**
We combine all these factors into a single score (0-100%):
- **90-100%**: 🟢 Excellent habitat - sharks love it here!
- **70-90%**: 🟢 Very good habitat - high shark activity expected
- **50-70%**: 🟡 Good habitat - moderate shark presence
- **30-50%**: 🟠 Marginal habitat - occasional shark visits
- **0-30%**: 🔴 Poor habitat - sharks rarely found here

## 🌟 What Makes SharkTracker Pro Special

### 🛰️ **Real NASA Satellite Data**
- **Live ocean data** updated every few hours
- **40+ years** of historical records for climate studies
- **Global coverage** from multiple NASA satellites
- **Research-grade quality** used by scientists worldwide

### 🦈 **Species-Specific Intelligence**
- **6 major shark species** with unique behavioral models
- **Literature-based parameters** from marine biology research
- **Seasonal patterns** and migration timing
- **Habitat preferences** based on decades of field studies

### 🎯 **Professional Accuracy**
- **Validated models** used in marine research
- **Quality control** removes bad data automatically
- **Uncertainty estimates** show confidence levels
- **Peer-reviewed methods** from published scientific papers

## 🌊 Species Profiles

### Great White Shark (*Carcharodon carcharias*)
- **Optimal Temperature**: 18.0°C (±3.5°C tolerance)
- **Trophic Level**: 4.5 (apex predator)
- **Habitat**: Temperate coastal waters
- **Depth Range**: 0-250m (optimal: 50m)
- **Behavior**: Ambush predator, high migration

### Tiger Shark (*Galeocerdo cuvier*)
- **Optimal Temperature**: 25.0°C (±4.0°C tolerance)
- **Trophic Level**: 4.2 (generalist predator)
- **Habitat**: Tropical coastal waters
- **Depth Range**: 0-350m (optimal: 100m)
- **Behavior**: Generalist predator, coastal affinity

### Bull Shark (*Carcharhinus leucas*)
- **Optimal Temperature**: 27.0°C (±5.0°C tolerance)
- **Trophic Level**: 4.0 (opportunistic predator)
- **Habitat**: Estuarine and coastal waters
- **Depth Range**: 0-150m (optimal: 30m)
- **Behavior**: Opportunistic, freshwater tolerance

### Great Hammerhead Shark (*Sphyrna mokarran*)
- **Optimal Temperature**: 24.0°C (±3.0°C tolerance)
- **Trophic Level**: 4.3 (specialized predator)
- **Habitat**: Tropical pelagic waters
- **Depth Range**: 0-300m (optimal: 80m)
- **Behavior**: Specialized predator, schooling

### Shortfin Mako Shark (*Isurus oxyrinchus*)
- **Optimal Temperature**: 20.0°C (±4.5°C tolerance)
- **Trophic Level**: 4.6 (high-speed predator)
- **Habitat**: Pelagic oceanic waters
- **Depth Range**: 0-500m (optimal: 150m)
- **Behavior**: High-speed predator, highly migratory

### Blue Shark (*Prionace glauca*)
- **Optimal Temperature**: 16.0°C (±6.0°C tolerance)
- **Trophic Level**: 3.8 (opportunistic pelagic)
- **Habitat**: Open ocean waters
- **Depth Range**: 0-400m (optimal: 200m)
- **Behavior**: Opportunistic, highly migratory

## 🆘 Need Help?

### 🔧 **Common Issues**

#### "Token expired" error
- Your NASA access needs renewal (every 2-3 months)
- See [NASA Token Setup Guide](NASA_TOKEN_SETUP.md) for quick renewal
- Takes just 2 minutes to fix!

#### "No data available"
- Check that your study area is over ocean (not land)
- Try a different date range
- Some remote areas may have limited satellite coverage

#### Web app won't start
- Try: `streamlit run app.py --server.port 8502`
- Make sure all dependencies are installed: `pip install -r requirements.txt`

### 💡 **Getting Better Results**
- **Choose the right species** for your location (tropical vs temperate)
- **Use appropriate time periods** (consider seasonal patterns)
- **Start with smaller areas** for detailed analysis
- **Check our species guide** for location recommendations

### 📚 **Learn More**
- **[Complete User Guide](USER_GUIDE.md)** - Everything you need to know
- **[Species Guide](SPECIES_GUIDE.md)** - Detailed shark information
- **[Web App Tutorial](WEB_APP_GUIDE.md)** - Step-by-step interface guide
- **[NASA Token Setup](NASA_TOKEN_SETUP.md)** - Account setup and renewal

---

## 🎓 Perfect for Education & Research

### 👨‍🏫 **Educators**
- **Interactive classroom demonstrations**
- **Student research projects**
- **Marine biology curriculum**
- **STEM education activities**

### 🔬 **Researchers**
- **Habitat modeling studies**
- **Climate change research**
- **Conservation planning**
- **Migration pattern analysis**

### 🌊 **Marine Enthusiasts**
- **Citizen science projects**
- **Dive planning assistance**
- **Ocean exploration**
- **Wildlife photography planning**

---

## 🌍 Join the SharkTracker Community

**SharkTracker Pro** - Making NASA satellite technology accessible for marine conservation and education.

**Ready to discover the secret lives of sharks?** 🦈🛰️

---

*Built with 🌊 for ocean conservation and 🦈 for shark protection*
