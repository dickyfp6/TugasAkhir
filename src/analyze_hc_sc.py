"""
Script untuk analisis Hard Constraint vs Soft Constraint
Author: Created for Tugas Akhir
Date: February 25, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path

def analyze_hard_soft_constraints(csv_file, output_dir):
    """
    Analyze kelengkapan Hard Constraint vs Soft Constraint
    """
    print("=" * 90)
    print("ANALISIS HARD CONSTRAINT VS SOFT CONSTRAINT")
    print("=" * 90)
    
    # Define Hard Constraints (19 nutrisi)
    hard_constraints = [
        'Water (g)',
        'Calories',
        'Sugars (g)',
        'Potassium, K (mg)',
        'Calcium (mg)',
        'Carbohydrate (g)',
        'Cholesterol (mg)',
        'Saturated Fats (g)',
        'Fat (g)',
        'Magnesium (mg)',
        'Sodium (mg)',
        'Protein (g)',
        'Zinc, Zn (mg)',
        'Fiber (g)',
        'Vitamin A, RAE (mcg)',
        'Vitamin B-12 (mcg)',
        'Vitamin B6 (mg)',
        'Vitamin C (mg)',
        'Iron, Fe (mg)'
    ]
    
    # Load data
    print(f"\n1. Loading data dari: {csv_file}")
    print("   (File ~213MB, mohon tunggu...)")
    df = pd.read_csv(csv_file, low_memory=False)
    print(f"   ✓ Total baris: {len(df):,}")
    print(f"   ✓ Total kolom: {len(df.columns)}")
    
    # Identify columns
    non_nutrient_cols = ['ID', 'Name', 'Food Group']
    all_nutrient_cols = [col for col in df.columns if col not in non_nutrient_cols]
    
    # Soft Constraints = All Nutrients - Hard Constraints
    soft_constraints = [col for col in all_nutrient_cols if col not in hard_constraints]
    
    print(f"\n2. Identifikasi constraint:")
    print(f"   ✓ Hard Constraints (HC): {len(hard_constraints)} nutrisi")
    print(f"   ✓ Soft Constraints (SC): {len(soft_constraints)} nutrisi")
    print(f"   ✓ Total: {len(all_nutrient_cols)} nutrisi")
    
    print(f"\n   Hard Constraints:")
    for i, col in enumerate(hard_constraints, 1):
        print(f"      {i:2d}. {col}")
    
    print(f"\n   Soft Constraints:")
    for i, col in enumerate(soft_constraints, 1):
        print(f"      {i:2d}. {col}")
    
    # Count completeness for HC and SC
    print(f"\n3. Menghitung kelengkapan HC dan SC per baris...")
    df['HC_count'] = df[hard_constraints].notna().sum(axis=1)
    df['SC_count'] = df[soft_constraints].notna().sum(axis=1)
    df['Total_count'] = df['HC_count'] + df['SC_count']
    
    df['HC_percentage'] = (df['HC_count'] / len(hard_constraints)) * 100
    df['SC_percentage'] = (df['SC_count'] / len(soft_constraints)) * 100
    
    # Statistics
    print(f"\n{'='*90}")
    print(f"STATISTIK KELENGKAPAN:")
    print(f"{'='*90}")
    print(f"\nHard Constraints (HC):")
    print(f"   Min HC: {df['HC_count'].min():.0f}/{len(hard_constraints)}")
    print(f"   Max HC: {df['HC_count'].max():.0f}/{len(hard_constraints)}")
    print(f"   Mean HC: {df['HC_count'].mean():.2f}/{len(hard_constraints)} ({df['HC_percentage'].mean():.1f}%)")
    print(f"   Median HC: {df['HC_count'].median():.0f}/{len(hard_constraints)}")
    print(f"   Std Dev: {df['HC_count'].std():.2f}")
    
    print(f"\nSoft Constraints (SC):")
    print(f"   Min SC: {df['SC_count'].min():.0f}/{len(soft_constraints)}")
    print(f"   Max SC: {df['SC_count'].max():.0f}/{len(soft_constraints)}")
    print(f"   Mean SC: {df['SC_count'].mean():.2f}/{len(soft_constraints)} ({df['SC_percentage'].mean():.1f}%)")
    print(f"   Median SC: {df['SC_count'].median():.0f}/{len(soft_constraints)}")
    print(f"   Std Dev: {df['SC_count'].std():.2f}")
    
    # Check for perfect HC
    perfect_hc = (df['HC_count'] == len(hard_constraints)).sum()
    print(f"\n   🎯 Data dengan HC LENGKAP (19/19): {perfect_hc:,} baris ({perfect_hc/len(df)*100:.2f}%)")
    
    # Sort data: Primary by HC (desc), Secondary by SC (desc)
    print(f"\n4. Sorting data berdasarkan HC (desc) dan SC (desc)...")
    df_sorted = df.sort_values(by=['HC_count', 'SC_count'], ascending=[False, False])
    print(f"   ✓ Data sorted!")
    
    # Create summary table: HC, SC, Total rows
    print(f"\n{'='*90}")
    print(f"TABEL SUMMARY HC vs SC:")
    print(f"{'='*90}")
    
    summary = df_sorted.groupby(['HC_count', 'SC_count']).size().reset_index(name='Total_Rows')
    summary = summary.sort_values(by=['HC_count', 'SC_count'], ascending=[False, False])
    
    # Add percentages
    summary['Percentage'] = (summary['Total_Rows'] / len(df)) * 100
    summary['Cumulative'] = summary['Total_Rows'].cumsum()
    summary['Cumulative_Pct'] = (summary['Cumulative'] / len(df)) * 100
    
    print(f"\n{'HC':>3} | {'SC':>3} | {'Total Rows':>12} | {'%':>7} | {'Cumulative':>12} | {'Cum %':>7}")
    print(f"{'-'*3}-+-{'-'*3}-+-{'-'*12}-+-{'-'*7}-+-{'-'*12}-+-{'-'*7}")
    
    for _, row in summary.head(50).iterrows():  # Show top 50
        hc = int(row['HC_count'])
        sc = int(row['SC_count'])
        total = int(row['Total_Rows'])
        pct = row['Percentage']
        cum = int(row['Cumulative'])
        cum_pct = row['Cumulative_Pct']
        print(f"{hc:3d} | {sc:3d} | {total:>12,} | {pct:>6.2f}% | {cum:>12,} | {cum_pct:>6.2f}%")
    
    if len(summary) > 50:
        print(f"... dan {len(summary) - 50} kombinasi lainnya")
    
    # Analysis by HC level
    print(f"\n{'='*90}")
    print(f"DISTRIBUSI DATA PER LEVEL HC:")
    print(f"{'='*90}")
    
    hc_distribution = df_sorted.groupby('HC_count').agg({
        'SC_count': ['count', 'mean', 'min', 'max'],
        'Total_count': 'mean'
    }).round(2)
    
    print(f"\n{'HC':>3} | {'Total Rows':>12} | {'%':>7} | {'SC Mean':>8} | {'SC Min':>7} | {'SC Max':>7} | {'Total Mean':>11}")
    print(f"{'-'*3}-+-{'-'*12}-+-{'-'*7}-+-{'-'*8}-+-{'-'*7}-+-{'-'*7}-+-{'-'*11}")
    
    for hc in sorted(df_sorted['HC_count'].unique(), reverse=True):
        hc_data = df_sorted[df_sorted['HC_count'] == hc]
        count = len(hc_data)
        pct = count / len(df) * 100
        sc_mean = hc_data['SC_count'].mean()
        sc_min = hc_data['SC_count'].min()
        sc_max = hc_data['SC_count'].max()
        total_mean = hc_data['Total_count'].mean()
        
        print(f"{int(hc):3d} | {count:>12,} | {pct:>6.2f}% | {sc_mean:>8.2f} | {int(sc_min):>7d} | {int(sc_max):>7d} | {total_mean:>11.2f}")
    
    # Top quality data (HC ≥ 15)
    print(f"\n{'='*90}")
    print(f"DATA BERKUALITAS TINGGI (HC ≥ 15):")
    print(f"{'='*90}")
    
    high_quality = df_sorted[df_sorted['HC_count'] >= 15]
    print(f"\nTotal data dengan HC ≥ 15: {len(high_quality):,} ({len(high_quality)/len(df)*100:.2f}%)")
    
    if len(high_quality) > 0:
        print(f"\nTop 20 makanan dengan HC & SC terlengkap:")
        print(f"{'-'*90}")
        for i, row in enumerate(high_quality.head(20).itertuples(), 1):
            name = str(row.Name)[:60] if hasattr(row, 'Name') else "N/A"
            print(f"{i:2d}. {name:<60} | HC: {row.HC_count:2.0f}/19 | SC: {row.SC_count:2.0f}/15")
    
    # Low quality data (HC < 5)
    print(f"\n{'='*90}")
    print(f"DATA BERKUALITAS RENDAH (HC < 5):")
    print(f"{'='*90}")
    
    low_quality = df_sorted[df_sorted['HC_count'] < 5]
    print(f"\nTotal data dengan HC < 5: {len(low_quality):,} ({len(low_quality)/len(df)*100:.2f}%)")
    
    if len(low_quality) > 0:
        print(f"\nContoh 10 makanan dengan HC terendah:")
        print(f"{'-'*90}")
        worst = df_sorted.nsmallest(10, ['HC_count', 'SC_count'])
        for i, row in enumerate(worst.itertuples(), 1):
            name = str(row.Name)[:60] if hasattr(row, 'Name') else "N/A"
            print(f"{i:2d}. {name:<60} | HC: {row.HC_count:2.0f}/19 | SC: {row.SC_count:2.0f}/15")
    
    # Save detailed reports
    print(f"\n{'='*90}")
    print(f"MENYIMPAN LAPORAN:")
    print(f"{'='*90}")
    
    # Save summary table
    summary_file = Path(output_dir) / "F. HC_SC_summary_table.csv"
    summary.to_csv(summary_file, index=False)
    print(f"\n1. Summary table: {summary_file}")
    
    # Save HC distribution
    hc_dist_file = Path(output_dir) / "F. HC_distribution.csv"
    hc_dist = df_sorted.groupby('HC_count').agg({
        'SC_count': ['count', 'mean', 'min', 'max', 'std'],
        'Total_count': ['mean', 'min', 'max']
    }).round(2)
    hc_dist.columns = ['_'.join(col).strip() for col in hc_dist.columns.values]
    hc_dist.to_csv(hc_dist_file)
    print(f"2. HC distribution: {hc_dist_file}")
    
    # Save detailed report
    report_file = Path(output_dir) / "F. HC_SC_detailed_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("LAPORAN ANALISIS HARD CONSTRAINT vs SOFT CONSTRAINT\n")
        f.write("="*90 + "\n\n")
        f.write(f"Total data: {len(df):,} baris\n")
        f.write(f"Hard Constraints: {len(hard_constraints)} nutrisi\n")
        f.write(f"Soft Constraints: {len(soft_constraints)} nutrisi\n\n")
        
        f.write("STATISTIK:\n")
        f.write("-"*90 + "\n")
        f.write(f"HC Mean: {df['HC_count'].mean():.2f}/{len(hard_constraints)} ({df['HC_percentage'].mean():.1f}%)\n")
        f.write(f"SC Mean: {df['SC_count'].mean():.2f}/{len(soft_constraints)} ({df['SC_percentage'].mean():.1f}%)\n")
        f.write(f"Data dengan HC lengkap (19/19): {perfect_hc:,} ({perfect_hc/len(df)*100:.2f}%)\n\n")
        
        f.write("TABEL SUMMARY HC vs SC (Top 100):\n")
        f.write("-"*90 + "\n")
        f.write(f"{'HC':>3} | {'SC':>3} | {'Total Rows':>12} | {'%':>7}\n")
        f.write(f"{'-'*3}-+-{'-'*3}-+-{'-'*12}-+-{'-'*7}\n")
        for _, row in summary.head(100).iterrows():
            f.write(f"{int(row['HC_count']):3d} | {int(row['SC_count']):3d} | {int(row['Total_Rows']):>12,} | {row['Percentage']:>6.2f}%\n")
        
        f.write("\n\nDISTRIBUSI PER LEVEL HC:\n")
        f.write("-"*90 + "\n")
        for hc in sorted(df_sorted['HC_count'].unique(), reverse=True):
            hc_data = df_sorted[df_sorted['HC_count'] == hc]
            count = len(hc_data)
            pct = count / len(df) * 100
            f.write(f"HC {int(hc):2d}: {count:>10,} baris ({pct:>5.2f}%) | SC mean: {hc_data['SC_count'].mean():.2f}\n")
    
    print(f"3. Detailed report: {report_file}")
    
    print(f"\n{'='*90}")
    print("✅ ANALISIS SELESAI!")
    print(f"{'='*90}")
    
    return df_sorted, summary

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    data_processed = base_dir / "data" / "processed"
    
    csv_file = data_processed / "4th_nutriensFood.csv"
    
    if not csv_file.exists():
        print(f"❌ Error: File tidak ditemukan: {csv_file}")
        exit(1)
    
    df_sorted, summary = analyze_hard_soft_constraints(str(csv_file), str(data_processed))
