"""
Shark Habitat Prediction Framework - Implementation
Mathematical framework for identifying sharks and predicting foraging habitats using NASA satellite data
"""

import numpy as np
import pandas as pd
from scipy import ndimage, interpolate
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, precision_recall_curve
import tensorflow as tf
from tensorflow.keras import layers, models
import xarray as xr
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class SharkHabitatPredictor:
    """
    Main class for shark habitat prediction using satellite data
    """
    
    def __init__(self, species='great_white'):
        self.species = species
        self.species_params = self._get_species_params(species)
        self.models = {}
        
    def _get_species_params(self, species):
        """Species-specific ecological parameters"""
        params = {
            'great_white': {
                'temp_opt': 18.0,
                'temp_std': 3.0,
                'temp_range': [12, 24],
                'depth_pref': [0, 200],
                'chl_k': 0.5,
                'chl_alpha': 2.0,
                'frontal_lambda': 0.1,
                'coastal_weight': 0.3
            },
            'tiger': {
                'temp_opt': 25.0,
                'temp_std': 2.5,
                'temp_range': [20, 30],
                'depth_pref': [0, 300],
                'chl_k': 0.8,
                'chl_alpha': 1.5,
                'frontal_lambda': 0.05,
                'coastal_weight': 0.8
            },
            'bull': {
                'temp_opt': 26.0,
                'temp_std': 4.0,
                'temp_range': [18, 32],
                'depth_pref': [0, 150],
                'chl_k': 1.0,
                'chl_alpha': 1.2,
                'frontal_lambda': 0.02,
                'coastal_weight': 0.9
            }
        }
        return params.get(species, params['great_white'])

class SatelliteDataProcessor:
    """
    Process NASA satellite data for shark habitat analysis
    """
    
    @staticmethod
    def calculate_sst_gradient(sst_data):
        """
        Calculate sea surface temperature gradient (frontal strength)
        
        Args:
            sst_data: 2D array of SST values
            
        Returns:
            grad_magnitude: Gradient magnitude array
        """
        # Calculate gradients using Sobel filters
        grad_x = ndimage.sobel(sst_data, axis=1)
        grad_y = ndimage.sobel(sst_data, axis=0)
        
        # Magnitude of gradient
        grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        return grad_magnitude
    
    @staticmethod
    def calculate_chlorophyll_anomaly(chl_data, climatology, std_dev):
        """
        Calculate chlorophyll anomaly from climatology
        
        Args:
            chl_data: Current chlorophyll data
            climatology: Long-term mean
            std_dev: Standard deviation
            
        Returns:
            anomaly: Standardized anomaly
        """
        anomaly = (chl_data - climatology) / std_dev
        return anomaly
    
    @staticmethod
    def calculate_productivity_index(chl, par, sst, temp_opt=20):
        """
        Calculate primary productivity index
        
        Args:
            chl: Chlorophyll concentration
            par: Photosynthetically available radiation
            sst: Sea surface temperature
            temp_opt: Optimal temperature for productivity
            
        Returns:
            productivity: Productivity index
        """
        # Temperature factor (Gaussian)
        temp_factor = np.exp(-((sst - temp_opt)**2) / (2 * 5**2))
        
        # Productivity index
        productivity = chl * par * temp_factor
        
        return productivity
    
    @staticmethod
    def detect_ocean_fronts(sst_data, threshold=0.5):
        """
        Detect ocean fronts using SST gradients
        
        Args:
            sst_data: SST array
            threshold: Gradient threshold for front detection
            
        Returns:
            fronts: Binary array of front locations
        """
        gradient = SatelliteDataProcessor.calculate_sst_gradient(sst_data)
        fronts = gradient > threshold
        
        return fronts.astype(int)

class HabitatSuitabilityModel:
    """
    Mathematical models for habitat suitability calculation
    """
    
    @staticmethod
    def temperature_suitability(temp, temp_opt, temp_std):
        """
        Gaussian temperature suitability function
        
        S_temp(T) = exp(-((T - T_opt)²)/(2σ_T²))
        """
        return np.exp(-((temp - temp_opt)**2) / (2 * temp_std**2))
    
    @staticmethod
    def chlorophyll_suitability(chl, k, alpha):
        """
        Michaelis-Menten type chlorophyll suitability
        
        S_chl(C) = C^α / (C^α + K^α)
        """
        return (chl**alpha) / (chl**alpha + k**alpha)
    
    @staticmethod
    def depth_suitability(depth, depth_min, depth_max, sigma=50):
        """
        Depth preference function with Gaussian tails
        """
        suitability = np.ones_like(depth)
        
        # Too shallow
        shallow_mask = depth < depth_min
        suitability[shallow_mask] = np.exp(-((depth[shallow_mask] - depth_min)**2) / (2 * sigma**2))
        
        # Too deep
        deep_mask = depth > depth_max
        suitability[deep_mask] = np.exp(-((depth[deep_mask] - depth_max)**2) / (2 * sigma**2))
        
        return suitability
    
    @staticmethod
    def frontal_suitability(gradient, lambda_param):
        """
        Frontal zone suitability
        
        S_front(∇SST) = 1 - exp(-|∇SST|/λ)
        """
        return 1 - np.exp(-gradient / lambda_param)
    
    @staticmethod
    def distance_to_coast_suitability(distance, coastal_weight):
        """
        Distance to coast suitability (exponential decay)
        """
        return np.exp(-distance * coastal_weight)

class HabitatSuitabilityIndex:
    """
    Calculate overall Habitat Suitability Index (HSI)
    """
    
    def __init__(self, species_params):
        self.params = species_params
        
    def calculate_hsi(self, environmental_data):
        """
        Calculate Habitat Suitability Index
        
        HSI(x,y,t) = Π wᵢ × Sᵢ(x,y,t)
        
        Args:
            environmental_data: Dictionary with environmental variables
            
        Returns:
            hsi: Habitat suitability index array
        """
        # Extract environmental variables
        sst = environmental_data['sst']
        chl = environmental_data['chlorophyll']
        depth = environmental_data['bathymetry']
        sst_gradient = environmental_data['sst_gradient']
        distance_coast = environmental_data.get('distance_to_coast', np.zeros_like(sst))
        
        # Calculate individual suitability components
        s_temp = HabitatSuitabilityModel.temperature_suitability(
            sst, self.params['temp_opt'], self.params['temp_std']
        )
        
        s_chl = HabitatSuitabilityModel.chlorophyll_suitability(
            chl, self.params['chl_k'], self.params['chl_alpha']
        )
        
        s_depth = HabitatSuitabilityModel.depth_suitability(
            depth, self.params['depth_pref'][0], self.params['depth_pref'][1]
        )
        
        s_front = HabitatSuitabilityModel.frontal_suitability(
            sst_gradient, self.params['frontal_lambda']
        )
        
        s_coast = HabitatSuitabilityModel.distance_to_coast_suitability(
            distance_coast, self.params['coastal_weight']
        )
        
        # Combine suitabilities (geometric mean approach)
        hsi = (s_temp * s_chl * s_depth * s_front * s_coast) ** (1/5)
        
        return hsi, {
            'temperature': s_temp,
            'chlorophyll': s_chl,
            'depth': s_depth,
            'frontal': s_front,
            'coastal': s_coast
        }

class MachineLearningPredictor:
    """
    Machine learning models for shark presence prediction
    """
    
    def __init__(self):
        self.models = {}
        
    def prepare_features(self, environmental_data):
        """
        Prepare feature matrix for ML models
        """
        features = []
        feature_names = []
        
        for var_name, data in environmental_data.items():
            if isinstance(data, np.ndarray) and data.ndim == 2:
                features.append(data.flatten())
                feature_names.append(var_name)
        
        # Stack features
        X = np.column_stack(features)
        
        # Add derived features
        if 'sst' in environmental_data and 'chlorophyll' in environmental_data:
            # Temperature-chlorophyll interaction
            temp_chl_interaction = (environmental_data['sst'] * 
                                  environmental_data['chlorophyll']).flatten()
            X = np.column_stack([X, temp_chl_interaction])
            feature_names.append('sst_chl_interaction')
        
        return X, feature_names
    
    def train_ensemble_model(self, X_train, y_train):
        """
        Train ensemble of models for shark presence prediction
        """
        # Logistic Regression
        self.models['logistic'] = LogisticRegression(random_state=42)
        self.models['logistic'].fit(X_train, y_train)
        
        # Random Forest
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=100, random_state=42
        )
        self.models['random_forest'].fit(X_train, y_train)
        
        # Neural Network
        self.models['neural_net'] = self._build_neural_network(X_train.shape[1])
        self.models['neural_net'].fit(
            X_train, y_train, 
            epochs=50, 
            batch_size=32, 
            validation_split=0.2,
            verbose=0
        )
    
    def _build_neural_network(self, input_dim):
        """
        Build neural network for habitat prediction
        """
        model = models.Sequential([
            layers.Dense(64, activation='relu', input_dim=input_dim),
            layers.Dropout(0.3),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def predict_ensemble(self, X_test):
        """
        Make ensemble predictions
        """
        predictions = {}
        
        # Individual model predictions
        predictions['logistic'] = self.models['logistic'].predict_proba(X_test)[:, 1]
        predictions['random_forest'] = self.models['random_forest'].predict_proba(X_test)[:, 1]
        predictions['neural_net'] = self.models['neural_net'].predict(X_test).flatten()
        
        # Ensemble prediction (weighted average)
        weights = {'logistic': 0.3, 'random_forest': 0.4, 'neural_net': 0.3}
        
        ensemble_pred = sum(weights[model] * pred 
                          for model, pred in predictions.items())
        
        return ensemble_pred, predictions

class TemporalDynamicsModel:
    """
    Model temporal dynamics of habitat suitability
    """
    
    @staticmethod
    def temporal_persistence(hsi_current, hsi_previous, alpha=0.7):
        """
        Model temporal persistence of habitat quality
        
        HSI(t+1) = α × HSI(t) + (1-α) × HSI_current(t+1)
        """
        if hsi_previous is None:
            return hsi_current
        
        return alpha * hsi_previous + (1 - alpha) * hsi_current
    
    @staticmethod
    def spatial_connectivity(hsi, kernel_size=5, beta=0.1):
        """
        Model spatial connectivity between habitat patches
        
        HSI_connected = HSI + β × Σ K(x-xᵢ, y-yᵢ) × HSI(xᵢ,yᵢ)
        """
        # Gaussian kernel for spatial connectivity
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size**2)
        
        # Convolve HSI with kernel
        connected_influence = ndimage.convolve(hsi, kernel, mode='constant')
        
        # Add connectivity influence
        hsi_connected = hsi + beta * connected_influence
        
        return np.clip(hsi_connected, 0, 1)

class UncertaintyQuantification:
    """
    Quantify prediction uncertainty
    """
    
    @staticmethod
    def bootstrap_uncertainty(model, X, n_bootstrap=100):
        """
        Calculate prediction uncertainty using bootstrap
        """
        n_samples = X.shape[0]
        predictions = []
        
        for _ in range(n_bootstrap):
            # Bootstrap sample
            indices = np.random.choice(n_samples, n_samples, replace=True)
            X_boot = X[indices]
            
            # Predict
            pred = model.predict_proba(X_boot)[:, 1]
            predictions.append(pred)
        
        predictions = np.array(predictions)
        
        # Calculate statistics
        mean_pred = np.mean(predictions, axis=0)
        std_pred = np.std(predictions, axis=0)
        
        # Confidence intervals
        ci_lower = np.percentile(predictions, 2.5, axis=0)
        ci_upper = np.percentile(predictions, 97.5, axis=0)
        
        return {
            'mean': mean_pred,
            'std': std_pred,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper
        }
    
    @staticmethod
    def model_uncertainty(ensemble_predictions):
        """
        Calculate uncertainty from model ensemble
        """
        pred_array = np.array(list(ensemble_predictions.values()))
        
        return {
            'mean': np.mean(pred_array, axis=0),
            'std': np.std(pred_array, axis=0),
            'min': np.min(pred_array, axis=0),
            'max': np.max(pred_array, axis=0)
        }

class ValidationMetrics:
    """
    Model validation and performance metrics
    """
    
    @staticmethod
    def calculate_auc_roc(y_true, y_pred):
        """Calculate AUC-ROC score"""
        return roc_auc_score(y_true, y_pred)
    
    @staticmethod
    def calculate_precision_recall(y_true, y_pred):
        """Calculate precision-recall curve"""
        precision, recall, thresholds = precision_recall_curve(y_true, y_pred)
        return precision, recall, thresholds
    
    @staticmethod
    def spatial_autocorrelation(residuals, coordinates):
        """
        Calculate Moran's I for spatial autocorrelation of residuals
        """
        # Simplified Moran's I calculation
        n = len(residuals)
        
        # Calculate spatial weights (inverse distance)
        distances = np.sqrt(np.sum((coordinates[:, None] - coordinates[None, :])**2, axis=2))
        weights = 1 / (distances + 1e-10)  # Add small value to avoid division by zero
        np.fill_diagonal(weights, 0)
        
        # Normalize weights
        row_sums = np.sum(weights, axis=1)
        weights = weights / row_sums[:, None]
        
        # Calculate Moran's I
        mean_residual = np.mean(residuals)
        numerator = np.sum(weights * np.outer(residuals - mean_residual, residuals - mean_residual))
        denominator = np.sum((residuals - mean_residual)**2)
        
        morans_i = (n / np.sum(weights)) * (numerator / denominator)
        
        return morans_i

# Example usage and demonstration
def example_usage():
    """
    Demonstrate the shark habitat prediction framework
    """
    # Initialize predictor for Great White Shark
    predictor = SharkHabitatPredictor(species='great_white')
    
    # Create synthetic environmental data (replace with real NASA data)
    np.random.seed(42)
    grid_size = (100, 100)
    
    environmental_data = {
        'sst': 15 + 10 * np.random.random(grid_size),  # 15-25°C
        'chlorophyll': np.random.exponential(0.5, grid_size),  # mg/m³
        'bathymetry': np.random.exponential(100, grid_size),  # meters
        'par': 30 + 20 * np.random.random(grid_size),  # Einstein/m²/day
    }
    
    # Calculate SST gradient
    environmental_data['sst_gradient'] = SatelliteDataProcessor.calculate_sst_gradient(
        environmental_data['sst']
    )
    
    # Calculate productivity index
    environmental_data['productivity'] = SatelliteDataProcessor.calculate_productivity_index(
        environmental_data['chlorophyll'],
        environmental_data['par'],
        environmental_data['sst']
    )
    
    # Calculate Habitat Suitability Index
    hsi_calculator = HabitatSuitabilityIndex(predictor.species_params)
    hsi, components = hsi_calculator.calculate_hsi(environmental_data)
    
    print(f"Habitat Suitability Index calculated")
    print(f"Mean HSI: {np.mean(hsi):.3f}")
    print(f"Max HSI: {np.max(hsi):.3f}")
    print(f"Suitable habitat area (HSI > 0.5): {np.sum(hsi > 0.5) / hsi.size * 100:.1f}%")
    
    # Prepare data for machine learning
    ml_predictor = MachineLearningPredictor()
    X, feature_names = ml_predictor.prepare_features(environmental_data)
    
    # Create synthetic ground truth (replace with real tracking data)
    y = (hsi.flatten() > 0.6).astype(int)  # Binary presence/absence
    
    # Add some noise to make it more realistic
    noise_indices = np.random.choice(len(y), int(0.1 * len(y)), replace=False)
    y[noise_indices] = 1 - y[noise_indices]
    
    # Train models
    ml_predictor.train_ensemble_model(X, y)
    
    # Make predictions
    ensemble_pred, individual_preds = ml_predictor.predict_ensemble(X)
    
    # Calculate validation metrics
    auc_score = ValidationMetrics.calculate_auc_roc(y, ensemble_pred)
    print(f"Ensemble AUC-ROC: {auc_score:.3f}")
    
    # Calculate uncertainty
    uncertainty = UncertaintyQuantification.model_uncertainty(individual_preds)
    print(f"Mean prediction uncertainty (std): {np.mean(uncertainty['std']):.3f}")
    
    return {
        'hsi': hsi,
        'components': components,
        'predictions': ensemble_pred.reshape(grid_size),
        'uncertainty': uncertainty['std'].reshape(grid_size),
        'environmental_data': environmental_data
    }

if __name__ == "__main__":
    # Run example
    results = example_usage()
    
    # Create visualization
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Plot environmental variables
    im1 = axes[0, 0].imshow(results['environmental_data']['sst'], cmap='coolwarm')
    axes[0, 0].set_title('Sea Surface Temperature (°C)')
    plt.colorbar(im1, ax=axes[0, 0])
    
    im2 = axes[0, 1].imshow(results['environmental_data']['chlorophyll'], cmap='viridis')
    axes[0, 1].set_title('Chlorophyll-a (mg/m³)')
    plt.colorbar(im2, ax=axes[0, 1])
    
    im3 = axes[0, 2].imshow(results['environmental_data']['sst_gradient'], cmap='plasma')
    axes[0, 2].set_title('SST Gradient (Fronts)')
    plt.colorbar(im3, ax=axes[0, 2])
    
    # Plot results
    im4 = axes[1, 0].imshow(results['hsi'], cmap='RdYlBu_r', vmin=0, vmax=1)
    axes[1, 0].set_title('Habitat Suitability Index')
    plt.colorbar(im4, ax=axes[1, 0])
    
    im5 = axes[1, 1].imshow(results['predictions'], cmap='RdYlBu_r', vmin=0, vmax=1)
    axes[1, 1].set_title('ML Prediction (Shark Presence)')
    plt.colorbar(im5, ax=axes[1, 1])
    
    im6 = axes[1, 2].imshow(results['uncertainty'], cmap='Reds')
    axes[1, 2].set_title('Prediction Uncertainty')
    plt.colorbar(im6, ax=axes[1, 2])
    
    plt.tight_layout()
    plt.savefig('shark_habitat_prediction_results.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Framework demonstration complete!")
    print("Results saved to 'shark_habitat_prediction_results.png'")
