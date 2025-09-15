#!/usr/bin/env python3
"""
Monte Carlo Simulation for Construction Pricing Analysis

Script utama yang menggabungkan semua komponen:
- Data loading dan preprocessing
- Monte Carlo simulation
- Static visualizations
- Interactive dashboards
- Risk analysis dan sensitivity analysis

Author: AI Assistant
Date: 2024
"""

import os
import sys
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from data_loader import DataLoader
from monte_carlo_simulation import PricingMonteCarloSimulation
from visualization_suite import MonteCarloVisualizer
from interactive_dashboard import InteractiveDashboard

def print_header():
    """Print aplikasi header"""
    print("\n" + "="*80)
    print("🎯 MONTE CARLO SIMULATION FOR CONSTRUCTION PRICING ANALYSIS")
    print("="*80)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔧 Components: Data Analysis | Monte Carlo | Visualization | Dashboard")
    print("="*80)

def print_section(title: str, emoji: str = "📊"):
    """Print section header"""
    print(f"\n{emoji} {title.upper()}")
    print("-" * (len(title) + 4))

def main():
    """Fungsi utama untuk menjalankan seluruh pipeline Monte Carlo"""
    
    # Print header
    print_header()
    
    # Configuration
    CSV_PATH = r"D:\python_projects\learning\montecarlo\dataset\construction_estimates.csv"
    N_SIMULATIONS = 10000
    OUTPUT_DIR = "./monte_carlo_output"
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/static_plots", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/interactive_dashboards", exist_ok=True)
    
    try:
        # ================================================================
        # STEP 1: DATA LOADING AND PREPROCESSING
        # ================================================================
        print_section("Step 1: Data Loading and Preprocessing", "📂")
        
        print(f"📁 Loading dataset from: {CSV_PATH}")
        loader = DataLoader(CSV_PATH)
        
        # Load and explore data
        if not loader.load_data():
            print("❌ Failed to load data. Please check the file path.")
            return False
        
        print("\n🔍 Data exploration:")
        sample_data = loader.explore_data()
        
        # Clean data
        print("\n🧹 Cleaning data...")
        loader.clean_data()
        
        # Analyze distributions
        print("\n📊 Analyzing distributions...")
        dist_results = loader.analyze_distributions()
        
        # Correlation analysis
        print("\n🔗 Correlation analysis...")
        corr_results = loader.correlation_analysis()
        
        print("✅ Data preprocessing completed successfully!")
        
        # ================================================================
        # STEP 2: MONTE CARLO SIMULATION
        # ================================================================
        print_section("Step 2: Monte Carlo Simulation", "🎲")
        
        print(f"🎯 Initializing Monte Carlo simulation with {N_SIMULATIONS:,} iterations")
        mc_sim = PricingMonteCarloSimulation(loader.data)
        
        # Fit distributions
        print("\n📈 Fitting statistical distributions...")
        distributions = mc_sim.fit_distributions(['norm', 'lognorm', 'gamma', 'uniform'])
        
        # Define scenarios
        scenarios = {
            'baseline': {},
            'material_increase_10pct': {'Material_Cost': 1.1},
            'material_increase_20pct': {'Material_Cost': 1.2},
            'labor_increase_15pct': {'Labor_Cost': 1.15},
            'labor_increase_25pct': {'Labor_Cost': 1.25},
            'combined_moderate': {'Material_Cost': 1.1, 'Labor_Cost': 1.15},
            'combined_aggressive': {'Material_Cost': 1.2, 'Labor_Cost': 1.25},
            'cost_reduction': {'Material_Cost': 0.9, 'Labor_Cost': 0.95}
        }
        
        print(f"\n🚀 Running simulation with {len(scenarios)} scenarios...")
        results = mc_sim.run_simulation(n_simulations=N_SIMULATIONS, scenarios=scenarios)
        
        # Print summary statistics
        print("\n📋 SIMULATION RESULTS SUMMARY")
        print("=" * 50)
        
        for scenario in ['baseline', 'combined_moderate', 'combined_aggressive']:
            if scenario in results:
                print(f"\n🎯 {scenario.upper()}:")
                summary = mc_sim.get_summary_statistics(scenario)
                print(summary.to_string(index=False))
                
                # Risk analysis
                mc_sim.print_risk_analysis(scenario)
        
        print("✅ Monte Carlo simulation completed successfully!")
        
        # ================================================================
        # STEP 3: STATIC VISUALIZATIONS
        # ================================================================
        print_section("Step 3: Static Visualizations", "📊")
        
        print("🎨 Creating static visualizations...")
        visualizer = MonteCarloVisualizer(results)
        
        # Generate comprehensive report
        static_dir = f"{OUTPUT_DIR}/static_plots"
        print(f"📁 Saving static plots to: {static_dir}")
        visualizer.create_comprehensive_report(static_dir)
        
        print("✅ Static visualizations completed successfully!")
        
        # ================================================================
        # STEP 4: INTERACTIVE DASHBOARDS
        # ================================================================
        print_section("Step 4: Interactive Dashboards", "🎛️")
        
        print("🌐 Creating interactive dashboards...")
        dashboard = InteractiveDashboard(results)
        
        # Generate comprehensive dashboards
        dashboard_dir = f"{OUTPUT_DIR}/interactive_dashboards"
        print(f"📁 Saving interactive dashboards to: {dashboard_dir}")
        dashboard.create_comprehensive_dashboard(dashboard_dir)
        
        print("✅ Interactive dashboards completed successfully!")
        
        # ================================================================
        # STEP 5: SUMMARY AND RECOMMENDATIONS
        # ================================================================
        print_section("Step 5: Summary and Recommendations", "📋")
        
        # Generate summary report
        generate_summary_report(results, mc_sim, OUTPUT_DIR)
        
        print("✅ Summary report generated successfully!")
        
        # ================================================================
        # COMPLETION
        # ================================================================
        print_section("Completion", "🎉")
        
        print(f"📁 All outputs saved to: {os.path.abspath(OUTPUT_DIR)}")
        print("\n📊 Generated Files:")
        print("├── Static Plots:")
        print("│   ├── 01_distribution_analysis.png")
        print("│   ├── 02_risk_metrics.png")
        print("│   ├── 03_scenario_comparison.png")
        print("│   ├── 04_correlation_heatmap.png")
        print("│   └── 05_sensitivity_analysis.png")
        print("├── Interactive Dashboards:")
        print("│   ├── 01_distribution_dashboard.html")
        print("│   ├── 02_risk_dashboard.html")
        print("│   └── 03_sensitivity_dashboard.html")
        print("└── summary_report.txt")
        
        print("\n🌐 To view interactive dashboards:")
        print(f"   Open the HTML files in {dashboard_dir} with your web browser")
        
        print("\n🎯 Monte Carlo Analysis Completed Successfully!")
        print(f"⏱️  Total execution time: {time.time() - start_time:.2f} seconds")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("🔧 Please check the error details and try again.")
        return False

def generate_summary_report(results: dict, mc_sim, output_dir: str):
    """Generate text summary report"""
    
    report_path = f"{output_dir}/summary_report.txt"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("MONTE CARLO SIMULATION - CONSTRUCTION PRICING ANALYSIS\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Executive Summary
        f.write("EXECUTIVE SUMMARY\n")
        f.write("-" * 20 + "\n")
        f.write("This Monte Carlo simulation analyzed construction pricing data to assess\n")
        f.write("risk and uncertainty in project cost estimates. The analysis included\n")
        f.write("multiple scenarios with varying material and labor cost assumptions.\n\n")
        
        # Key Findings
        f.write("KEY FINDINGS\n")
        f.write("-" * 15 + "\n")
        
        baseline_stats = results['baseline']['statistics']['Total_Estimate']
        f.write(f"• Baseline Total Estimate: ${baseline_stats['mean']:,.2f} (mean)\n")
        f.write(f"• Standard Deviation: ${baseline_stats['std']:,.2f}\n")
        f.write(f"• 95% Confidence Interval: ${baseline_stats['q25']:,.2f} - ${baseline_stats['q75']:,.2f}\n")
        
        if 'risk_metrics' in results['baseline']:
            risk_metrics = results['baseline']['risk_metrics']['Total_Estimate']
            f.write(f"• Value at Risk (95%): ${risk_metrics['var_95']:,.2f}\n")
            f.write(f"• Probability of Loss: {risk_metrics['prob_loss']:.1%}\n")
        
        f.write("\n")
        
        # Scenario Analysis
        f.write("SCENARIO ANALYSIS\n")
        f.write("-" * 20 + "\n")
        
        for scenario, data in results.items():
            if scenario != 'baseline':
                stats = data['statistics']['Total_Estimate']
                baseline_mean = baseline_stats['mean']
                change_pct = ((stats['mean'] - baseline_mean) / baseline_mean) * 100
                
                f.write(f"\n{scenario.replace('_', ' ').title()}:\n")
                f.write(f"  • Mean Estimate: ${stats['mean']:,.2f}\n")
                f.write(f"  • Change from Baseline: {change_pct:+.1f}%\n")
                f.write(f"  • Standard Deviation: ${stats['std']:,.2f}\n")
        
        f.write("\n")
        
        # Recommendations
        f.write("RECOMMENDATIONS\n")
        f.write("-" * 16 + "\n")
        f.write("1. Risk Management: Consider hedging strategies for material cost volatility\n")
        f.write("2. Contingency Planning: Maintain 15-20% contingency for cost overruns\n")
        f.write("3. Scenario Planning: Regularly update cost assumptions based on market conditions\n")
        f.write("4. Monitoring: Track actual costs against simulated ranges for model validation\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("End of Report\n")
    
    print(f"📄 Summary report saved: {report_path}")

if __name__ == "__main__":
    # Record start time
    start_time = time.time()
    
    # Run main function
    success = main()
    
    if success:
        print("\n🎊 Program executed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Program failed to execute.")
        sys.exit(1)