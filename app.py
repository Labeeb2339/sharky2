#!/usr/bin/env python3
"""
Shark Habitat Prediction Web Application
Interactive UI for visualizing shark habitat suitability data
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, date
import json
import os
from enhanced_shark_framework import PredictionEngine
from shark_analysis_visualization import HabitatAnalyzer, ReportGenerator

# Configure Streamlit page
st.set_page_config(
    page_title="🦈 Shark Habitat Predictor",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .species-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }

    /* Fix dropdown text visibility */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Fix dropdown options */
    .stSelectbox > div > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Fix dropdown menu */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Fix dropdown text */
    div[data-baseweb="select"] > div > div {
        color: #000000 !important;
    }

    /* Fix dropdown options list */
    ul[role="listbox"] {
        background-color: #ffffff !important;
    }

    ul[role="listbox"] li {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    ul[role="listbox"] li:hover {
        background-color: #e6f3ff !important;
        color: #000000 !important;
    }

    /* Additional fixes for Streamlit selectbox */
    .stSelectbox label {
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* Force dark text in all selectbox elements */
    .stSelectbox div[data-testid="stSelectbox"] > div > div {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    /* Fix for the actual dropdown text */
    .stSelectbox div[role="button"] {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    /* Ensure dropdown arrow is visible */
    .stSelectbox svg {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

def load_species_data():
    """Load species information for the UI"""
    return {
        'great_white': {
            'name': 'Great White Shark',
            'scientific': 'Carcharodon carcharias',
            'optimal_temp': 18,
            'temp_range': '14-22°C',
            'depth_range': '0-250m',
            'habitat': 'Coastal and offshore waters',
            'emoji': '🦈'
        },
        'tiger_shark': {
            'name': 'Tiger Shark',
            'scientific': 'Galeocerdo cuvier',
            'optimal_temp': 25,
            'temp_range': '21-29°C',
            'depth_range': '0-350m',
            'habitat': 'Tropical and subtropical waters',
            'emoji': '🐅'
        },
        'bull_shark': {
            'name': 'Bull Shark',
            'scientific': 'Carcharhinus leucas',
            'optimal_temp': 27,
            'temp_range': '22-32°C',
            'depth_range': '0-150m',
            'habitat': 'Coastal waters and rivers',
            'emoji': '🐂'
        }
    }

def create_habitat_map(results, species_info):
    """Create an interactive habitat suitability map"""
    hsi_grid = results['hsi']
    lats = results.get('latitudes', np.linspace(32, 42, len(hsi_grid)))
    lons = results.get('longitudes', np.linspace(-125, -115, len(hsi_grid[0])))
    
    # Create meshgrid for plotting
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # Flatten arrays for plotting
    lat_flat = lat_grid.flatten()
    lon_flat = lon_grid.flatten()
    hsi_flat = np.array(hsi_grid).flatten()
    
    # Create DataFrame
    df = pd.DataFrame({
        'Latitude': lat_flat,
        'Longitude': lon_flat,
        'HSI': hsi_flat,
        'Quality': ['Excellent' if h > 0.8 else 'Good' if h > 0.6 else 'Moderate' if h > 0.4 else 'Poor' if h > 0.2 else 'Unsuitable' for h in hsi_flat]
    })
    
    # Create the map
    fig = px.scatter_mapbox(
        df, 
        lat="Latitude", 
        lon="Longitude", 
        color="HSI",
        size="HSI",
        hover_data=["Quality"],
        color_continuous_scale="Viridis",
        size_max=15,
        zoom=6,
        title=f"{species_info['emoji']} {species_info['name']} Habitat Suitability"
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        height=600,
        title_font_size=20
    )
    
    return fig

def create_hsi_distribution(results):
    """Create HSI distribution histogram"""
    hsi_flat = np.array(results['hsi']).flatten()
    
    fig = px.histogram(
        x=hsi_flat,
        nbins=30,
        title="Habitat Suitability Index Distribution",
        labels={'x': 'HSI Value', 'y': 'Frequency'},
        color_discrete_sequence=['#1f77b4']
    )
    
    fig.add_vline(x=np.mean(hsi_flat), line_dash="dash", line_color="red", 
                  annotation_text=f"Mean: {np.mean(hsi_flat):.3f}")
    
    return fig

def create_quality_pie_chart(results):
    """Create habitat quality distribution pie chart"""
    hsi_flat = np.array(results['hsi']).flatten()
    
    excellent = np.sum(hsi_flat > 0.8)
    good = np.sum((hsi_flat > 0.6) & (hsi_flat <= 0.8))
    moderate = np.sum((hsi_flat > 0.4) & (hsi_flat <= 0.6))
    poor = np.sum((hsi_flat > 0.2) & (hsi_flat <= 0.4))
    unsuitable = np.sum(hsi_flat <= 0.2)
    
    labels = ['Excellent', 'Good', 'Moderate', 'Poor', 'Unsuitable']
    values = [excellent, good, moderate, poor, unsuitable]
    colors = ['#2E8B57', '#32CD32', '#FFD700', '#FF8C00', '#DC143C']
    
    fig = px.pie(
        values=values,
        names=labels,
        title="Habitat Quality Distribution",
        color_discrete_sequence=colors
    )
    
    return fig

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🦈 Shark Habitat Prediction System</h1>', unsafe_allow_html=True)
    st.markdown("**Powered by NASA Satellite Data & Advanced Marine Ecology Models**")
    st.info("🔄 **Live Demo**: This app auto-updates when code changes are pushed to GitHub!")
    
    # Sidebar for controls
    st.sidebar.header("🎛️ Analysis Controls")
    
    # Species selection with better visibility
    species_data = load_species_data()
    species_options = {f"{info['emoji']} {info['name']}": key for key, info in species_data.items()}

    # Add custom styling for the selectbox
    st.sidebar.markdown("**🦈 Select Shark Species:**")
    selected_species_display = st.sidebar.selectbox(
        "Choose species",
        list(species_options.keys()),
        label_visibility="collapsed"
    )
    selected_species = species_options[selected_species_display]
    species_info = species_data[selected_species]
    
    # Study area controls
    st.sidebar.subheader("📍 Study Area")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        lat_min = st.number_input("Min Latitude", value=32.0, step=0.1)
        lon_min = st.number_input("Min Longitude", value=-125.0, step=0.1)
    with col2:
        lat_max = st.number_input("Max Latitude", value=42.0, step=0.1)
        lon_max = st.number_input("Max Longitude", value=-115.0, step=0.1)
    
    # Date range
    st.sidebar.subheader("📅 Time Period")
    start_date = st.sidebar.date_input("Start Date", value=date(2024, 1, 1))
    end_date = st.sidebar.date_input("End Date", value=date(2024, 1, 31))
    
    # Analysis button
    run_analysis = st.sidebar.button("🚀 Run Analysis", type="primary")
    
    # Species information card
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div class="species-card">
        <h3>{species_info['emoji']} {species_info['name']}</h3>
        <p><strong>Scientific:</strong> <em>{species_info['scientific']}</em></p>
        <p><strong>Optimal Temp:</strong> {species_info['optimal_temp']}°C</p>
        <p><strong>Temp Range:</strong> {species_info['temp_range']}</p>
        <p><strong>Depth Range:</strong> {species_info['depth_range']}</p>
        <p><strong>Habitat:</strong> {species_info['habitat']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    if run_analysis:
        with st.spinner(f"🔄 Analyzing {species_info['name']} habitat..."):
            try:
                # Initialize prediction engine
                engine = PredictionEngine(species=selected_species)
                
                # Get environmental data
                lat_range = (lat_min, lat_max)
                lon_range = (lon_min, lon_max)
                date_range = (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                
                # Fetch data
                sst_data = engine.data_fetcher.fetch_modis_sst(lat_range, lon_range, date_range)
                chl_data = engine.data_fetcher.fetch_modis_chlorophyll(lat_range, lon_range, date_range)
                environmental_data = {'sst': sst_data, 'chlorophyll': chl_data}
                
                # Predict habitat
                results = engine.predict_habitat_suitability(environmental_data)
                
                # Calculate statistics
                hsi_flat = np.array(results['hsi']).flatten()
                mean_hsi = np.mean(hsi_flat)
                max_hsi = np.max(hsi_flat)
                min_hsi = np.min(hsi_flat)
                
                # Display metrics
                st.success("✅ Analysis Complete!")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Mean HSI", f"{mean_hsi:.3f}")
                with col2:
                    st.metric("Max HSI", f"{max_hsi:.3f}")
                with col3:
                    st.metric("Min HSI", f"{min_hsi:.3f}")
                with col4:
                    st.metric("Grid Points", len(hsi_flat))
                
                # Create tabs for different visualizations
                tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Habitat Map", "📊 Distribution", "🥧 Quality Breakdown", "📋 Detailed Report"])
                
                with tab1:
                    st.plotly_chart(create_habitat_map(results, species_info), use_container_width=True)
                
                with tab2:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(create_hsi_distribution(results), use_container_width=True)
                    with col2:
                        st.plotly_chart(create_quality_pie_chart(results), use_container_width=True)
                
                with tab3:
                    # Quality breakdown table
                    hsi_flat = np.array(results['hsi']).flatten()
                    total_points = len(hsi_flat)
                    
                    quality_data = {
                        'Quality Level': ['Excellent (>0.8)', 'Good (0.6-0.8)', 'Moderate (0.4-0.6)', 'Poor (0.2-0.4)', 'Unsuitable (≤0.2)'],
                        'Count': [
                            np.sum(hsi_flat > 0.8),
                            np.sum((hsi_flat > 0.6) & (hsi_flat <= 0.8)),
                            np.sum((hsi_flat > 0.4) & (hsi_flat <= 0.6)),
                            np.sum((hsi_flat > 0.2) & (hsi_flat <= 0.4)),
                            np.sum(hsi_flat <= 0.2)
                        ]
                    }
                    quality_data['Percentage'] = [f"{(count/total_points)*100:.1f}%" for count in quality_data['Count']]
                    
                    quality_df = pd.DataFrame(quality_data)
                    st.dataframe(quality_df, use_container_width=True)
                
                with tab4:
                    # Generate detailed report
                    analyzer = HabitatAnalyzer()
                    report_gen = ReportGenerator()
                    
                    stats = analyzer.calculate_habitat_statistics(results['hsi'])
                    report = report_gen.generate_habitat_report(results, selected_species)
                    
                    st.text_area("Detailed Analysis Report", report, height=400)
                    
                    # Download button for report
                    st.download_button(
                        label="📥 Download Report",
                        data=report,
                        file_name=f"shark_habitat_report_{selected_species}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("💡 Tip: Make sure all dependencies are installed and try a smaller study area.")
    
    else:
        # Welcome screen
        st.markdown("""
        ## 🌊 Welcome to the Shark Habitat Prediction System
        
        This advanced system uses **NASA satellite data** and **marine ecology models** to predict shark habitat suitability.
        
        ### 🚀 Features:
        - **Real-time NASA satellite data** (MODIS, VIIRS)
        - **Species-specific models** for Great White, Tiger, and Bull sharks
        - **Interactive habitat maps** with zoom and pan
        - **Statistical analysis** and quality metrics
        - **Professional reports** for research and conservation
        
        ### 📋 How to Use:
        1. Select your shark species from the sidebar
        2. Define your study area coordinates
        3. Choose the time period for analysis
        4. Click "🚀 Run Analysis" to generate predictions
        
        ### 🔬 Scientific Basis:
        Our models incorporate:
        - Sea Surface Temperature (SST) preferences
        - Chlorophyll-a concentration (productivity)
        - Thermal frontal zones
        - Species-specific ecological parameters
        
        **Ready to explore shark habitats? Configure your analysis in the sidebar!**
        """)

if __name__ == "__main__":
    main()
