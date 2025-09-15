# 🎯 Monte Carlo Simulation for Construction Pricing Analysis

Sebuah implementasi komprehensif simulasi Monte Carlo untuk analisis pricing konstruksi menggunakan Python. Proyek ini menyediakan tools lengkap untuk analisis risiko, visualisasi, dan dashboard interaktif dengan dukungan AI-powered insights menggunakan Google Gemini AI.

## 📊 Fitur Utama

### 🔍 Data Analysis
- **Automatic Data Loading**: Memuat dan membersihkan dataset construction estimates
- **Distribution Fitting**: Otomatis fit berbagai distribusi statistik (Normal, Log-normal, Gamma, Uniform)
- **Correlation Analysis**: Analisis korelasi antar variabel dengan visualisasi heatmap
- **Statistical Summary**: Ringkasan statistik deskriptif lengkap

### 🎲 Monte Carlo Simulation
- **Multi-Scenario Analysis**: Simulasi berbagai skenario (baseline, kenaikan material, kenaikan labor, kombinasi)
- **Risk Metrics**: Perhitungan VaR (Value at Risk), CVaR, Expected Shortfall
- **Sensitivity Analysis**: Analisis sensitivitas perubahan parameter terhadap hasil
- **Configurable Parameters**: Jumlah simulasi dan skenario dapat disesuaikan

### 📈 Visualizations
- **Static Plots**: Comprehensive visualization suite dengan matplotlib dan seaborn
- **Interactive Dashboards**: Dashboard interaktif menggunakan Plotly
- **Risk Analysis Charts**: Visualisasi khusus untuk analisis risiko
- **Scenario Comparison**: Perbandingan visual antar skenario

### 🎛️ Interactive Features
- **HTML Dashboards**: Dashboard yang dapat dibuka di browser
- **Real-time Filtering**: Filter dan selection interaktif
- **Drill-down Capabilities**: Kemampuan untuk melihat detail data
- **Export Options**: Export hasil ke berbagai format

### 🤖 AI-Powered Features
- **Intelligent Reports**: Laporan analisis otomatis menggunakan Gemini AI
- **Smart Insights**: Interpretasi hasil simulasi dengan AI
- **Risk Recommendations**: Rekomendasi mitigasi risiko berbasis AI
- **Automated Analysis**: Analisis mendalam otomatis dari hasil simulasi

## 🚀 Quick Start

### Prerequisites

1. **Install Dependencies**
```bash
pip install pandas numpy matplotlib seaborn scipy plotly google-generativeai python-dotenv
```

2. **Setup API Keys**
   - Copy `.env.example` to `.env`
   - Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add your API key to the `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### Quick Start - AI-Powered Analysis
```bash
python ai_report_generator.py
```

### Basic Usage
```python
# Jalankan seluruh pipeline
python main_monte_carlo.py
```

### Custom Analysis
```python
from data_loader import DataLoader
from monte_carlo_simulation import PricingMonteCarloSimulation
from visualization_suite import MonteCarloVisualizer
from interactive_dashboard import InteractiveDashboard

# Load data
loader = DataLoader("path/to/your/data.csv")
loader.load_data()
loader.clean_data()

# Run simulation
mc_sim = PricingMonteCarloSimulation(loader.data)
mc_sim.fit_distributions()
results = mc_sim.run_simulation(n_simulations=10000)

# Create visualizations
visualizer = MonteCarloVisualizer(results)
visualizer.create_comprehensive_report()

# Create interactive dashboard
dashboard = InteractiveDashboard(results)
dashboard.create_comprehensive_dashboard()
```

## 📁 Struktur Proyek

```
montecarlo/
├── data_loader.py              # Data loading dan preprocessing
├── monte_carlo_simulation.py   # Core Monte Carlo simulation
├── visualization_suite.py      # Static visualizations
├── interactive_dashboard.py    # Interactive dashboards
├── ai_report_generator.py      # AI-powered report generation
├── main_monte_carlo.py        # Script utama
├── README.md                  # Dokumentasi ini
├── .env.example               # Template environment variables
├── .env                       # Your API keys (DO NOT COMMIT)
├── monte_carlo_output/        # Output folder
│   ├── static_plots/          # Static visualization files
│   ├── interactive_dashboards/ # HTML dashboard files
│   └── summary_report.txt     # Text summary report
└── ai_report_output/          # AI-powered HTML reports
```

## 📊 Dataset Requirements

Dataset harus memiliki kolom berikut:
- `Material_Cost`: Biaya material (numeric)
- `Labor_Cost`: Biaya tenaga kerja (numeric)
- `Profit_Rate`: Tingkat keuntungan dalam persen (numeric)
- `Discount_or_Markup`: Diskon atau markup (numeric)
- `Total_Estimate`: Total estimasi biaya (numeric)
- `Policy_Reason`: Alasan kebijakan (categorical, optional)

## 🎯 Skenario Analisis

Proyek ini menganalisis beberapa skenario:

1. **Baseline**: Kondisi normal tanpa perubahan
2. **Material Increase**: Kenaikan biaya material 10% dan 20%
3. **Labor Increase**: Kenaikan biaya tenaga kerja 15% dan 25%
4. **Combined Scenarios**: Kombinasi kenaikan material dan labor
5. **Cost Reduction**: Skenario pengurangan biaya

## 📈 Output yang Dihasilkan

### Static Visualizations
- `01_distribution_analysis.png`: Analisis distribusi variabel
- `02_risk_metrics.png`: Perbandingan metrik risiko
- `03_scenario_comparison.png`: Perbandingan skenario
- `04_correlation_heatmap.png`: Heatmap korelasi
- `05_sensitivity_analysis.png`: Analisis sensitivitas

### Interactive Dashboards
- `01_distribution_dashboard.html`: Dashboard distribusi interaktif
- `02_risk_dashboard.html`: Dashboard analisis risiko
- `03_sensitivity_dashboard.html`: Dashboard analisis sensitivitas

### AI-Powered Reports
- `ai_monte_carlo_report.html`: Laporan komprehensif dengan AI insights
- `ai_analysis_summary.txt`: Ringkasan analisis AI dalam format teks

### Reports
- `summary_report.txt`: Laporan ringkasan dalam format teks

## 🔧 Konfigurasi

### Mengubah Jumlah Simulasi
```python
# Dalam main_monte_carlo.py
N_SIMULATIONS = 10000  # Ubah sesuai kebutuhan
```

### Menambah Skenario Baru
```python
# Dalam main_monte_carlo.py
scenarios = {
    'baseline': {},
    'custom_scenario': {
        'Material_Cost': 1.15,  # 15% increase
        'Labor_Cost': 0.9       # 10% decrease
    }
}
```

### Mengubah Distribusi yang Ditest
```python
# Dalam monte_carlo_simulation.py
distributions = mc_sim.fit_distributions(['norm', 'lognorm', 'gamma', 'beta', 'uniform'])
```

## 📊 Metrik Risiko

### Value at Risk (VaR)
- **VaR 95%**: Kerugian maksimum dengan confidence level 95%
- **VaR 99%**: Kerugian maksimum dengan confidence level 99%

### Conditional Value at Risk (CVaR)
- **CVaR 95%**: Expected shortfall beyond VaR 95%

### Additional Metrics
- **Probability of Loss**: Probabilitas mengalami kerugian
- **Expected Shortfall**: Rata-rata kerugian dalam worst-case scenarios

## 🎨 Customization

### Mengubah Color Scheme
```python
# Dalam visualization_suite.py
sns.set_palette("husl")  # Ubah ke palette lain
```

### Mengubah Figure Size
```python
# Dalam visualization_suite.py
visualizer = MonteCarloVisualizer(results, figsize=(20, 12))
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Error**: Pastikan semua dependencies terinstall
   ```bash
   pip install -r requirements.txt
   ```

2. **File Path Error**: Gunakan absolute path untuk dataset
   ```python
   CSV_PATH = r"C:\full\path\to\your\data.csv"
   ```

3. **Memory Issues**: Kurangi jumlah simulasi untuk dataset besar
   ```python
   N_SIMULATIONS = 5000  # Reduce from 10000
   ```

4. **Visualization Issues**: Pastikan display backend tersedia
   ```python
   import matplotlib
   matplotlib.use('Agg')  # For headless environments
   ```

## 🔐 Security Notes

⚠️ **Important**: Never commit your `.env` file or expose your API keys!

- The `.env` file is already added to `.gitignore`
- Use `.env.example` as a template for other users
- Keep your API keys secure and rotate them regularly
- Never share your API keys in code, documentation, or version control

## 📚 Dependencies

- **pandas**: Data manipulation dan analysis
- **numpy**: Numerical computing
- **matplotlib**: Static plotting
- **seaborn**: Statistical visualization
- **scipy**: Scientific computing dan statistical distributions
- **plotly**: Interactive visualizations
- **google-generativeai**: Google Gemini AI integration
- **python-dotenv**: Environment variables management
- **warnings**: Suppress warnings untuk output yang bersih

## 🎯 Use Cases

### Construction Industry
- **Project Cost Estimation**: Estimasi biaya proyek dengan uncertainty
- **Risk Assessment**: Penilaian risiko cost overrun
- **Budget Planning**: Perencanaan budget dengan contingency
- **Scenario Planning**: Analisis berbagai skenario market conditions

### Financial Analysis
- **Investment Analysis**: Analisis investasi proyek konstruksi
- **Portfolio Risk**: Manajemen risiko portfolio proyek
- **Insurance Pricing**: Pricing asuransi konstruksi

### Academic Research
- **Monte Carlo Methods**: Pembelajaran metode Monte Carlo
- **Risk Management**: Studi kasus manajemen risiko
- **Statistical Modeling**: Pemodelan statistik untuk construction data

## 🔮 Future Enhancements

- [ ] **Advanced AI Models**: Integration dengan model AI lainnya (Claude, GPT-4)
- [ ] **Machine Learning Integration**: Prediksi cost menggunakan ML models
- [ ] **Real-time Data Integration**: Koneksi ke real-time market data
- [ ] **Web Application**: Deploy sebagai web app dengan Flask/Django
- [ ] **Database Integration**: Koneksi ke database untuk data storage
- [ ] **API Development**: REST API untuk integration dengan sistem lain
- [ ] **Advanced Risk Models**: Implementasi model risiko yang lebih sophisticated
- [ ] **Multi-language AI Reports**: Laporan AI dalam berbagai bahasa

## 📄 License

MIT License - Feel free to use and modify for your projects.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

**When contributing:**
1. Never commit API keys or sensitive data
2. Update `.env.example` if you add new environment variables
3. Test that the project works with environment variables from `.env.example`
4. Follow security best practices for API key management

## 📞 Support

Jika ada pertanyaan atau issues, silakan buat issue di repository ini.

---

**Happy Analyzing! 🎉**

*Dibuat dengan ❤️ menggunakan Python dan Monte Carlo methods*