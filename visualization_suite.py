import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style untuk visualisasi yang lebih menarik
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class MonteCarloVisualizer:
    """
    Kelas untuk visualisasi hasil simulasi Monte Carlo.
    
    Fitur:
    - Distribution plots
    - Risk analysis charts
    - Scenario comparison
    - Sensitivity analysis
    - Interactive dashboards
    """
    
    def __init__(self, simulation_results: dict, figsize: tuple = (15, 10)):
        """
        Inisialisasi visualizer.
        
        Args:
            simulation_results: Hasil dari PricingMonteCarloSimulation
            figsize: Ukuran default untuk figure
        """
        self.results = simulation_results
        self.figsize = figsize
        self.colors = sns.color_palette("husl", len(simulation_results))
        
        print(f"🎨 MonteCarloVisualizer initialized")
        print(f"📊 Available scenarios: {list(simulation_results.keys())}")
    
    def plot_distribution_analysis(self, scenario: str = 'baseline', 
                                 variables: list = None, save_path: str = None):
        """
        Plot analisis distribusi untuk variabel-variabel tertentu.
        
        Args:
            scenario: Nama skenario
            variables: List variabel untuk diplot
            save_path: Path untuk menyimpan plot
        """
        if scenario not in self.results:
            print(f"❌ Scenario '{scenario}' tidak ditemukan")
            return
        
        samples = self.results[scenario]['samples']
        
        if variables is None:
            variables = ['Material_Cost', 'Labor_Cost', 'Total_Estimate']
        
        # Filter variabel yang ada
        available_vars = [var for var in variables if var in samples.columns]
        
        if not available_vars:
            print("❌ Tidak ada variabel yang valid untuk diplot")
            return
        
        n_vars = len(available_vars)
        fig, axes = plt.subplots(2, n_vars, figsize=(5*n_vars, 10))
        
        if n_vars == 1:
            axes = axes.reshape(-1, 1)
        
        fig.suptitle(f'Distribution Analysis - {scenario.title()}', fontsize=16, fontweight='bold')
        
        for i, var in enumerate(available_vars):
            data = samples[var]
            
            # Histogram dengan KDE
            axes[0, i].hist(data, bins=50, alpha=0.7, density=True, color=self.colors[i])
            axes[0, i].axvline(data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {data.mean():,.0f}')
            axes[0, i].axvline(data.median(), color='orange', linestyle='--', linewidth=2, label=f'Median: {data.median():,.0f}')
            
            # KDE overlay
            kde_x = np.linspace(data.min(), data.max(), 100)
            kde = stats.gaussian_kde(data)
            axes[0, i].plot(kde_x, kde(kde_x), 'k-', linewidth=2, alpha=0.8)
            
            axes[0, i].set_title(f'{var} Distribution', fontweight='bold')
            axes[0, i].set_xlabel(var)
            axes[0, i].set_ylabel('Density')
            axes[0, i].legend()
            axes[0, i].grid(True, alpha=0.3)
            
            # Q-Q Plot
            stats.probplot(data, dist="norm", plot=axes[1, i])
            axes[1, i].set_title(f'{var} Q-Q Plot', fontweight='bold')
            axes[1, i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📁 Plot saved: {save_path}")
        
        plt.show()
    
    def plot_risk_metrics(self, scenarios: list = None, save_path: str = None):
        """
        Plot risk metrics untuk berbagai skenario.
        
        Args:
            scenarios: List skenario untuk dibandingkan
            save_path: Path untuk menyimpan plot
        """
        if scenarios is None:
            scenarios = list(self.results.keys())
        
        # Filter skenario yang ada
        available_scenarios = [s for s in scenarios if s in self.results]
        
        if not available_scenarios:
            print("❌ Tidak ada skenario yang valid")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=self.figsize)
        fig.suptitle('Risk Metrics Comparison', fontsize=16, fontweight='bold')
        
        # Prepare data
        risk_data = []
        for scenario in available_scenarios:
            if 'risk_metrics' in self.results[scenario]:
                for var, metrics in self.results[scenario]['risk_metrics'].items():
                    if 'Total_Estimate' in var:
                        risk_data.append({
                            'Scenario': scenario,
                            'Variable': var,
                            'VaR_95': metrics['var_95'],
                            'VaR_99': metrics['var_99'],
                            'CVaR_95': metrics['cvar_95'],
                            'Prob_Loss': metrics['prob_loss']
                        })
        
        if not risk_data:
            print("❌ Tidak ada data risk metrics")
            return
        
        risk_df = pd.DataFrame(risk_data)
        
        # VaR 95% comparison
        sns.barplot(data=risk_df, x='Scenario', y='VaR_95', hue='Variable', ax=axes[0, 0])
        axes[0, 0].set_title('Value at Risk (95%)', fontweight='bold')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # VaR 99% comparison
        sns.barplot(data=risk_df, x='Scenario', y='VaR_99', hue='Variable', ax=axes[0, 1])
        axes[0, 1].set_title('Value at Risk (99%)', fontweight='bold')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3)
        
        # CVaR comparison
        sns.barplot(data=risk_df, x='Scenario', y='CVaR_95', hue='Variable', ax=axes[1, 0])
        axes[1, 0].set_title('Conditional VaR (95%)', fontweight='bold')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        
        # Probability of Loss
        sns.barplot(data=risk_df, x='Scenario', y='Prob_Loss', hue='Variable', ax=axes[1, 1])
        axes[1, 1].set_title('Probability of Loss', fontweight='bold')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].set_ylabel('Probability')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📁 Plot saved: {save_path}")
        
        plt.show()
    
    def plot_scenario_comparison(self, variable: str = 'Total_Estimate', 
                               save_path: str = None):
        """
        Plot perbandingan distribusi antar skenario.
        
        Args:
            variable: Variabel yang akan dibandingkan
            save_path: Path untuk menyimpan plot
        """
        fig, axes = plt.subplots(2, 2, figsize=self.figsize)
        fig.suptitle(f'Scenario Comparison - {variable}', fontsize=16, fontweight='bold')
        
        # Collect data
        scenario_data = {}
        for scenario, results in self.results.items():
            if variable in results['samples'].columns:
                scenario_data[scenario] = results['samples'][variable]
        
        if not scenario_data:
            print(f"❌ Variabel '{variable}' tidak ditemukan dalam hasil simulasi")
            return
        
        # 1. Overlapping histograms
        for i, (scenario, data) in enumerate(scenario_data.items()):
            axes[0, 0].hist(data, bins=50, alpha=0.6, label=scenario, color=self.colors[i % len(self.colors)])
        axes[0, 0].set_title('Distribution Overlay', fontweight='bold')
        axes[0, 0].set_xlabel(variable)
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Box plots
        data_list = [data for data in scenario_data.values()]
        labels = list(scenario_data.keys())
        axes[0, 1].boxplot(data_list, labels=labels)
        axes[0, 1].set_title('Box Plot Comparison', fontweight='bold')
        axes[0, 1].set_ylabel(variable)
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Violin plots
        df_combined = pd.DataFrame()
        for scenario, data in scenario_data.items():
            temp_df = pd.DataFrame({variable: data, 'Scenario': scenario})
            df_combined = pd.concat([df_combined, temp_df], ignore_index=True)
        
        sns.violinplot(data=df_combined, x='Scenario', y=variable, ax=axes[1, 0])
        axes[1, 0].set_title('Violin Plot Comparison', fontweight='bold')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Cumulative distribution
        for i, (scenario, data) in enumerate(scenario_data.items()):
            sorted_data = np.sort(data)
            y_vals = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
            axes[1, 1].plot(sorted_data, y_vals, label=scenario, linewidth=2, color=self.colors[i % len(self.colors)])
        axes[1, 1].set_title('Cumulative Distribution', fontweight='bold')
        axes[1, 1].set_xlabel(variable)
        axes[1, 1].set_ylabel('Cumulative Probability')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📁 Plot saved: {save_path}")
        
        plt.show()
    
    def plot_correlation_heatmap(self, scenario: str = 'baseline', save_path: str = None):
        """
        Plot correlation heatmap untuk variabel dalam skenario tertentu.
        
        Args:
            scenario: Nama skenario
            save_path: Path untuk menyimpan plot
        """
        if scenario not in self.results:
            print(f"❌ Scenario '{scenario}' tidak ditemukan")
            return
        
        samples = self.results[scenario]['samples']
        numeric_cols = samples.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("❌ Tidak cukup variabel numerik untuk correlation analysis")
            return
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Calculate correlation matrix
        corr_matrix = samples[numeric_cols].corr()
        
        # Create heatmap
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdYlBu_r', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8}, ax=ax)
        
        ax.set_title(f'Correlation Matrix - {scenario.title()}', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📁 Plot saved: {save_path}")
        
        plt.show()
    
    def plot_sensitivity_analysis(self, base_scenario: str = 'baseline', 
                                comparison_scenarios: list = None, 
                                variable: str = 'Total_Estimate',
                                save_path: str = None):
        """
        Plot sensitivity analysis membandingkan dampak perubahan parameter.
        
        Args:
            base_scenario: Skenario baseline
            comparison_scenarios: List skenario untuk dibandingkan
            variable: Variabel target untuk analisis
            save_path: Path untuk menyimpan plot
        """
        if comparison_scenarios is None:
            comparison_scenarios = [s for s in self.results.keys() if s != base_scenario]
        
        if base_scenario not in self.results:
            print(f"❌ Base scenario '{base_scenario}' tidak ditemukan")
            return
        
        base_stats = self.results[base_scenario]['statistics']
        if variable not in base_stats:
            print(f"❌ Variabel '{variable}' tidak ditemukan dalam base scenario")
            return
        
        base_mean = base_stats[variable]['mean']
        
        # Collect sensitivity data
        sensitivity_data = []
        for scenario in comparison_scenarios:
            if scenario in self.results and variable in self.results[scenario]['statistics']:
                scenario_mean = self.results[scenario]['statistics'][variable]['mean']
                change_pct = ((scenario_mean - base_mean) / base_mean) * 100
                
                sensitivity_data.append({
                    'Scenario': scenario.replace('_', ' ').title(),
                    'Mean_Value': scenario_mean,
                    'Change_Percent': change_pct,
                    'Absolute_Change': scenario_mean - base_mean
                })
        
        if not sensitivity_data:
            print("❌ Tidak ada data untuk sensitivity analysis")
            return
        
        sens_df = pd.DataFrame(sensitivity_data)
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle(f'Sensitivity Analysis - {variable}', fontsize=16, fontweight='bold')
        
        # 1. Percentage change
        bars1 = axes[0].bar(sens_df['Scenario'], sens_df['Change_Percent'], 
                           color=[self.colors[i % len(self.colors)] for i in range(len(sens_df))])
        axes[0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
        axes[0].set_title('Percentage Change from Baseline', fontweight='bold')
        axes[0].set_ylabel('Change (%)')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars1, sens_df['Change_Percent']):
            height = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width()/2., height + (0.01 * max(abs(sens_df['Change_Percent']))),
                        f'{value:.1f}%', ha='center', va='bottom' if height >= 0 else 'top')
        
        # 2. Absolute values
        all_means = [base_mean] + sens_df['Mean_Value'].tolist()
        all_scenarios = ['Baseline'] + sens_df['Scenario'].tolist()
        
        bars2 = axes[1].bar(all_scenarios, all_means, 
                           color=['gray'] + [self.colors[i % len(self.colors)] for i in range(len(sens_df))])
        axes[1].set_title('Mean Values Comparison', fontweight='bold')
        axes[1].set_ylabel(f'Mean {variable}')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars2, all_means):
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., height + (0.01 * max(all_means)),
                        f'{value:,.0f}', ha='center', va='bottom')
        
        # 3. Tornado chart (absolute change)
        sens_df_sorted = sens_df.reindex(sens_df['Absolute_Change'].abs().sort_values().index)
        
        colors_tornado = ['red' if x < 0 else 'green' for x in sens_df_sorted['Absolute_Change']]
        bars3 = axes[2].barh(sens_df_sorted['Scenario'], sens_df_sorted['Absolute_Change'], color=colors_tornado)
        axes[2].axvline(x=0, color='black', linestyle='-', alpha=0.3)
        axes[2].set_title('Tornado Chart (Absolute Impact)', fontweight='bold')
        axes[2].set_xlabel(f'Change in {variable}')
        axes[2].grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars3, sens_df_sorted['Absolute_Change']):
            width = bar.get_width()
            axes[2].text(width + (0.01 * max(abs(sens_df_sorted['Absolute_Change']))) * (1 if width >= 0 else -1),
                        bar.get_y() + bar.get_height()/2.,
                        f'{value:,.0f}', ha='left' if width >= 0 else 'right', va='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📁 Plot saved: {save_path}")
        
        plt.show()
    
    def create_comprehensive_report(self, save_dir: str = "./monte_carlo_report"):
        """
        Buat laporan komprehensif dengan semua visualisasi.
        
        Args:
            save_dir: Directory untuk menyimpan semua plot
        """
        import os
        
        # Create directory if not exists
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"\n📊 Creating comprehensive Monte Carlo report...")
        print(f"📁 Saving to: {save_dir}")
        
        # 1. Distribution analysis
        print("├── Creating distribution analysis...")
        self.plot_distribution_analysis(save_path=f"{save_dir}/01_distribution_analysis.png")
        
        # 2. Risk metrics
        print("├── Creating risk metrics comparison...")
        self.plot_risk_metrics(save_path=f"{save_dir}/02_risk_metrics.png")
        
        # 3. Scenario comparison
        print("├── Creating scenario comparison...")
        self.plot_scenario_comparison(save_path=f"{save_dir}/03_scenario_comparison.png")
        
        # 4. Correlation analysis
        print("├── Creating correlation heatmap...")
        self.plot_correlation_heatmap(save_path=f"{save_dir}/04_correlation_heatmap.png")
        
        # 5. Sensitivity analysis
        print("├── Creating sensitivity analysis...")
        self.plot_sensitivity_analysis(save_path=f"{save_dir}/05_sensitivity_analysis.png")
        
        print(f"\n✅ Comprehensive report created successfully!")
        print(f"📁 All plots saved in: {save_dir}")

# Contoh penggunaan
if __name__ == "__main__":
    # Import dan jalankan simulasi
    from monte_carlo_simulation import PricingMonteCarloSimulation
    from data_loader import DataLoader
    
    print("🚀 Running Monte Carlo Visualization Demo...")
    
    # Load data
    loader = DataLoader("D:\\abdurachman.putra\\Downloads\\archive (2)\\construction_estimates.csv")
    loader.load_data()
    loader.clean_data()
    
    # Run simulation
    mc_sim = PricingMonteCarloSimulation(loader.data)
    mc_sim.fit_distributions()
    results = mc_sim.run_simulation(n_simulations=5000)
    
    # Create visualizer
    visualizer = MonteCarloVisualizer(results)
    
    # Generate individual plots
    print("\n📊 Generating visualizations...")
    
    print("├── Distribution Analysis")
    visualizer.plot_distribution_analysis()
    
    print("├── Risk Metrics")
    visualizer.plot_risk_metrics()
    
    print("├── Scenario Comparison")
    visualizer.plot_scenario_comparison()
    
    print("├── Correlation Heatmap")
    visualizer.plot_correlation_heatmap()
    
    print("├── Sensitivity Analysis")
    visualizer.plot_sensitivity_analysis()
    
    # Create comprehensive report
    print("\n📋 Creating comprehensive report...")
    visualizer.create_comprehensive_report()
    
    print("\n🎉 Visualization demo completed successfully!")