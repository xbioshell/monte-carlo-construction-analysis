import pandas as pd
import numpy as np
import base64
import os
from datetime import datetime
import json
from data_loader import DataLoader
from monte_carlo_simulation import PricingMonteCarloSimulation
from visualization_suite import MonteCarloVisualizer

class AIReportGenerator:
    """
    AI-Powered HTML Report Generator untuk Monte Carlo Analysis
    Menghasilkan laporan yang eye-catching dan mudah dipahami untuk orang awam
    """
    
    def __init__(self, simulation_results, data_loader, output_dir="./ai_report_output"):
        self.results = simulation_results
        self.data_loader = data_loader
        self.output_dir = output_dir
        self.report_data = {}
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
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
        """Explain risk metrics dengan bahasa sederhana"""
        baseline = self.results['baseline']['samples']
        var_95 = np.percentile(baseline['Total_Estimate'], 95)
        var_99 = np.percentile(baseline['Total_Estimate'], 99)
        
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
        """Create actionable recommendations"""
        baseline = self.results['baseline']['samples']
        risk_level = self._assess_risk_level(baseline)
        
        recommendations = [
            {
                'title': '💰 Budget Planning',
                'action': f"Siapkan budget dasar Rp {baseline['Total_Estimate'].mean():,.0f} + contingency 15%",
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
        """Generate modern HTML template dengan eye-catching design"""
        return """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 AI-Powered Monte Carlo Analysis Report</title>
    <style>
        /* Modern CSS dengan eye-catching design */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --accent-color: #ff6b6b;
            --success-color: #51cf66;
            --warning-color: #ffd43b;
            --danger-color: #ff8787;
            --text-dark: #2c3e50;
            --text-light: #7f8c8d;
            --bg-light: #f8f9fa;
            --shadow: 0 10px 30px rgba(0,0,0,0.1);
            --shadow-hover: 0 20px 40px rgba(0,0,0,0.15);
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        
        /* Hero Section */
        .hero {{
            background: var(--primary-gradient);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            animation: float 20s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-20px); }}
        }}
        
        .hero h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            animation: slideInDown 1s ease-out;
        }}
        
        .hero p {{
            font-size: 1.2rem;
            opacity: 0.9;
            animation: slideInUp 1s ease-out 0.3s both;
        }}
        
        @keyframes slideInDown {{
            from {{ transform: translateY(-50px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        @keyframes slideInUp {{
            from {{ transform: translateY(50px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        /* Cards */
        .card {{
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--primary-gradient);
        }
        
        .card:hover {
            transform: translateY(-10px);
            box-shadow: var(--shadow-hover);
        }
        
        /* AI Assistant Styling */
        .ai-section {
            background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
            border-left: 4px solid var(--accent-color);
            position: relative;
        }
        
        .ai-avatar {
            width: 60px;
            height: 60px;
            background: var(--primary-gradient);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        
        /* Metrics Cards */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            border-top: 4px solid var(--accent-color);
        }
        
        .metric-card:hover {
            transform: scale(1.05);
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: var(--accent-color);
            margin: 0.5rem 0;
        }
        
        .metric-label {
            color: var(--text-light);
            font-size: 0.9rem;
        }
        
        /* Risk Level Styling */
        .risk-indicator {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-weight: bold;
            margin: 1rem 0;
        }
        
        .risk-low { background: var(--success-color); color: white; }
        .risk-medium { background: var(--warning-color); color: var(--text-dark); }
        .risk-high { background: var(--danger-color); color: white; }
        
        /* Charts */
        .chart-container {
            text-align: center;
            margin: 2rem 0;
            padding: 1rem;
            background: var(--bg-light);
            border-radius: 15px;
        }
        
        .chart-container img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: var(--shadow);
        }
        
        /* Recommendations */
        .recommendation {
            background: linear-gradient(135deg, #51cf6620 0%, #51cf6610 100%);
            border-left: 4px solid var(--success-color);
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 10px;
        }
        
        .recommendation h4 {
            color: var(--success-color);
            margin-bottom: 0.5rem;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2rem; }
            .container { padding: 1rem; }
            .metrics-grid { grid-template-columns: 1fr; }
        }
        
        /* Floating Navigation */
        .floating-nav {
            position: fixed;
            top: 50%;
            right: 2rem;
            transform: translateY(-50%);
            background: white;
            border-radius: 25px;
            padding: 1rem;
            box-shadow: var(--shadow);
            z-index: 1000;
        }
        
        .nav-item {
            display: block;
            padding: 0.5rem;
            margin: 0.5rem 0;
            text-decoration: none;
            color: var(--text-dark);
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        
        .nav-item:hover {
            background: var(--primary-gradient);
            color: white;
        }
        
        /* Animations */
        .fade-in {
            animation: fadeIn 1s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Print Styles */
        @media print {
            .floating-nav { display: none; }
            .card { break-inside: avoid; }
        }
    </style>
</head>
<body>
    <!-- Floating Navigation -->
    <nav class="floating-nav">
        <a href="#executive" class="nav-item">📊 Summary</a>
        <a href="#data" class="nav-item">📈 Data</a>
        <a href="#risk" class="nav-item">⚠️ Risk</a>
        <a href="#scenarios" class="nav-item">🔍 Scenarios</a>
        <a href="#recommendations" class="nav-item">💡 Actions</a>
    </nav>
    
    <!-- Hero Section -->
    <header class="hero">
        <h1>🎯 AI-Powered Monte Carlo Analysis</h1>
        <p>Laporan Analisis Risiko Proyek Konstruksi yang Mudah Dipahami</p>
        <p><small>Generated on {timestamp}</small></p>
    </header>
    
    <div class="container">
        <!-- Executive Summary -->
        <section id="executive" class="card ai-section fade-in">
            <div class="ai-avatar">🤖</div>
            <h2>📊 Executive Summary</h2>
            <p style="font-size: 1.1rem; margin: 1rem 0;">{executive_greeting}</p>
            <p style="font-size: 1.2rem; font-weight: bold; margin: 1rem 0;">{executive_main_finding}</p>
            <p style="font-style: italic; color: var(--text-light);">{executive_simple_explanation}</p>
            <p style="margin-top: 1rem;">{executive_confidence}</p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{mean_estimate}</div>
                    <div class="metric-label">Estimasi Rata-rata</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{std_estimate}</div>
                    <div class="metric-label">Variasi (±)</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{risk_level_emoji}</div>
                    <div class="metric-label">Tingkat Risiko</div>
                </div>
            </div>
        </section>
        
        <!-- Data Story -->
        <section id="data" class="card fade-in">
            <h2>📈 Cerita Data Kita</h2>
            <div class="ai-section" style="margin: 1rem 0; padding: 1.5rem;">
                <div class="ai-avatar">📊</div>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">{data_story}</p>
                <ul style="list-style: none; padding: 0;">
                    {data_explanation_list}
                </ul>
            </div>
            
            <div class="chart-container">
                <h3>Distribusi Data Historis</h3>
                <img src="data:image/png;base64,{distribution_chart}" alt="Distribution Analysis">
                <p style="margin-top: 1rem; font-style: italic;">Grafik ini menunjukkan pola distribusi biaya dari 1,000 proyek historis</p>
            </div>
        </section>
        
        <!-- Risk Analysis -->
        <section id="risk" class="card ai-section fade-in">
            <div class="ai-avatar">⚠️</div>
            <h2>⚠️ Analisis Risiko</h2>
            <p style="font-size: 1.1rem; margin: 1rem 0;">{risk_intro}</p>
            
            <div class="risk-indicator risk-{risk_level_class}">
                {risk_level_emoji} Tingkat Risiko: {risk_level_text}
            </div>
            
            <div style="background: var(--bg-light); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h4>🎯 Penjelasan VaR (Value at Risk)</h4>
                <p>{var_explanation}</p>
                <p style="font-style: italic; color: var(--text-light); margin-top: 0.5rem;">{var_analogy}</p>
            </div>
            
            <div class="chart-container">
                <h3>Visualisasi Risiko</h3>
                <img src="data:image/png;base64,{risk_chart}" alt="Risk Analysis">
            </div>
            
            <div style="background: linear-gradient(135deg, #ffd43b20 0%, #ffd43b10 100%); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <p style="font-weight: bold;">💡 {what_to_do}</p>
            </div>
        </section>
        
        <!-- Scenario Analysis -->
        <section id="scenarios" class="card fade-in">
            <h2>🔍 Analisis Skenario</h2>
            <div class="ai-section" style="margin: 1rem 0; padding: 1.5rem;">
                <div class="ai-avatar">🔮</div>
                <p style="font-size: 1.1rem;">{scenario_intro}</p>
            </div>
            
            {scenario_cards}
            
            <div class="chart-container">
                <h3>Perbandingan Skenario</h3>
                <img src="data:image/png;base64,{scenario_chart}" alt="Scenario Comparison">
            </div>
        </section>
        
        <!-- Recommendations -->
        <section id="recommendations" class="card ai-section fade-in">
            <div class="ai-avatar">💡</div>
            <h2>💡 Rekomendasi AI</h2>
            <p style="font-size: 1.1rem; margin: 1rem 0;">{recommendations_intro}</p>
            
            {recommendation_cards}
            
            <div style="text-align: center; margin: 2rem 0; padding: 1.5rem; background: linear-gradient(135deg, #51cf6620 0%, #51cf6610 100%); border-radius: 15px;">
                <h3 style="color: var(--success-color);">🚀 {recommendations_closing}</h3>
            </div>
        </section>
        
        <!-- Footer -->
        <footer style="text-align: center; padding: 2rem; color: var(--text-light);">
            <p>📊 Generated by AI-Powered Monte Carlo Analysis System</p>
            <p><small>Report created on {timestamp}</small></p>
        </footer>
    </div>
    
    <script>
        // Smooth scrolling untuk navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                target.scrollIntoView({ behavior: 'smooth' });
            });
        });
        
        // Animate numbers on scroll
        function animateNumbers() {
            const numbers = document.querySelectorAll('.metric-value');
            numbers.forEach(num => {
                const finalValue = num.textContent;
                num.textContent = '0';
                
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            animateValue(num, 0, parseFloat(finalValue.replace(/[^\d.-]/g, '')), 2000);
                            observer.unobserve(entry.target);
                        }
                    });
                });
                
                observer.observe(num);
            });
        }
        
        function animateValue(element, start, end, duration) {
            const startTime = performance.now();
            const originalText = element.textContent;
            
            function update(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const current = start + (end - start) * progress;
                
                if (originalText.includes('Rp')) {
                    element.textContent = `Rp ${Math.floor(current).toLocaleString()}`;
                } else {
                    element.textContent = Math.floor(current).toLocaleString();
                }
                
                if (progress < 1) {
                    requestAnimationFrame(update);
                }
            }
            
            requestAnimationFrame(update);
        }
        
        // Initialize animations
        document.addEventListener('DOMContentLoaded', animateNumbers);
    </script>
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
            var_explanation=insights['risk_explanation']['var_explanation']['simple'],
            var_analogy=insights['risk_explanation']['var_explanation']['analogy'],
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