"""
Script untuk analisis kelengkapan nutrisi dan kategorisasi data
Author: Created for Tugas Akhir
Date: February 25, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def analyze_nutrient_completeness(csv_file, output_dir):
    """
    Analyze kelengkapan nutrisi per baris dan kategorisasi
    """
    print("=" * 80)
    print("ANALISIS KELENGKAPAN NUTRISI")
    print("=" * 80)
    
    # Load data
    print(f"\n1. Loading data dari: {csv_file}")
    print("   (File ~213MB, mohon tunggu...)")
    df = pd.read_csv(csv_file, low_memory=False)
    print(f"   ✓ Total baris: {len(df):,}")
    print(f"   ✓ Total kolom: {len(df.columns)}")
    
    # Identify nutrient columns (exclude ID, Name, Food Group)
    non_nutrient_cols = ['ID', 'Name', 'Food Group']
    nutrient_cols = [col for col in df.columns if col not in non_nutrient_cols]
    
    print(f"\n2. Identifikasi kolom nutrisi:")
    print(f"   ✓ Total kolom nutrisi: {len(nutrient_cols)}")
    print(f"   ✓ Kolom non-nutrisi: {non_nutrient_cols}")
    
    # Count non-null nutrients per row
    print(f"\n3. Menghitung kelengkapan nutrisi per baris...")
    df['nutrient_count'] = df[nutrient_cols].notna().sum(axis=1)
    df['nutrient_percentage'] = (df['nutrient_count'] / len(nutrient_cols)) * 100
    
    # Statistics
    print(f"\n{'='*80}")
    print(f"STATISTIK KELENGKAPAN:")
    print(f"{'='*80}")
    print(f"Total nutrisi: {len(nutrient_cols)}")
    print(f"Min nutrisi terisi: {df['nutrient_count'].min():.0f}")
    print(f"Max nutrisi terisi: {df['nutrient_count'].max():.0f}")
    print(f"Mean nutrisi terisi: {df['nutrient_count'].mean():.2f}")
    print(f"Median nutrisi terisi: {df['nutrient_count'].median():.0f}")
    print(f"Std Dev: {df['nutrient_count'].std():.2f}")
    
    # Distribution analysis
    print(f"\n{'='*80}")
    print(f"DISTRIBUSI KELENGKAPAN:")
    print(f"{'='*80}")
    
    # Show exact count distribution
    completeness_dist = df['nutrient_count'].value_counts().sort_index(ascending=False)
    print(f"\nBaris dengan nutrisi lengkap ({len(nutrient_cols)} nutrisi):")
    if len(nutrient_cols) in completeness_dist.index:
        print(f"   ✓ {completeness_dist[len(nutrient_cols)]:,} baris (100% lengkap)")
    else:
        print(f"   ✗ Tidak ada baris dengan 100% lengkap")
    
    # Top 10 most common completeness levels
    print(f"\nTop 10 level kelengkapan nutrisi:")
    for i, (count, freq) in enumerate(completeness_dist.head(10).items(), 1):
        pct = (count / len(nutrient_cols)) * 100
        print(f"   {i:2d}. {count:2d}/{len(nutrient_cols)} nutrisi ({pct:5.1f}%) - {freq:>8,} baris ({freq/len(df)*100:5.2f}%)")
    
    # Categorization using meaningful ranges
    print(f"\n{'='*80}")
    print(f"KATEGORISASI OTOMATIS:")
    print(f"{'='*80}")
    
    # Define categories based on completeness percentage
    def categorize_completeness(count, total):
        pct = (count / total) * 100
        if pct == 100:
            return "1. PERFECT (100%)"
        elif pct >= 90:
            return "2. EXCELLENT (90-99%)"
        elif pct >= 70:
            return "3. GOOD (70-89%)"
        elif pct >= 50:
            return "4. MODERATE (50-69%)"
        elif pct >= 30:
            return "5. LOW (30-49%)"
        else:
            return "6. VERY LOW (<30%)"
    
    df['completeness_category'] = df['nutrient_count'].apply(
        lambda x: categorize_completeness(x, len(nutrient_cols))
    )
    
    # Show categorization results
    category_stats = df.groupby('completeness_category').agg({
        'nutrient_count': ['count', 'mean', 'min', 'max'],
        'nutrient_percentage': 'mean'
    }).round(2)
    
    print(f"\nHasil Kategorisasi:")
    print(f"-" * 80)
    
    for category in sorted(df['completeness_category'].unique()):
        cat_df = df[df['completeness_category'] == category]
        count = len(cat_df)
        pct_of_total = count / len(df) * 100
        avg_nutrients = cat_df['nutrient_count'].mean()
        min_nutrients = cat_df['nutrient_count'].min()
        max_nutrients = cat_df['nutrient_count'].max()
        
        print(f"\n{category}")
        print(f"   Jumlah baris: {count:>10,} ({pct_of_total:5.2f}%)")
        print(f"   Range nutrisi: {min_nutrients:.0f} - {max_nutrients:.0f}")
        print(f"   Rata-rata: {avg_nutrients:.2f} nutrisi")
        
        # Show sample foods
        samples = cat_df['Name'].head(3).tolist()
        print(f"   Contoh makanan:")
        for i, food in enumerate(samples, 1):
            print(f"      {i}. {food}")
    
    # Additional analysis: Most complete and least complete foods
    print(f"\n{'='*80}")
    print(f"MAKANAN PALING LENGKAP NUTRISINYA:")
    print(f"{'='*80}")
    most_complete = df.nlargest(10, 'nutrient_count')[['Name', 'nutrient_count', 'nutrient_percentage']]
    for i, row in enumerate(most_complete.itertuples(), 1):
        print(f"{i:2d}. {row.Name[:60]:<60} - {row.nutrient_count:.0f}/{len(nutrient_cols)} ({row.nutrient_percentage:.1f}%)")
    
    print(f"\n{'='*80}")
    print(f"MAKANAN PALING TIDAK LENGKAP NUTRISINYA:")
    print(f"{'='*80}")
    least_complete = df.nsmallest(10, 'nutrient_count')[['Name', 'nutrient_count', 'nutrient_percentage']]
    for i, row in enumerate(least_complete.itertuples(), 1):
        print(f"{i:2d}. {row.Name[:60]:<60} - {row.nutrient_count:.0f}/{len(nutrient_cols)} ({row.nutrient_percentage:.1f}%)")
    
    # Save detailed report
    output_file = Path(output_dir) / "E. nutrient_completeness_report.txt"
    print(f"\n{'='*80}")
    print(f"Menyimpan laporan detail ke: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("LAPORAN KELENGKAPAN NUTRISI\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total data: {len(df):,} baris\n")
        f.write(f"Total nutrisi: {len(nutrient_cols)} kolom\n\n")
        
        f.write("KATEGORI KELENGKAPAN:\n")
        f.write("-"*80 + "\n")
        for category in sorted(df['completeness_category'].unique()):
            cat_df = df[df['completeness_category'] == category]
            count = len(cat_df)
            pct = count / len(df) * 100
            f.write(f"\n{category}\n")
            f.write(f"  Jumlah: {count:,} baris ({pct:.2f}%)\n")
            f.write(f"  Range: {cat_df['nutrient_count'].min():.0f} - {cat_df['nutrient_count'].max():.0f} nutrisi\n")
            f.write(f"  Rata-rata: {cat_df['nutrient_count'].mean():.2f} nutrisi\n")
        
        f.write("\n\n" + "="*80 + "\n")
        f.write("DISTRIBUSI LENGKAP PER JUMLAH NUTRISI:\n")
        f.write("="*80 + "\n")
        for count, freq in completeness_dist.items():
            pct = (count / len(nutrient_cols)) * 100
            f.write(f"{count:2d} nutrisi ({pct:5.1f}%): {freq:>10,} baris\n")
    
    print(f"   ✓ Laporan tersimpan!")
    
    # Save categorized data (optional - might be large)
    # output_csv = Path(output_dir) / "5th_categorized_nutriensFood.csv"
    # print(f"\nMenyimpan data dengan kategori ke: {output_csv}")
    # df.to_csv(output_csv, index=False)
    # print(f"   ✓ Data tersimpan!")
    
    # Create summary CSV
    summary_csv = Path(output_dir) / "E. nutrient_completeness_summary.csv"
    summary_df = df.groupby('completeness_category').agg({
        'nutrient_count': ['count', 'mean', 'min', 'max'],
        'nutrient_percentage': 'mean'
    }).round(2)
    summary_df.columns = ['Total_Rows', 'Avg_Nutrients', 'Min_Nutrients', 'Max_Nutrients', 'Avg_Percentage']
    summary_df.to_csv(summary_csv)
    print(f"\nSummary data tersimpan di: {summary_csv}")
    
    print(f"\n{'='*80}")
    print("✅ ANALISIS SELESAI!")
    print(f"{'='*80}")
    
    return df

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    data_processed = base_dir / "data" / "processed"
    
    csv_file = data_processed / "4th_nutriensFood.csv"
    
    if not csv_file.exists():
        print(f"❌ Error: File tidak ditemukan: {csv_file}")
        exit(1)
    
    df = analyze_nutrient_completeness(str(csv_file), str(data_processed))
