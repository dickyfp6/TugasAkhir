"""
Script untuk filtering kolom dari halal_food.csv
Keep hanya kolom yang ada di listNutriens.txt
Author: Created for Tugas Akhir
Date: February 25, 2026
"""

import pandas as pd
from pathlib import Path

def filter_columns(input_csv, nutrient_list_file, output_csv):
    """
    Filter kolom CSV, keep hanya kolom yang ada di nutrient list
    
    Args:
        input_csv (str): Path ke halal_food.csv
        nutrient_list_file (str): Path ke listNutriens.txt
        output_csv (str): Path untuk output nutriensFood.csv
    """
    print("=" * 70)
    print("FILTERING KOLOM NUTRISI")
    print("=" * 70)
    
    # Load list kolom yang diinginkan
    print(f"\n1. Loading list kolom dari: {nutrient_list_file}")
    with open(nutrient_list_file, 'r', encoding='utf-8') as f:
        desired_columns = [line.strip() for line in f if line.strip()]
    
    print(f"   ✓ Total kolom yang akan dipertahankan: {len(desired_columns)}")
    print(f"   ✓ Kolom: {', '.join(desired_columns[:5])}...")
    
    # Load CSV
    print(f"\n2. Loading data dari: {input_csv}")
    print("   (File besar ~410MB, mohon tunggu...)")
    
    # Load with only desired columns to save memory
    df = pd.read_csv(input_csv, usecols=desired_columns, low_memory=False)
    
    print(f"   ✓ Data berhasil dimuat!")
    print(f"   ✓ Total baris: {len(df):,}")
    print(f"   ✓ Total kolom: {len(df.columns)}")
    
    # Show column info
    print(f"\n3. Info kolom yang dipertahankan:")
    for i, col in enumerate(df.columns, 1):
        non_null = df[col].notna().sum()
        null_count = df[col].isna().sum()
        print(f"   {i:2d}. {col:40s} - Non-null: {non_null:>9,} ({non_null/len(df)*100:5.1f}%)")
    
    # Save to new file
    print(f"\n4. Menyimpan hasil ke: {output_csv}")
    df.to_csv(output_csv, index=False)
    print(f"   ✓ File berhasil disimpan!")
    
    # File size comparison
    import os
    input_size = os.path.getsize(input_csv) / (1024 * 1024)  # MB
    output_size = os.path.getsize(output_csv) / (1024 * 1024)  # MB
    reduction = (1 - output_size / input_size) * 100
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Input file:          {input_csv}")
    print(f"Nutrient list:       {nutrient_list_file}")
    print(f"Output file:         {output_csv}")
    print(f"Total rows:          {len(df):,}")
    print(f"Original columns:    117")
    print(f"Kept columns:        {len(df.columns)}")
    print(f"Removed columns:     {117 - len(df.columns)}")
    print(f"Input file size:     {input_size:.2f} MB")
    print(f"Output file size:    {output_size:.2f} MB")
    print(f"Size reduction:      {reduction:.1f}%")
    print("=" * 70)
    print("\n✅ Filtering kolom selesai!")
    
    return df

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    data_processed = base_dir / "data" / "processed"
    
    input_csv = data_processed / "3rd_halalFood.csv"
    nutrient_list = data_processed / "C. listNutriens.txt"
    output_csv = data_processed / "4th_nutriensFood.csv"
    
    # Check if files exist
    if not input_csv.exists():
        print(f"❌ Error: File tidak ditemukan: {input_csv}")
        exit(1)
    
    if not nutrient_list.exists():
        print(f"❌ Error: File tidak ditemukan: {nutrient_list}")
        exit(1)
    
    # Run filtering
    df = filter_columns(str(input_csv), str(nutrient_list), str(output_csv))
