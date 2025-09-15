import pandas as pd
import numpy as np
import base64
import os
from datetime import datetime
import json
from data_loader import DataLoader
from monte_carlo_simulation import PricingMonteCarloSimulation
from visualization_suite import MonteCarloVisualizer

class SimpleAIReportGenerator:
    """AI Report Generator dengan HTML template yang sederhana"""
    
    def __init__(self, simulation_results, data_loader, output_dir="./ai_report_output"):
        self.results = simulation_results
        self.data_loader = data_loader
        self.output_dir = output_dir
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def _create_executive_summary(self):
        """Create executive summary dengan bahasa conversational"""
        baseline = self.results['baseline']['samples']
        mean_estimate = baseline['Total_Estimate'].mean()
        std_estimate = baseline['Total_Estimate'].std()
        
        return {
            'greeting': "🤖 Halo! Saya AI assistant Anda yang akan membantu menjelaskan hasil analisis Monte Carlo untuk proyek konstruksi Anda.",
            'main_finding': f"Berdasarkan simulasi 10,000 skenario, estimasi biaya rata-rata proyek Anda adalah **Rp {mean_estimate:,.0f}** dengan variasi sekitar **Rp {std_estimate:,.0f}**.",
            'simple_explanation': "Bayangkan Anda menjalankan proyek serupa 10,000 kali dengan kondisi yang berbeda-beda. Inilah gambaran biaya yang paling mungkin terjadi.",
            'confidence_level': "Saya cukup yakin dengan prediksi ini karena didasarkan pada analisis data historis 1,000 proyek konstruksi."
        }
    
    def _create_risk_explanation(self):
        """Explain risk dengan analogi sederhana"""
        baseline = self.results['baseline']['samples']
        total_estimate = baseline['Total_Estimate']
        cv = total_estimate.std() / total_estimate.mean()
        
        if cv < 0.1:
            risk_level, emoji = "rendah", "🟢"
        elif cv < 0.2:
            risk_level, emoji = "sedang", "🟡"
        else:
            risk_level, emoji = "tinggi", "🔴"
        
        return {
            'risk_level': risk_level,
            'emoji': emoji,
            'explanation': f"Tingkat risiko proyek Anda adalah **{risk_level}** {emoji}. Ini seperti cuaca - semakin tinggi variasi, semakin tidak dapat diprediksi.",
            'practical_meaning': "Artinya, Anda perlu menyiapkan buffer dana untuk mengantisipasi kemungkinan kenaikan biaya.",
            'recommendation': "Saya sarankan untuk menyiapkan dana cadangan sekitar 15-20% dari estimasi rata-rata."
        }
    
    def _create_scenario_insights(self):
        """Create insights untuk berbagai skenario"""
        scenarios_analysis = {}
        baseline_mean = self.results['baseline']['samples']['Total_Estimate'].mean()
        
        scenario_names = {
            'material_increase_10pct': 'Kenaikan Material 10%',
            'labor_increase_15pct': 'Kenaikan Tenaga Kerja 15%',
            'combined_increase': 'Kenaikan Kombinasi'
        }
        
        for scenario_name, scenario_data in self.results.items():
            if scenario_name == 'baseline':
                continue
                
            scenario_mean = scenario_data['samples']['Total_Estimate'].mean()
            impact = ((scenario_mean - baseline_mean) / baseline_mean) * 100
            
            scenarios_analysis[scenario_name] = {
                'name': scenario_names.get(scenario_name, scenario_name),
                'impact_percentage': impact,
                'impact_amount': scenario_mean - baseline_mean,
                'new_estimate': scenario_mean
            }
        
        return scenarios_analysis
    
    def _encode_image_to_base64(self, image_path):
        """Encode image to base64 untuk embedding di HTML"""
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                return f"data:image/png;base64,{encoded_string}"
        except:
            return ""
    
    def generate_report(self):
        """Generate HTML report dengan design yang eye-catching"""
        print("🤖 Generating AI-powered HTML report...")
        
        # Generate insights
        executive_summary = self._create_executive_summary()
        risk_explanation = self._create_risk_explanation()
        scenario_insights = self._create_scenario_insights()
        
        # Encode charts
        chart_paths = {
            'distribution': './monte_carlo_report/01_distribution_analysis.png',
            'risk_metrics': './monte_carlo_report/02_risk_metrics.png',
            'scenario_comparison': './monte_carlo_report/03_scenario_comparison.png',
            'correlation': './monte_carlo_report/04_correlation_heatmap.png',
            'sensitivity': './monte_carlo_report/05_sensitivity_analysis.png'
        }
        
        encoded_charts = {}
        for name, path in chart_paths.items():
            encoded_charts[name] = self._encode_image_to_base64(path)
        
        # Create HTML content
        html_content = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 AI-Powered Monte Carlo Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        
        .hero h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        
        .hero p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .card {{
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }}
        
        .card h2 {{
            color: #667eea;
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }}
        
        .card h3 {{
            color: #764ba2;
            margin-bottom: 0.5rem;
            font-size: 1.3rem;
        }}
        
        .highlight {{
            background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }}
        
        .risk-indicator {{
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-weight: bold;
            margin: 0.5rem 0;
        }}
        
        .risk-low {{
            background: #d4edda;
            color: #155724;
        }}
        
        .risk-medium {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .risk-high {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .scenario-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .scenario-card {{
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #ff6b6b;
        }}
        
        .chart-container {{
            text-align: center;
            margin: 2rem 0;
        }}
        
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .ai-avatar {{
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: white;
            margin-bottom: 1rem;
        }}
        
        .timestamp {{
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            margin-top: 2rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <div class="hero">
            <h1>🎯 AI-Powered Monte Carlo Analysis</h1>
            <p>Laporan Analisis Risiko Proyek Konstruksi</p>
            <div class="timestamp">Generated on {datetime.now().strftime('%d %B %Y, %H:%M')}</div>
        </div>
        
        <!-- Executive Summary -->
        <div class="card">
            <div class="ai-avatar">🤖</div>
            <h2>📋 Ringkasan Eksekutif</h2>
            <div class="highlight">
                <p>{executive_summary['greeting']}</p>
            </div>
            <p><strong>{executive_summary['main_finding']}</strong></p>
            <p>{executive_summary['simple_explanation']}</p>
            <p><em>{executive_summary['confidence_level']}</em></p>
        </div>
        
        <!-- Risk Analysis -->
        <div class="card">
            <h2>⚠️ Analisis Risiko</h2>
            <div class="risk-indicator risk-{risk_explanation['risk_level']}">
                {risk_explanation['emoji']} Risiko {risk_explanation['risk_level'].title()}
            </div>
            <p>{risk_explanation['explanation']}</p>
            <p>{risk_explanation['practical_meaning']}</p>
            <div class="highlight">
                <strong>💡 Rekomendasi:</strong> {risk_explanation['recommendation']}
            </div>
        </div>
        
        <!-- Scenario Analysis -->
        <div class="card">
            <h2>📊 Analisis Skenario</h2>
            <p>Mari kita lihat bagaimana perubahan kondisi dapat mempengaruhi biaya proyek:</p>
            <div class="scenario-grid">
"""
        
        # Add scenario cards
        for scenario_key, scenario_data in scenario_insights.items():
            impact_color = "#e74c3c" if scenario_data['impact_percentage'] > 0 else "#27ae60"
            html_content += f"""
                <div class="scenario-card">
                    <h3>{scenario_data['name']}</h3>
                    <p><strong>Dampak:</strong> <span style="color: {impact_color}">{scenario_data['impact_percentage']:+.1f}%</span></p>
                    <p><strong>Perubahan Biaya:</strong> Rp {scenario_data['impact_amount']:,.0f}</p>
                    <p><strong>Estimasi Baru:</strong> Rp {scenario_data['new_estimate']:,.0f}</p>
                </div>
"""
        
        html_content += """
            </div>
        </div>
        
        <!-- Charts Section -->
        <div class="card">
            <h2>📈 Visualisasi Data</h2>
            
            <h3>Analisis Distribusi</h3>
            <div class="chart-container">
"""
        
        if encoded_charts['distribution']:
            html_content += f'<img src="{encoded_charts["distribution"]}" alt="Distribution Analysis">'
        
        html_content += """
            </div>
            
            <h3>Perbandingan Risiko</h3>
            <div class="chart-container">
"""
        
        if encoded_charts['risk_metrics']:
            html_content += f'<img src="{encoded_charts["risk_metrics"]}" alt="Risk Metrics">'
        
        html_content += """
            </div>
            
            <h3>Perbandingan Skenario</h3>
            <div class="chart-container">
"""
        
        if encoded_charts['scenario_comparison']:
            html_content += f'<img src="{encoded_charts["scenario_comparison"]}" alt="Scenario Comparison">'
        
        html_content += """
            </div>
            
            <h3>Analisis Korelasi</h3>
            <div class="chart-container">
"""
        
        if encoded_charts['correlation']:
            html_content += f'<img src="{encoded_charts["correlation"]}" alt="Correlation Analysis">'
        
        html_content += """
            </div>
            
            <h3>Analisis Sensitivitas</h3>
            <div class="chart-container">
"""
        
        if encoded_charts['sensitivity']:
            html_content += f'<img src="{encoded_charts["sensitivity"]}" alt="Sensitivity Analysis">'
        
        html_content += """
            </div>
        </div>
        
        <!-- Footer -->
        <div class="card">
            <h2>🎉 Kesimpulan</h2>
            <p>Analisis Monte Carlo ini memberikan gambaran komprehensif tentang risiko dan peluang dalam proyek konstruksi Anda. Gunakan informasi ini untuk membuat keputusan yang lebih baik dan mengelola risiko dengan efektif.</p>
            <div class="highlight">
                <strong>💡 Tips:</strong> Selalu pertimbangkan skenario terburuk dan siapkan rencana mitigasi risiko yang sesuai.
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        # Save HTML file
        report_path = os.path.join(self.output_dir, "monte_carlo_ai_report.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ AI Report generated successfully!")
        print(f"📄 Report saved to: {report_path}")
        
        return report_path

if __name__ == "__main__":
    # Load data and run simulation
    CSV_PATH = r"D:\python_projects\learning\montecarlo\dataset\construction_estimates.csv"
    
    print("🔄 Loading data and running Monte Carlo simulation...")
    
    # Load and clean data
    loader = DataLoader(CSV_PATH)
    loader.load_data()
    loader.clean_data()
    
    # Run Monte Carlo simulation
    mc_sim = PricingMonteCarloSimulation(loader.data)
    mc_sim.fit_distributions()
    
    # Define scenarios
    scenarios = {
        'baseline': {},
        'material_increase_10pct': {'Material_Cost': 1.1},
        'labor_increase_15pct': {'Labor_Cost': 1.15},
        'combined_increase': {'Material_Cost': 1.1, 'Labor_Cost': 1.15}
    }
    
    # Run simulation
    print("Running Monte Carlo simulation...")
    results = mc_sim.run_simulation(
        n_simulations=10000,
        scenarios=scenarios
    )
    
    # Generate visualizations
    visualizer = MonteCarloVisualizer(results)
    visualizer.create_comprehensive_report()
    
    # Generate AI report
    ai_report = SimpleAIReportGenerator(results, loader)
    report_path = ai_report.generate_report()
    
    print(f"\n🎉 AI-Powered Report completed!")
    print(f"📄 Open this file in your browser: {report_path}")