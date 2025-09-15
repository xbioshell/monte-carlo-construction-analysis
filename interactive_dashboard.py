import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
from plotly.colors import qualitative
import warnings
warnings.filterwarnings('ignore')

class InteractiveDashboard:
    """
    Kelas untuk membuat interactive dashboard Monte Carlo simulation.
    
    Fitur:
    - Interactive plots dengan Plotly
    - Real-time filtering dan selection
    - Drill-down capabilities
    - Export ke HTML
    """
    
    def __init__(self, simulation_results: dict):
        """
        Inisialisasi dashboard.
        
        Args:
            simulation_results: Hasil dari PricingMonteCarloSimulation
        """
        self.results = simulation_results
        self.colors = qualitative.Set3
        
        print(f"🎛️ InteractiveDashboard initialized")
        print(f"📊 Available scenarios: {list(simulation_results.keys())}")
    
    def create_distribution_dashboard(self, save_path: str = None):
        """
        Buat interactive dashboard untuk analisis distribusi.
        
        Args:
            save_path: Path untuk menyimpan HTML file
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distribution Comparison', 'Box Plot Analysis', 
                           'Violin Plot Analysis', 'Cumulative Distribution'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Prepare data
        all_data = []
        for scenario, results in self.results.items():
            samples = results['samples']
            if 'Total_Estimate' in samples.columns:
                temp_df = pd.DataFrame({
                    'Total_Estimate': samples['Total_Estimate'],
                    'Scenario': scenario
                })
                all_data.append(temp_df)
        
        if not all_data:
            print("❌ Tidak ada data Total_Estimate untuk dashboard")
            return
        
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # 1. Distribution comparison (Histogram)
        for i, scenario in enumerate(self.results.keys()):
            if 'Total_Estimate' in self.results[scenario]['samples'].columns:
                data = self.results[scenario]['samples']['Total_Estimate']
                fig.add_trace(
                    go.Histogram(
                        x=data,
                        name=scenario,
                        opacity=0.7,
                        nbinsx=50,
                        legendgroup=scenario,
                        marker_color=self.colors[i % len(self.colors)]
                    ),
                    row=1, col=1
                )
        
        # 2. Box plots
        for i, scenario in enumerate(self.results.keys()):
            if 'Total_Estimate' in self.results[scenario]['samples'].columns:
                data = self.results[scenario]['samples']['Total_Estimate']
                fig.add_trace(
                    go.Box(
                        y=data,
                        name=scenario,
                        legendgroup=scenario,
                        showlegend=False,
                        marker_color=self.colors[i % len(self.colors)]
                    ),
                    row=1, col=2
                )
        
        # 3. Violin plots
        for i, scenario in enumerate(self.results.keys()):
            if 'Total_Estimate' in self.results[scenario]['samples'].columns:
                data = self.results[scenario]['samples']['Total_Estimate']
                fig.add_trace(
                    go.Violin(
                        y=data,
                        name=scenario,
                        legendgroup=scenario,
                        showlegend=False,
                        marker_color=self.colors[i % len(self.colors)]
                    ),
                    row=2, col=1
                )
        
        # 4. Cumulative distribution
        for i, scenario in enumerate(self.results.keys()):
            if 'Total_Estimate' in self.results[scenario]['samples'].columns:
                data = self.results[scenario]['samples']['Total_Estimate']
                sorted_data = np.sort(data)
                y_vals = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
                
                fig.add_trace(
                    go.Scatter(
                        x=sorted_data,
                        y=y_vals,
                        mode='lines',
                        name=scenario,
                        legendgroup=scenario,
                        showlegend=False,
                        line=dict(color=self.colors[i % len(self.colors)], width=3)
                    ),
                    row=2, col=2
                )
        
        # Update layout
        fig.update_layout(
            title={
                'text': '🎯 Monte Carlo Simulation - Interactive Distribution Dashboard',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Total Estimate", row=1, col=1)
        fig.update_yaxes(title_text="Frequency", row=1, col=1)
        
        fig.update_yaxes(title_text="Total Estimate", row=1, col=2)
        fig.update_yaxes(title_text="Total Estimate", row=2, col=1)
        
        fig.update_xaxes(title_text="Total Estimate", row=2, col=2)
        fig.update_yaxes(title_text="Cumulative Probability", row=2, col=2)
        
        if save_path:
            fig.write_html(save_path)
            print(f"📁 Interactive dashboard saved: {save_path}")
        
        fig.show()
        return fig
    
    def create_risk_dashboard(self, save_path: str = None):
        """
        Buat interactive dashboard untuk analisis risiko.
        
        Args:
            save_path: Path untuk menyimpan HTML file
        """
        # Prepare risk data
        risk_data = []
        for scenario, results in self.results.items():
            if 'risk_metrics' in results:
                for var, metrics in results['risk_metrics'].items():
                    if 'Total_Estimate' in var:
                        risk_data.append({
                            'Scenario': scenario,
                            'Variable': var,
                            'VaR_95': metrics['var_95'],
                            'VaR_99': metrics['var_99'],
                            'CVaR_95': metrics['cvar_95'],
                            'Prob_Loss': metrics['prob_loss'] * 100,  # Convert to percentage
                            'Expected_Shortfall': metrics['expected_shortfall']
                        })
        
        if not risk_data:
            print("❌ Tidak ada data risk metrics untuk dashboard")
            return
        
        risk_df = pd.DataFrame(risk_data)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Value at Risk Comparison', 'Risk Metrics Radar Chart',
                           'Probability of Loss', 'Expected Shortfall vs VaR'),
            specs=[[{"type": "bar"}, {"type": "scatterpolar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # 1. VaR Comparison (Bar chart)
        scenarios = risk_df['Scenario'].unique()
        
        fig.add_trace(
            go.Bar(
                x=scenarios,
                y=risk_df['VaR_95'],
                name='VaR 95%',
                marker_color='lightblue',
                text=[f'{val:,.0f}' for val in risk_df['VaR_95']],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=scenarios,
                y=risk_df['VaR_99'],
                name='VaR 99%',
                marker_color='darkblue',
                text=[f'{val:,.0f}' for val in risk_df['VaR_99']],
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # 2. Risk Metrics Radar Chart
        for i, scenario in enumerate(scenarios):
            scenario_data = risk_df[risk_df['Scenario'] == scenario].iloc[0]
            
            # Normalize metrics for radar chart (0-100 scale)
            normalized_metrics = {
                'VaR 95%': (scenario_data['VaR_95'] / risk_df['VaR_95'].max()) * 100,
                'VaR 99%': (scenario_data['VaR_99'] / risk_df['VaR_99'].max()) * 100,
                'CVaR 95%': (scenario_data['CVaR_95'] / risk_df['CVaR_95'].max()) * 100,
                'Prob Loss': scenario_data['Prob_Loss'],
                'Exp. Shortfall': (scenario_data['Expected_Shortfall'] / risk_df['Expected_Shortfall'].max()) * 100
            }
            
            fig.add_trace(
                go.Scatterpolar(
                    r=list(normalized_metrics.values()),
                    theta=list(normalized_metrics.keys()),
                    fill='toself',
                    name=scenario,
                    line_color=self.colors[i % len(self.colors)]
                ),
                row=1, col=2
            )
        
        # 3. Probability of Loss
        fig.add_trace(
            go.Bar(
                x=scenarios,
                y=risk_df['Prob_Loss'],
                name='Probability of Loss (%)',
                marker_color='red',
                text=[f'{val:.1f}%' for val in risk_df['Prob_Loss']],
                textposition='auto',
                showlegend=False
            ),
            row=2, col=1
        )
        
        # 4. Expected Shortfall vs VaR scatter
        fig.add_trace(
            go.Scatter(
                x=risk_df['VaR_95'],
                y=risk_df['Expected_Shortfall'],
                mode='markers+text',
                text=scenarios,
                textposition='top center',
                marker=dict(
                    size=12,
                    color=risk_df['Prob_Loss'],
                    colorscale='Reds',
                    showscale=True,
                    colorbar=dict(title="Prob. Loss (%)")
                ),
                name='Risk Profile',
                showlegend=False
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title={
                'text': '⚠️ Monte Carlo Simulation - Interactive Risk Dashboard',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            height=800,
            showlegend=True
        )
        
        # Update axes
        fig.update_xaxes(title_text="Scenario", row=1, col=1)
        fig.update_yaxes(title_text="Value at Risk", row=1, col=1)
        
        fig.update_xaxes(title_text="Scenario", row=2, col=1)
        fig.update_yaxes(title_text="Probability (%)", row=2, col=1)
        
        fig.update_xaxes(title_text="VaR 95%", row=2, col=2)
        fig.update_yaxes(title_text="Expected Shortfall", row=2, col=2)
        
        if save_path:
            fig.write_html(save_path)
            print(f"📁 Interactive risk dashboard saved: {save_path}")
        
        fig.show()
        return fig
    
    def create_sensitivity_dashboard(self, base_scenario: str = 'baseline', save_path: str = None):
        """
        Buat interactive dashboard untuk sensitivity analysis.
        
        Args:
            base_scenario: Skenario baseline
            save_path: Path untuk menyimpan HTML file
        """
        if base_scenario not in self.results:
            print(f"❌ Base scenario '{base_scenario}' tidak ditemukan")
            return
        
        # Prepare sensitivity data
        base_stats = self.results[base_scenario]['statistics']
        sensitivity_data = []
        
        for scenario, results in self.results.items():
            if scenario != base_scenario:
                stats = results['statistics']
                for var in ['Material_Cost', 'Labor_Cost', 'Total_Estimate']:
                    if var in base_stats and var in stats:
                        base_mean = base_stats[var]['mean']
                        scenario_mean = stats[var]['mean']
                        change_pct = ((scenario_mean - base_mean) / base_mean) * 100
                        
                        sensitivity_data.append({
                            'Scenario': scenario,
                            'Variable': var,
                            'Base_Mean': base_mean,
                            'Scenario_Mean': scenario_mean,
                            'Change_Percent': change_pct,
                            'Absolute_Change': scenario_mean - base_mean
                        })
        
        if not sensitivity_data:
            print("❌ Tidak ada data untuk sensitivity analysis")
            return
        
        sens_df = pd.DataFrame(sensitivity_data)
        
        # Create interactive plots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Sensitivity Heatmap', 'Tornado Chart',
                           'Variable Impact Comparison', 'Scenario Impact Summary'),
            specs=[[{"type": "heatmap"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # 1. Sensitivity Heatmap
        pivot_df = sens_df.pivot(index='Variable', columns='Scenario', values='Change_Percent')
        
        fig.add_trace(
            go.Heatmap(
                z=pivot_df.values,
                x=pivot_df.columns,
                y=pivot_df.index,
                colorscale='RdYlBu_r',
                text=[[f'{val:.1f}%' for val in row] for row in pivot_df.values],
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Change (%)")
            ),
            row=1, col=1
        )
        
        # 2. Tornado Chart (for Total_Estimate)
        total_est_data = sens_df[sens_df['Variable'] == 'Total_Estimate'].copy()
        total_est_data = total_est_data.reindex(total_est_data['Absolute_Change'].abs().sort_values().index)
        
        colors_tornado = ['red' if x < 0 else 'green' for x in total_est_data['Absolute_Change']]
        
        fig.add_trace(
            go.Bar(
                y=total_est_data['Scenario'],
                x=total_est_data['Absolute_Change'],
                orientation='h',
                marker_color=colors_tornado,
                text=[f'{val:,.0f}' for val in total_est_data['Absolute_Change']],
                textposition='auto',
                name='Impact on Total Estimate',
                showlegend=False
            ),
            row=1, col=2
        )
        
        # 3. Variable Impact Comparison
        variables = sens_df['Variable'].unique()
        for i, var in enumerate(variables):
            var_data = sens_df[sens_df['Variable'] == var]
            fig.add_trace(
                go.Bar(
                    x=var_data['Scenario'],
                    y=var_data['Change_Percent'],
                    name=var,
                    marker_color=self.colors[i % len(self.colors)],
                    text=[f'{val:.1f}%' for val in var_data['Change_Percent']],
                    textposition='auto'
                ),
                row=2, col=1
            )
        
        # 4. Scenario Impact Summary (Bubble chart)
        scenario_summary = sens_df.groupby('Scenario').agg({
            'Change_Percent': ['mean', 'std'],
            'Absolute_Change': 'sum'
        }).round(2)
        
        scenario_summary.columns = ['Mean_Change', 'Std_Change', 'Total_Impact']
        scenario_summary = scenario_summary.reset_index()
        
        fig.add_trace(
            go.Scatter(
                x=scenario_summary['Mean_Change'],
                y=scenario_summary['Std_Change'],
                mode='markers+text',
                text=scenario_summary['Scenario'],
                textposition='top center',
                marker=dict(
                    size=np.abs(scenario_summary['Total_Impact']) / 1000,  # Scale bubble size
                    color=scenario_summary['Mean_Change'],
                    colorscale='RdYlBu_r',
                    showscale=True,
                    colorbar=dict(title="Mean Change (%)")
                ),
                name='Scenario Profile',
                showlegend=False
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title={
                'text': '🎯 Monte Carlo Simulation - Interactive Sensitivity Dashboard',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            height=800,
            showlegend=True
        )
        
        # Update axes
        fig.update_xaxes(title_text="Scenario", row=1, col=1)
        fig.update_yaxes(title_text="Variable", row=1, col=1)
        
        fig.update_xaxes(title_text="Impact on Total Estimate", row=1, col=2)
        fig.update_yaxes(title_text="Scenario", row=1, col=2)
        
        fig.update_xaxes(title_text="Scenario", row=2, col=1)
        fig.update_yaxes(title_text="Change (%)", row=2, col=1)
        
        fig.update_xaxes(title_text="Mean Change (%)", row=2, col=2)
        fig.update_yaxes(title_text="Standard Deviation (%)", row=2, col=2)
        
        if save_path:
            fig.write_html(save_path)
            print(f"📁 Interactive sensitivity dashboard saved: {save_path}")
        
        fig.show()
        return fig
    
    def create_comprehensive_dashboard(self, save_dir: str = "./interactive_dashboards"):
        """
        Buat semua interactive dashboards.
        
        Args:
            save_dir: Directory untuk menyimpan HTML files
        """
        import os
        
        # Create directory if not exists
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"\n🎛️ Creating comprehensive interactive dashboards...")
        print(f"📁 Saving to: {save_dir}")
        
        # 1. Distribution dashboard
        print("├── Creating distribution dashboard...")
        self.create_distribution_dashboard(f"{save_dir}/01_distribution_dashboard.html")
        
        # 2. Risk dashboard
        print("├── Creating risk dashboard...")
        self.create_risk_dashboard(f"{save_dir}/02_risk_dashboard.html")
        
        # 3. Sensitivity dashboard
        print("├── Creating sensitivity dashboard...")
        self.create_sensitivity_dashboard(save_path=f"{save_dir}/03_sensitivity_dashboard.html")
        
        print(f"\n✅ All interactive dashboards created successfully!")
        print(f"📁 HTML files saved in: {save_dir}")
        print(f"🌐 Open the HTML files in your browser to interact with the dashboards")

# Contoh penggunaan
if __name__ == "__main__":
    # Import dan jalankan simulasi
    from monte_carlo_simulation import PricingMonteCarloSimulation
    from data_loader import DataLoader
    
    print("🚀 Running Interactive Dashboard Demo...")
    
    # Load data
    loader = DataLoader("D:\\abdurachman.putra\\Downloads\\archive (2)\\construction_estimates.csv")
    loader.load_data()
    loader.clean_data()
    
    # Run simulation
    mc_sim = PricingMonteCarloSimulation(loader.data)
    mc_sim.fit_distributions()
    results = mc_sim.run_simulation(n_simulations=3000)  # Smaller sample for faster demo
    
    # Create interactive dashboard
    dashboard = InteractiveDashboard(results)
    
    # Generate individual dashboards
    print("\n🎛️ Generating interactive dashboards...")
    
    print("├── Distribution Dashboard")
    dashboard.create_distribution_dashboard()
    
    print("├── Risk Dashboard")
    dashboard.create_risk_dashboard()
    
    print("├── Sensitivity Dashboard")
    dashboard.create_sensitivity_dashboard()
    
    # Create comprehensive dashboards
    print("\n📋 Creating comprehensive interactive dashboards...")
    dashboard.create_comprehensive_dashboard()
    
    print("\n🎉 Interactive dashboard demo completed successfully!")
    print("🌐 Open the generated HTML files in your browser to explore the interactive features!")