import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm, lognorm, gamma, beta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class PricingMonteCarloSimulation:
    """
    Kelas untuk melakukan simulasi Monte Carlo pada data pricing konstruksi.
    
    Fitur:
    - Analisis distribusi otomatis
    - Simulasi berbagai skenario
    - Analisis risiko dan sensitivitas
    - Visualisasi hasil
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Inisialisasi dengan dataset.
        
        Args:
            data: DataFrame dengan kolom Material_Cost, Labor_Cost, Profit_Rate, 
                  Discount_or_Markup, Total_Estimate
        """
        self.data = data.copy()
        self.distributions = {}
        self.simulation_results = {}
        self.fitted_params = {}
        
        # Kolom numerik untuk simulasi
        self.numeric_columns = ['Material_Cost', 'Labor_Cost', 'Profit_Rate', 
                               'Discount_or_Markup', 'Total_Estimate']
        
        print("🎯 PricingMonteCarloSimulation initialized")
        print(f"📊 Dataset shape: {self.data.shape}")
    
    def fit_distributions(self, test_distributions: List[str] = None) -> Dict:
        """
        Fit berbagai distribusi statistik ke setiap kolom numerik.
        
        Args:
            test_distributions: List nama distribusi untuk ditest
            
        Returns:
            Dictionary dengan best fit distribution untuk setiap kolom
        """
        if test_distributions is None:
            test_distributions = ['norm', 'lognorm', 'gamma', 'beta', 'uniform']
        
        print("\n🔍 Fitting distributions...")
        
        for col in self.numeric_columns:
            if col not in self.data.columns:
                continue
                
            data_col = self.data[col].dropna()
            
            # Normalize data untuk beta distribution (0-1 range)
            if 'beta' in test_distributions:
                data_normalized = (data_col - data_col.min()) / (data_col.max() - data_col.min())
            
            best_dist = None
            best_params = None
            best_ks_stat = float('inf')
            
            for dist_name in test_distributions:
                try:
                    if dist_name == 'norm':
                        params = stats.norm.fit(data_col)
                        ks_stat, _ = stats.kstest(data_col, lambda x: stats.norm.cdf(x, *params))
                    elif dist_name == 'lognorm':
                        # Pastikan data positif untuk lognorm
                        if (data_col > 0).all():
                            params = stats.lognorm.fit(data_col)
                            ks_stat, _ = stats.kstest(data_col, lambda x: stats.lognorm.cdf(x, *params))
                        else:
                            continue
                    elif dist_name == 'gamma':
                        if (data_col > 0).all():
                            params = stats.gamma.fit(data_col)
                            ks_stat, _ = stats.kstest(data_col, lambda x: stats.gamma.cdf(x, *params))
                        else:
                            continue
                    elif dist_name == 'beta':
                        params = stats.beta.fit(data_normalized)
                        ks_stat, _ = stats.kstest(data_normalized, lambda x: stats.beta.cdf(x, *params))
                    elif dist_name == 'uniform':
                        params = (data_col.min(), data_col.max())
                        ks_stat, _ = stats.kstest(data_col, lambda x: stats.uniform.cdf(x, params[0], params[1]-params[0]))
                    
                    if ks_stat < best_ks_stat:
                        best_ks_stat = ks_stat
                        best_dist = dist_name
                        best_params = params
                        
                except Exception as e:
                    continue
            
            self.distributions[col] = {
                'distribution': best_dist,
                'params': best_params,
                'ks_statistic': best_ks_stat,
                'data_range': (data_col.min(), data_col.max()),
                'mean': data_col.mean(),
                'std': data_col.std()
            }
            
            print(f"├── {col}: {best_dist} (KS: {best_ks_stat:.4f})")
        
        print("✅ Distribution fitting completed!")
        return self.distributions
    
    def generate_samples(self, n_simulations: int = 10000, 
                        scenario_adjustments: Dict = None) -> pd.DataFrame:
        """
        Generate samples dari fitted distributions.
        
        Args:
            n_simulations: Jumlah simulasi
            scenario_adjustments: Dict untuk adjust parameter (e.g., {'Material_Cost': 1.1})
            
        Returns:
            DataFrame dengan generated samples
        """
        if not self.distributions:
            raise ValueError("Distributions belum di-fit. Jalankan fit_distributions() dulu.")
        
        print(f"\n🎲 Generating {n_simulations:,} samples...")
        
        samples = {}
        
        for col, dist_info in self.distributions.items():
            dist_name = dist_info['distribution']
            params = dist_info['params']
            
            # Apply scenario adjustments
            if scenario_adjustments and col in scenario_adjustments:
                adjustment = scenario_adjustments[col]
                print(f"├── Applying {adjustment}x adjustment to {col}")
            else:
                adjustment = 1.0
            
            try:
                if dist_name == 'norm':
                    samples[col] = np.random.normal(params[0] * adjustment, params[1], n_simulations)
                elif dist_name == 'lognorm':
                    samples[col] = stats.lognorm.rvs(*params, size=n_simulations) * adjustment
                elif dist_name == 'gamma':
                    samples[col] = stats.gamma.rvs(*params, size=n_simulations) * adjustment
                elif dist_name == 'beta':
                    # Beta distribution perlu denormalisasi
                    beta_samples = stats.beta.rvs(*params, size=n_simulations)
                    data_range = dist_info['data_range']
                    samples[col] = (beta_samples * (data_range[1] - data_range[0]) + data_range[0]) * adjustment
                elif dist_name == 'uniform':
                    samples[col] = np.random.uniform(params[0] * adjustment, params[1] * adjustment, n_simulations)
                else:
                    # Fallback ke normal distribution
                    samples[col] = np.random.normal(dist_info['mean'] * adjustment, dist_info['std'], n_simulations)
                    
            except Exception as e:
                print(f"⚠️  Error generating samples for {col}: {e}")
                # Fallback ke normal distribution
                samples[col] = np.random.normal(dist_info['mean'] * adjustment, dist_info['std'], n_simulations)
        
        samples_df = pd.DataFrame(samples)
        
        # Recalculate Total_Estimate berdasarkan komponen lain
        if all(col in samples_df.columns for col in ['Material_Cost', 'Labor_Cost', 'Profit_Rate', 'Discount_or_Markup']):
            base_cost = samples_df['Material_Cost'] + samples_df['Labor_Cost']
            profit_amount = base_cost * (samples_df['Profit_Rate'] / 100)
            samples_df['Total_Estimate_Calculated'] = base_cost + profit_amount + samples_df['Discount_or_Markup']
        
        print("✅ Sample generation completed!")
        return samples_df
    
    def run_simulation(self, n_simulations: int = 10000, 
                      scenarios: Dict[str, Dict] = None) -> Dict:
        """
        Jalankan simulasi Monte Carlo dengan berbagai skenario.
        
        Args:
            n_simulations: Jumlah simulasi per skenario
            scenarios: Dict skenario {nama: {adjustments}}
            
        Returns:
            Dictionary hasil simulasi
        """
        if scenarios is None:
            scenarios = {
                'baseline': {},
                'material_increase_10pct': {'Material_Cost': 1.1},
                'labor_increase_15pct': {'Labor_Cost': 1.15},
                'combined_increase': {'Material_Cost': 1.1, 'Labor_Cost': 1.15}
            }
        
        print(f"\n🚀 Running Monte Carlo simulation...")
        print(f"📊 Scenarios: {list(scenarios.keys())}")
        
        results = {}
        
        for scenario_name, adjustments in scenarios.items():
            print(f"\n🎯 Running scenario: {scenario_name}")
            
            samples = self.generate_samples(n_simulations, adjustments)
            
            # Analisis statistik
            scenario_results = {
                'samples': samples,
                'statistics': {},
                'risk_metrics': {}
            }
            
            for col in samples.columns:
                stats_dict = {
                    'mean': samples[col].mean(),
                    'median': samples[col].median(),
                    'std': samples[col].std(),
                    'min': samples[col].min(),
                    'max': samples[col].max(),
                    'q25': samples[col].quantile(0.25),
                    'q75': samples[col].quantile(0.75),
                    'q95': samples[col].quantile(0.95),
                    'q99': samples[col].quantile(0.99)
                }
                scenario_results['statistics'][col] = stats_dict
                
                # Risk metrics
                if 'Total_Estimate' in col:
                    baseline_mean = self.data['Total_Estimate'].mean() if 'Total_Estimate' in self.data.columns else samples[col].mean()
                    
                    risk_metrics = {
                        'var_95': samples[col].quantile(0.05),  # Value at Risk 95%
                        'var_99': samples[col].quantile(0.01),  # Value at Risk 99%
                        'cvar_95': samples[col][samples[col] <= samples[col].quantile(0.05)].mean(),  # Conditional VaR
                        'prob_loss': (samples[col] < baseline_mean).mean(),  # Probability of loss
                        'expected_shortfall': samples[col][samples[col] <= samples[col].quantile(0.05)].mean()
                    }
                    scenario_results['risk_metrics'][col] = risk_metrics
            
            results[scenario_name] = scenario_results
            print(f"✅ Scenario {scenario_name} completed")
        
        self.simulation_results = results
        print("\n🎉 Monte Carlo simulation completed!")
        return results
    
    def get_summary_statistics(self, scenario: str = 'baseline') -> pd.DataFrame:
        """
        Dapatkan ringkasan statistik untuk skenario tertentu.
        
        Args:
            scenario: Nama skenario
            
        Returns:
            DataFrame dengan ringkasan statistik
        """
        if scenario not in self.simulation_results:
            raise ValueError(f"Scenario '{scenario}' tidak ditemukan")
        
        stats_data = []
        scenario_data = self.simulation_results[scenario]['statistics']
        
        for col, stats in scenario_data.items():
            stats_data.append({
                'Variable': col,
                'Mean': f"{stats['mean']:,.2f}",
                'Median': f"{stats['median']:,.2f}",
                'Std Dev': f"{stats['std']:,.2f}",
                'Min': f"{stats['min']:,.2f}",
                'Max': f"{stats['max']:,.2f}",
                'Q95': f"{stats['q95']:,.2f}",
                'Q99': f"{stats['q99']:,.2f}"
            })
        
        return pd.DataFrame(stats_data)
    
    def print_risk_analysis(self, scenario: str = 'baseline'):
        """
        Print analisis risiko untuk skenario tertentu.
        
        Args:
            scenario: Nama skenario
        """
        if scenario not in self.simulation_results:
            print(f"❌ Scenario '{scenario}' tidak ditemukan")
            return
        
        print(f"\n📊 RISK ANALYSIS - {scenario.upper()}")
        print("=" * 50)
        
        risk_data = self.simulation_results[scenario]['risk_metrics']
        
        for col, metrics in risk_data.items():
            print(f"\n🎯 {col}:")
            print(f"├── VaR 95%: {metrics['var_95']:,.2f}")
            print(f"├── VaR 99%: {metrics['var_99']:,.2f}")
            print(f"├── CVaR 95%: {metrics['cvar_95']:,.2f}")
            print(f"├── Probability of Loss: {metrics['prob_loss']:.2%}")
            print(f"└── Expected Shortfall: {metrics['expected_shortfall']:,.2f}")

# Contoh penggunaan
if __name__ == "__main__":
    # Load data
    from data_loader import DataLoader
    
    loader = DataLoader("D:\\abdurachman.putra\\Downloads\\archive (2)\\construction_estimates.csv")
    loader.load_data()
    loader.clean_data()
    clean_data = loader.data
    
    # Inisialisasi simulasi
    mc_sim = PricingMonteCarloSimulation(clean_data)
    
    # Fit distributions
    distributions = mc_sim.fit_distributions()
    
    # Run simulation
    results = mc_sim.run_simulation(n_simulations=5000)
    
    # Print hasil
    print("\n" + "="*60)
    print("📈 SUMMARY STATISTICS")
    print("="*60)
    summary = mc_sim.get_summary_statistics('baseline')
    print(summary.to_string(index=False))
    
    # Risk analysis
    mc_sim.print_risk_analysis('baseline')
    mc_sim.print_risk_analysis('material_increase_10pct')
    
    print("\n✅ Monte Carlo Simulation completed successfully!")