# 🦈 Shark Habitat Prediction Web App

A comprehensive web application for predicting shark foraging habitats using NASA satellite data with an interactive dashboard.

## 🌟 Features

- **Interactive Web Interface**: User-friendly Streamlit dashboard
- **Real-time Analysis**: Generate habitat predictions on demand
- **Species Selection**: Great White, Tiger Shark, and Bull Shark models
- **Interactive Maps**: Plotly-powered habitat suitability visualizations
- **NASA Data Integration**: Real-time satellite data from MODIS and VIIRS sensors
- **Custom Study Areas**: Define analysis boundaries with lat/lon controls
- **Professional Reports**: Detailed analysis with management recommendations

## 🚀 Live Demo

**Deploy this app to Streamlit Cloud for free!**

## 🛠️ Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/shark-habitat-app.git
cd shark-habitat-app

# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Cloud Deployment on Streamlit Cloud

1. **Create GitHub Repository**:
   - Push this code to a new GitHub repository
   - Make sure `app.py` and `requirements.txt` are in the root

2. **Deploy to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live at**: `https://your-app-name.streamlit.app`

## 📊 How It Works

### 1. Species-Specific Modeling
- **Great White Shark**: Optimal temp 15-20°C, high chlorophyll preference
- **Tiger Shark**: Optimal temp 22-28°C, moderate chlorophyll preference  
- **Bull Shark**: Optimal temp 20-30°C, variable chlorophyll tolerance

### 2. NASA Satellite Data
- Sea Surface Temperature (SST) from MODIS/VIIRS
- Chlorophyll-a concentration for productivity analysis
- Real-time data quality assessment

### 3. Habitat Suitability Index (HSI)
- Mathematical models combining temperature and productivity
- Species-specific ecological parameters
- Spatial analysis and connectivity metrics

## 🗂️ Project Structure

```
shark-habitat-app/
├── app.py                          # Main Streamlit web application
├── enhanced_shark_framework.py     # Core prediction algorithms
├── nasa_data_integration.py        # NASA API integration
├── shark_analysis_visualization.py # Analysis and visualization tools
├── requirements.txt               # Python dependencies
└── README.md                     # Documentation
```

## 🔧 Technical Stack

- **Frontend**: Streamlit with custom CSS
- **Visualization**: Plotly for interactive maps and charts
- **Data Processing**: Pandas, NumPy, SciPy
- **Machine Learning**: Scikit-learn, TensorFlow
- **NASA APIs**: Ocean Color, MODIS, VIIRS data
- **Deployment**: Streamlit Cloud

## 📈 Usage

1. **Select Species**: Choose from Great White, Tiger, or Bull Shark
2. **Define Study Area**: Set latitude/longitude boundaries
3. **Choose Date Range**: Select analysis period
4. **Generate Analysis**: Click "Analyze Habitat" for real-time predictions
5. **Explore Results**: Interactive maps, charts, and detailed reports

## 🌍 Environmental Impact

This tool helps marine biologists and conservationists:
- Identify critical shark habitats
- Plan marine protected areas
- Monitor ecosystem changes
- Support sustainable fishing practices

## 🚀 Deployment Instructions

### Step-by-Step GitHub + Streamlit Cloud Deployment

1. **Initialize Git Repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Shark Habitat Prediction App"
   ```

2. **Create GitHub Repository**:
   - Go to [github.com](https://github.com) and create a new repository
   - Name it something like `shark-habitat-app`
   - Don't initialize with README (you already have one)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/yourusername/shark-habitat-app.git
   git branch -M main
   git push -u origin main
   ```

4. **Deploy to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy!"

5. **Your app will be live!** 🎉

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- NASA Ocean Color Program
- MODIS and VIIRS satellite missions
- Marine ecology research community
- Streamlit team for the amazing framework

---

**Made with ❤️ for marine conservation**
