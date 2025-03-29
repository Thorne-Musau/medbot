import shap
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

class SHAPExplainer:
    def __init__(self):
        # Load model and data with absolute paths
        self.model = joblib.load(Path('models/saved_models/disease_predictor.joblib').resolve())
        self.symptom_names = joblib.load(Path('data/processed/symptom_names.joblib').resolve())
        self.label_encoder = joblib.load(Path('data/processed/label_encoder.joblib').resolve())
        
        # Prepare background data
        X_train = pd.read_csv(Path('data/processed/X_train.csv').resolve()).values
        self.background = shap.utils.sample(X_train, 10)  # Updated sampling method

    def explain_prediction(self, symptom_vector):
        """Generate SHAP explanations for a prediction"""
        # Create explainer
        explainer = shap.KernelExplainer(
            self.model.predict_proba,
            self.background,
            link='logit'
        )
        
        # Calculate SHAP values
        X = np.array(symptom_vector).reshape(1, -1)
        shap_values = explainer.shap_values(X)
        
        # Create proper Explanation object for each class
        shap_exps = []
        for i, values in enumerate(shap_values):
            exp = shap.Explanation(
                values=values,
                base_values=explainer.expected_value[i],
                data=X,
                feature_names=self.symptom_names
            )
            shap_exps.append(exp)
        
        # Visualize
        self._plot_shap(shap_exps)
        
        return shap_values

    def _plot_shap(self, shap_exps):
        """Generate SHAP plots without GUI"""
        try:
            # Summary plot for each class
            for i, exp in enumerate(shap_exps):
                plt.figure(figsize=(10, 6))
                shap.summary_plot(
                    exp.values,
                    features=exp.data,
                    feature_names=self.symptom_names,
                    plot_type='bar',
                    show=False
                )
                plt.title(f"SHAP Summary Plot for {self.label_encoder.classes_[i]}")
                plt.tight_layout()
                plt.savefig(Path('docs/shap_summary.png').resolve(), dpi=300)
                plt.close()
            
            # Waterfall plot for top prediction
            pred_class = np.argmax([exp.base_values for exp in shap_exps])
            plt.figure(figsize=(12, 6))
            shap.plots.waterfall(shap_exps[pred_class], show=False)
            plt.savefig(Path('docs/shap_force.png').resolve(), dpi=300)
            plt.close()
            
        except Exception as e:
            print(f"Visualization failed: {str(e)}")