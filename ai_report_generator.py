import pandas as pd
import numpy as np
import base64
import os
from datetime import datetime
import json
import google.generativeai as genai
from data_loader import DataLoader
from monte_carlo_simulation import PricingMonteCarloSimulation
from visualization_suite import MonteCarloVisualizer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
genai.configure(api_key=api_key)

class AIReportGenerator:
    """
    AI-Powered HTML Report Generator untuk Monte Carlo Analysis
    Menghasilkan laporan yang eye-catching dan mudah dipahami untuk orang awam
    Menggunakan Google Gemini AI untuk generate insights yang dinamis
    """
    
    def __init__(self, simulation_results, data_loader, output_dir="./ai_report_output"):
        self.results = simulation_results
        self.data_loader = data_loader
        self.output_dir = output_dir
        self.report_data = {}
        
        # Initialize Gemini AI model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def _call_gemini_ai(self, prompt):
        """Helper function to call Gemini AI with error handling"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"⚠️ Gemini AI error: {e}")
            return "AI tidak dapat menghasilkan insight saat ini. Menggunakan analisis statistik standar."
    
    def _parse_ai_response_to_summary(self, ai_response, mean_estimate, std_estimate):
        """Parse AI response when JSON parsing fails"""
        return {
            'greeting': "🤖 Halo! Saya AI assistant Anda yang menganalisis hasil Monte Carlo.",
            'main_finding': f"Berdasarkan analisis AI: {ai_response[:200]}...",
            'simple_explanation': f"Estimasi rata-rata: Rp {mean_estimate:,.0f} dengan variasi Rp {std_estimate:,.0f}",
            'confidence_level': "Analisis ini dihasilkan menggunakan Google Gemini AI."
        }
        
    def _generate_ai_insights(self):
        """Generate AI-powered insights dan explanations"""
        insights = {
            'executive_summary': self._create_executive_summary(),
            'data_story': self._create_data_story(),
            'risk_explanation': self._create_risk_explanation(),
            'scenario_insights': self._create_scenario_insights(),
            'recommendations': self._create_recommendations()
        }
        return insights
    
    def _create_executive_summary(self):
        """Create executive summary menggunakan Gemini AI"""
        baseline = self.results['baseline']['samples']
        mean_estimate = baseline['Total_Estimate'].mean()
        std_estimate = baseline['Total_Estimate'].std()
        min_estimate = baseline['Total_Estimate'].min()
        max_estimate = baseline['Total_Estimate'].max()
        
        # Prepare data for AI analysis
        prompt = f"""
Anda adalah AI assistant yang ahli dalam analisis Monte Carlo untuk proyek konstruksi. 
Berdasarkan data simulasi berikut, buatlah executive summary yang conversational dan mudah dipahami:

Data Simulasi Monte Carlo (10,000 iterasi):
- Estimasi biaya rata-rata: Rp {mean_estimate:,.0f}
- Standar deviasi: Rp {std_estimate:,.0f}
- Estimasi minimum: Rp {min_estimate:,.0f}
- Estimasi maksimum: Rp {max_estimate:,.0f}
- Coefficient of Variation: {(std_estimate/mean_estimate)*100:.1f}%

Buatlah 4 komponen berikut dalam format JSON:
1. greeting: Sapaan ramah sebagai AI assistant
2. main_finding: Temuan utama dengan angka-angka penting
3. simple_explanation: Penjelasan sederhana dengan analogi yang mudah dipahami
4. confidence_level: Tingkat kepercayaan terhadap prediksi

Gunakan bahasa Indonesia yang conversational dan profesional. Fokus pada insight praktis untuk decision making.
"""
        
        try:
            ai_response = self._call_gemini_ai(prompt)
            # Try to parse JSON response
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: parse manually or use default
                return self._parse_ai_response_to_summary(ai_response, mean_estimate, std_estimate)
        except:
            # Fallback to original method if AI fails
            return {
                'greeting': "🤖 Halo! Saya AI assistant Anda yang akan membantu menjelaskan hasil analisis Monte Carlo untuk proyek konstruksi Anda.",
                'main_finding': f"Berdasarkan simulasi 10,000 skenario, estimasi biaya rata-rata proyek Anda adalah **Rp {mean_estimate:,.0f}** dengan variasi sekitar **Rp {std_estimate:,.0f}**.",
                'simple_explanation': "Bayangkan Anda menjalankan proyek serupa 10,000 kali dengan kondisi yang berbeda-beda. Inilah gambaran biaya yang paling mungkin terjadi.",
                'confidence_level': "Saya cukup yakin dengan prediksi ini karena didasarkan pada analisis data historis 1,000 proyek konstruksi."
            }
    
    def _create_data_story(self):
        """Explain data dengan storytelling approach"""
        data_info = {
            'total_projects': len(self.data_loader.data),
            'variables_analyzed': len(self.data_loader.data.columns),
            'story': "Mari saya ceritakan tentang data yang kita analisis...",
            'explanation': [
                "📊 Kita menganalisis **1,000 proyek konstruksi** dengan 6 faktor utama",
                "🏗️ Setiap proyek memiliki karakteristik biaya material, tenaga kerja, dan profit yang berbeda",
                "🎯 Tujuannya: memprediksi biaya proyek Anda berdasarkan pola historis",
                "🔍 Seperti melihat kristal bola, tapi menggunakan matematika dan data!"
            ]
        }
        return data_info
    
    def _create_risk_explanation(self):
        """Explain risk metrics menggunakan Gemini AI"""
        baseline = self.results['baseline']['samples']
        var_95 = np.percentile(baseline['Total_Estimate'], 95)
        var_99 = np.percentile(baseline['Total_Estimate'], 99)
        mean_estimate = baseline['Total_Estimate'].mean()
        cv = baseline['Total_Estimate'].std() / mean_estimate
        
        prompt = f"""
Anda adalah AI expert dalam risk management untuk proyek konstruksi.
Berdasarkan hasil Monte Carlo simulation, jelaskan risiko dengan bahasa yang mudah dipahami:

Data Risiko:
- Value at Risk 95%: Rp {var_95:,.0f}
- Value at Risk 99%: Rp {var_99:,.0f}
- Estimasi rata-rata: Rp {mean_estimate:,.0f}
- Coefficient of Variation: {cv*100:.1f}%

Buatlah penjelasan risiko yang mencakup:
1. intro: Pengantar tentang pentingnya memahami risiko
2. var_explanation: Penjelasan VaR dengan analogi sederhana
3. risk_level: Tingkat risiko (rendah/sedang/tinggi) berdasarkan CV
4. what_to_do: Rekomendasi praktis untuk mitigasi risiko

Gunakan bahasa Indonesia yang conversational, emoji, dan analogi yang mudah dipahami.
Format dalam JSON dengan 4 key di atas.
"""
        
        try:
            ai_response = self._call_gemini_ai(prompt)
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
            
        # Fallback to original method
        return {
            'intro': "⚠️ Mari kita bicara tentang risiko dengan bahasa yang mudah dipahami...",
            'var_explanation': {
                'simple': f"**VaR 95%** = Rp {var_95:,.0f} artinya: Bayangkan Anda menjalankan proyek serupa 100 kali. Dalam 95 kali, biaya tidak akan melebihi angka ini. Hanya 5 kali yang mungkin lebih mahal.",
                'analogy': "Seperti ramalan cuaca: 95% kemungkinan tidak hujan, tapi tetap bawa payung untuk 5% sisanya! ☂️"
            },
            'risk_level': self._assess_risk_level(baseline),
            'what_to_do': "💡 Apa yang harus Anda lakukan dengan informasi ini? Siapkan contingency budget sekitar 10-15% dari estimasi dasar."
        }
    
    def _assess_risk_level(self, data):
        """Assess overall risk level"""
        cv = data['Total_Estimate'].std() / data['Total_Estimate'].mean()
        
        if cv < 0.1:
            return {'level': 'LOW', 'color': '#51cf66', 'emoji': '😊', 'description': 'Risiko rendah - proyek cukup predictable'}
        elif cv < 0.3:
            return {'level': 'MEDIUM', 'color': '#ffd43b', 'emoji': '😐', 'description': 'Risiko sedang - perlu monitoring'}
        else:
            return {'level': 'HIGH', 'color': '#ff8787', 'emoji': '😰', 'description': 'Risiko tinggi - perlu contingency plan'}
    
    def _create_scenario_insights(self):
        """Create insights untuk scenario comparison"""
        scenarios = []
        
        for scenario_name, data in self.results.items():
            if scenario_name == 'baseline':
                continue
                
            baseline_mean = self.results['baseline']['samples']['Total_Estimate'].mean()
            scenario_mean = data['samples']['Total_Estimate'].mean()
            impact = ((scenario_mean - baseline_mean) / baseline_mean) * 100
            
            scenarios.append({
                'name': scenario_name,
                'impact_percent': impact,
                'explanation': self._explain_scenario_impact(scenario_name, impact),
                'recommendation': self._get_scenario_recommendation(scenario_name, impact)
            })
        
        return {
            'intro': "🔍 Mari kita lihat apa yang terjadi jika kondisi berubah...",
            'scenarios': scenarios
        }
    
    def _explain_scenario_impact(self, scenario, impact):
        """Explain scenario impact dengan conversational tone"""
        explanations = {
            'material_increase_10pct': f"Jika harga material naik 10%, biaya proyek akan naik sekitar {impact:.1f}%. Seperti efek domino - satu komponen naik, total ikut naik.",
            'labor_increase_15pct': f"Kenaikan upah pekerja 15% akan menambah biaya sekitar {impact:.1f}%. Tenaga kerja adalah investasi penting!",
            'combined_increase': f"Kombinasi kenaikan material dan labor bisa menambah biaya hingga {impact:.1f}%. Double whammy yang perlu diantisipasi."
        }
        return explanations.get(scenario, f"Skenario ini akan mengubah biaya sekitar {impact:.1f}%.")
    
    def _get_scenario_recommendation(self, scenario, impact):
        """Get recommendation berdasarkan scenario"""
        if abs(impact) < 5:
            return "✅ Dampak minimal - tidak perlu tindakan khusus"
        elif abs(impact) < 15:
            return "⚠️ Dampak sedang - siapkan contingency budget"
        else:
            return "🚨 Dampak besar - perlu strategi mitigasi risiko"
    
    def _create_recommendations(self):
        """Create actionable recommendations menggunakan Gemini AI"""
        baseline = self.results['baseline']['samples']
        risk_level = self._assess_risk_level(baseline)
        mean_estimate = baseline['Total_Estimate'].mean()
        std_estimate = baseline['Total_Estimate'].std()
        cv = std_estimate / mean_estimate
        
        # Analisis skenario untuk konteks
        scenario_impacts = []
        for scenario_name, scenario_data in self.results.items():
            if scenario_name != 'baseline':
                scenario_mean = scenario_data['samples']['Total_Estimate'].mean()
                impact = ((scenario_mean - mean_estimate) / mean_estimate) * 100
                scenario_impacts.append(f"{scenario_name}: {impact:.1f}%")
        
        prompt = f"""
Anda adalah AI consultant untuk manajemen proyek konstruksi.
Berdasarkan hasil Monte Carlo simulation, buatlah rekomendasi actionable:

Data Analisis:
- Estimasi rata-rata: Rp {mean_estimate:,.0f}
- Standard deviasi: Rp {std_estimate:,.0f}
- Coefficient of Variation: {cv*100:.1f}%
- Tingkat risiko: {risk_level['level']} ({risk_level['description']})
- Dampak skenario: {', '.join(scenario_impacts)}

Buatlah rekomendasi yang mencakup:
1. intro: Pengantar singkat
2. actions: Array 3-4 rekomendasi dengan struktur:
   - title: Judul dengan emoji
   - action: Tindakan spesifik yang harus dilakukan
   - reason: Alasan berdasarkan data
3. closing: Penutup motivational

Gunakan bahasa Indonesia yang praktis dan actionable.
Format dalam JSON dengan struktur di atas.
"""
        
        try:
            ai_response = self._call_gemini_ai(prompt)
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
            
        # Fallback to original method
        recommendations = [
            {
                'title': '💰 Budget Planning',
                'action': f"Siapkan budget dasar Rp {mean_estimate:,.0f} + contingency 15%",
                'reason': 'Berdasarkan analisis risiko dan variabilitas historis'
            },
            {
                'title': '📊 Monitoring Key Metrics',
                'action': 'Pantau harga material dan upah pekerja secara berkala',
                'reason': 'Kedua faktor ini paling berpengaruh terhadap total biaya'
            },
            {
                'title': '🎯 Risk Mitigation',
                'action': f"Fokus pada mitigasi risiko {risk_level['level'].lower()}",
                'reason': f"Proyek Anda memiliki tingkat risiko {risk_level['description']}"
            }
        ]
        
        return {
            'intro': '💡 Berdasarkan analisis, ini yang sebaiknya Anda lakukan:',
            'actions': recommendations,
            'closing': '🚀 Dengan persiapan yang tepat, proyek Anda akan berjalan lebih smooth!'
        }
    
    def _encode_image_to_base64(self, image_path):
        """Convert image to base64 untuk embed di HTML"""
        try:
            with open(image_path, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except:
            return None
    
    def _get_html_template(self):
        """Generate simple HTML template for testing"""
        return """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 AI-Powered Monte Carlo Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .card {{ background: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 10px; }}
        .hero {{ background: #667eea; color: white; padding: 30px; text-align: center; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0; }}
        .metric-card {{ background: white; padding: 15px; border-radius: 8px; text-align: center; }}
        .chart-container {{ text-align: center; margin: 20px 0; }}
        .chart-container img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>🎯 AI-Powered Monte Carlo Analysis Report</h1>
        <p>Generated on {timestamp}</p>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>📊 Executive Summary</h2>
            <p>{executive_greeting}</p>
            <p><strong>{executive_main_finding}</strong></p>
            <p><em>{executive_simple_explanation}</em></p>
            <p>{executive_confidence}</p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div><strong>{mean_estimate}</strong></div>
                    <div>Estimasi Rata-rata</div>
                </div>
                <div class="metric-card">
                    <div><strong>{std_estimate}</strong></div>
                    <div>Variasi (±)</div>
                </div>
                <div class="metric-card">
                    <div><strong>{risk_level_emoji}</strong></div>
                    <div>Tingkat Risiko</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>📈 Cerita Data</h2>
            <p>{data_story}</p>
            <ul>{data_explanation_list}</ul>
            <div class="chart-container">
                <img src="data:image/png;base64,{distribution_chart}" alt="Distribution Analysis">
            </div>
        </div>
        
        <div class="card">
            <h2>⚠️ Analisis Risiko</h2>
            <p>{risk_intro}</p>
            <p>{var_explanation}</p>
            <p>{var_analogy}</p>
            <p>{what_to_do}</p>
            <div class="chart-container">
                <img src="data:image/png;base64,{risk_chart}" alt="Risk Analysis">
            </div>
        </div>
        
        <div class="card">
            <h2>🔍 Skenario Analysis</h2>
            <p>{scenario_intro}</p>
            {scenario_cards}
            <div class="chart-container">
                <img src="data:image/png;base64,{scenario_chart}" alt="Scenario Analysis">
            </div>
        </div>
        
        <div class="card">
            <h2>💡 Rekomendasi</h2>
            <p>{recommendations_intro}</p>
            {recommendation_cards}
            <p>{recommendations_closing}</p>
        </div>
    </div>
</body>
</html>
        """
    
    def generate_report(self):
        """Generate complete AI-powered HTML report"""
        print("🤖 Generating AI-powered HTML report...")
        
        # Generate AI insights
        insights = self._generate_ai_insights()
        
        # Get chart images
        chart_paths = {
            'distribution': os.path.join(self.output_dir, '../monte_carlo_output/static_plots/01_distribution_analysis.png'),
            'risk': os.path.join(self.output_dir, '../monte_carlo_output/static_plots/02_risk_metrics.png'),
            'scenario': os.path.join(self.output_dir, '../monte_carlo_output/static_plots/03_scenario_comparison.png')
        }
        
        # Encode charts to base64
        charts_b64 = {}
        for name, path in chart_paths.items():
            charts_b64[name] = self._encode_image_to_base64(path) or ''
        
        # Prepare template variables
        baseline = self.results['baseline']['samples']
        risk_level = self._assess_risk_level(baseline)
        
        # Create scenario cards HTML
        scenario_cards_html = ""
        for scenario in insights['scenario_insights']['scenarios']:
            impact_color = 'var(--success-color)' if scenario['impact_percent'] < 5 else 'var(--warning-color)' if scenario['impact_percent'] < 15 else 'var(--danger-color)'
            scenario_cards_html += f"""
            <div class="card" style="border-left: 4px solid {impact_color};">
                <h4>{scenario['name'].replace('_', ' ').title()}</h4>
                <p style="font-size: 1.1rem; margin: 1rem 0;">{scenario['explanation']}</p>
                <div style="background: var(--bg-light); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <strong>Impact: {scenario['impact_percent']:+.1f}%</strong>
                </div>
                <p style="color: {impact_color}; font-weight: bold;">{scenario['recommendation']}</p>
            </div>
            """
        
        # Create recommendation cards HTML
        recommendation_cards_html = ""
        for rec in insights['recommendations']['actions']:
            recommendation_cards_html += f"""
            <div class="recommendation">
                <h4>{rec['title']}</h4>
                <p style="font-weight: bold; margin: 0.5rem 0;">{rec['action']}</p>
                <p style="font-size: 0.9rem; color: var(--text-light);">{rec['reason']}</p>
            </div>
            """
        
        # Create data explanation list HTML
        data_explanation_html = ""
        for explanation in insights['data_story']['explanation']:
            data_explanation_html += f"<li style='margin: 0.5rem 0; font-size: 1rem;'>{explanation}</li>"
        
        # Fill template
        html_content = self._get_html_template().format(
            timestamp=datetime.now().strftime("%d %B %Y, %H:%M"),
            executive_greeting=insights['executive_summary']['greeting'],
            executive_main_finding=insights['executive_summary']['main_finding'],
            executive_simple_explanation=insights['executive_summary']['simple_explanation'],
            executive_confidence=insights['executive_summary']['confidence_level'],
            mean_estimate=f"Rp {baseline['Total_Estimate'].mean():,.0f}",
            std_estimate=f"Rp {baseline['Total_Estimate'].std():,.0f}",
            risk_level_emoji=risk_level['emoji'],
            risk_level_class=risk_level['level'].lower(),
            risk_level_text=risk_level['description'],
            data_story=insights['data_story']['story'],
            data_explanation_list=data_explanation_html,
            distribution_chart=charts_b64['distribution'],
            risk_intro=insights['risk_explanation']['intro'],
            var_explanation=insights['risk_explanation']['var_explanation']['simple'] if isinstance(insights['risk_explanation']['var_explanation'], dict) else insights['risk_explanation']['var_explanation'],
            var_analogy=insights['risk_explanation']['var_explanation']['analogy'] if isinstance(insights['risk_explanation']['var_explanation'], dict) else "Seperti ramalan cuaca: 95% kemungkinan tidak hujan, tapi tetap bawa payung untuk 5% sisanya! ☂️",
            what_to_do=insights['risk_explanation']['what_to_do'],
            risk_chart=charts_b64['risk'],
            scenario_intro=insights['scenario_insights']['intro'],
            scenario_cards=scenario_cards_html,
            scenario_chart=charts_b64['scenario'],
            recommendations_intro=insights['recommendations']['intro'],
            recommendation_cards=recommendation_cards_html,
            recommendations_closing=insights['recommendations']['closing']
        )
        
        # Save HTML report
        output_path = os.path.join(self.output_dir, 'ai_powered_report.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ AI-powered report generated: {output_path}")
        return output_path

# Usage example
if __name__ == "__main__":
    # Load data dan run simulation
    CSV_PATH = r"D:\python_projects\learning\montecarlo\dataset\construction_estimates.csv"
    
    print("🔄 Loading data and running Monte Carlo simulation...")
    
    # Load and prepare data
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
    
    # Run simulations for all scenarios
    print("Running baseline scenario...")
    results = mc_sim.run_simulation(
        n_simulations=10000,
        scenarios=scenarios
    )
    
    # Generate visualizations (needed for charts)
    visualizer = MonteCarloVisualizer(results)
    visualizer.create_comprehensive_report()
    
    # Generate AI-powered report
    ai_report = AIReportGenerator(results, loader)
    report_path = ai_report.generate_report()
    
    print(f"\n🎉 AI-Powered Report completed!")
    print(f"📄 Open this file in your browser: {report_path}")