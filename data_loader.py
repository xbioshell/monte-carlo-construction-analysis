import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class DataLoader:
    def __init__(self, csv_path):
        """
        Initialize DataLoader dengan path ke CSV file
        """
        self.csv_path = csv_path
        self.data = None
        self.original_columns = None
        
    def load_data(self):
        """
        Load data dari CSV file
        """
        try:
            self.data = pd.read_csv(self.csv_path)
            self.original_columns = self.data.columns.tolist()
            print(f"✅ Data berhasil dimuat: {len(self.data)} baris, {len(self.data.columns)} kolom")
            print(f"📊 Kolom yang tersedia: {list(self.data.columns)}")
            return True
        except FileNotFoundError:
            print(f"❌ File tidak ditemukan: {self.csv_path}")
            return False
        except Exception as e:
            print(f"❌ Error saat memuat data: {str(e)}")
            return False
    
    def explore_data(self):
        """
        Eksplorasi awal dataset
        """
        if self.data is None:
            print("❌ Data belum dimuat. Jalankan load_data() terlebih dahulu.")
            return
        
        print("\n" + "="*60)
        print("📈 EKSPLORASI DATASET CONSTRUCTION ESTIMATES")
        print("="*60)
        
        # Basic info
        print(f"\n📋 Informasi Dasar:")
        print(f"├── Jumlah baris: {len(self.data):,}")
        print(f"├── Jumlah kolom: {len(self.data.columns)}")
        print(f"├── Memory usage: {self.data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"└── Missing values: {self.data.isnull().sum().sum()}")
        
        # Column info
        print(f"\n📊 Informasi Kolom:")
        for i, col in enumerate(self.data.columns):
            dtype = self.data[col].dtype
            null_count = self.data[col].isnull().sum()
            unique_count = self.data[col].nunique()
            print(f"├── {col}: {dtype} (Null: {null_count}, Unique: {unique_count})")
        
        # Statistical summary
        print(f"\n📈 Statistik Deskriptif:")
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(self.data[numeric_cols].describe())
        
        # Data types
        print(f"\n🔍 Tipe Data:")
        print(self.data.dtypes)
        
        return self.data.head()
    
    def clean_data(self):
        """
        Pembersihan data dasar
        """
        if self.data is None:
            print("❌ Data belum dimuat.")
            return
        
        print("\n🧹 Membersihkan data...")
        
        # Remove duplicates
        initial_rows = len(self.data)
        self.data = self.data.drop_duplicates()
        removed_duplicates = initial_rows - len(self.data)
        if removed_duplicates > 0:
            print(f"├── Menghapus {removed_duplicates} baris duplikat")
        
        # Handle missing values
        missing_summary = self.data.isnull().sum()
        if missing_summary.sum() > 0:
            print(f"├── Missing values ditemukan:")
            for col, missing_count in missing_summary[missing_summary > 0].items():
                print(f"    └── {col}: {missing_count} ({missing_count/len(self.data)*100:.1f}%)")
        
        # Basic data validation
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col.lower() in ['cost', 'price', 'estimate', 'total']:
                negative_count = (self.data[col] < 0).sum()
                if negative_count > 0:
                    print(f"├── ⚠️  {col} memiliki {negative_count} nilai negatif")
        
        print(f"└── ✅ Data cleaning selesai. Final shape: {self.data.shape}")
    
    def analyze_distributions(self):
        """
        Analisis distribusi untuk kolom numerik
        """
        if self.data is None:
            print("❌ Data belum dimuat.")
            return
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ Tidak ada kolom numerik untuk dianalisis.")
            return
        
        print("\n📊 Analisis Distribusi:")
        print("="*50)
        
        # Create subplots
        n_cols = min(3, len(numeric_cols))
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes
        else:
            axes = axes.flatten()
        
        distribution_results = {}
        
        for i, col in enumerate(numeric_cols):
            if i >= len(axes):
                break
                
            ax = axes[i]
            data_col = self.data[col].dropna()
            
            # Histogram
            ax.hist(data_col, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')
            
            # Fit normal distribution
            try:
                mu, sigma = stats.norm.fit(data_col)
                x = np.linspace(data_col.min(), data_col.max(), 100)
                ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2, 
                       label=f'Normal(μ={mu:.0f}, σ={sigma:.0f})')
                
                # Kolmogorov-Smirnov test
                ks_stat, ks_pvalue = stats.kstest(data_col, lambda x: stats.norm.cdf(x, mu, sigma))
                
                distribution_results[col] = {
                    'mean': mu,
                    'std': sigma,
                    'ks_statistic': ks_stat,
                    'ks_pvalue': ks_pvalue,
                    'is_normal': ks_pvalue > 0.05
                }
                
            except Exception as e:
                print(f"⚠️  Error fitting distribution untuk {col}: {str(e)}")
                distribution_results[col] = {'error': str(e)}
            
            ax.set_title(f'Distribusi {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Density')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        # Hide empty subplots
        for i in range(len(numeric_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('d:\\python_projects\\learning\\montecarlo\\distribution_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        # Print distribution analysis results
        print("\n📈 Hasil Analisis Distribusi:")
        for col, results in distribution_results.items():
            if 'error' not in results:
                normality = "✅ Normal" if results['is_normal'] else "❌ Non-normal"
                print(f"├── {col}:")
                print(f"    ├── Mean: {results['mean']:.2f}")
                print(f"    ├── Std: {results['std']:.2f}")
                print(f"    ├── KS p-value: {results['ks_pvalue']:.4f}")
                print(f"    └── Normalitas: {normality}")
        
        return distribution_results
    
    def correlation_analysis(self):
        """
        Analisis korelasi antar variabel
        """
        if self.data is None:
            print("❌ Data belum dimuat.")
            return
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("❌ Perlu minimal 2 kolom numerik untuk analisis korelasi.")
            return
        
        # Calculate correlation matrix
        correlation_matrix = self.data[numeric_cols].corr()
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdYlBu_r', 
                   center=0, square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        plt.title('Correlation Matrix - Construction Estimates Dataset')
        plt.tight_layout()
        plt.savefig('d:\\python_projects\\learning\\montecarlo\\correlation_matrix.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        # Print strong correlations
        print("\n🔗 Korelasi Kuat (|r| > 0.5):")
        strong_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_val = correlation_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    col1 = correlation_matrix.columns[i]
                    col2 = correlation_matrix.columns[j]
                    strong_correlations.append((col1, col2, corr_val))
                    print(f"├── {col1} ↔ {col2}: {corr_val:.3f}")
        
        if not strong_correlations:
            print("├── Tidak ada korelasi kuat yang ditemukan.")
        
        return correlation_matrix
    
    def get_sample_data(self, n_samples=None):
        """
        Ambil sample data untuk testing
        """
        if self.data is None:
            print("❌ Data belum dimuat.")
            return None
        
        if n_samples is None:
            return self.data.copy()
        else:
            return self.data.sample(n=min(n_samples, len(self.data))).copy()

# Usage example
if __name__ == "__main__":
    # Initialize data loader
    csv_path = r"D:\python_projects\learning\montecarlo\dataset\construction_estimates.csv"
    loader = DataLoader(csv_path)
    
    # Load and explore data
    if loader.load_data():
        print("\n" + "="*60)
        print("🔍 SAMPLE DATA (5 baris pertama):")
        print("="*60)
        sample = loader.explore_data()
        print(sample)
        
        # Clean data
        loader.clean_data()
        
        # Analyze distributions
        dist_results = loader.analyze_distributions()
        
        # Correlation analysis
        corr_matrix = loader.correlation_analysis()
        
        print("\n✅ Analisis data selesai!")
        print("📁 File yang dihasilkan:")
        print("├── distribution_analysis.png")
        print("└── correlation_matrix.png")
    else:
        print("❌ Gagal memuat data. Periksa path file.")