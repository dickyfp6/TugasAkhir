"""
Script untuk filtering makanan yang mengandung kata haram
Author: Created for Tugas Akhir
Date: February 25, 2026

Fungsi:
- Membaca list kata haram dari file txt
- Filter menu makanan yang mengandung minimal 1 kata haram dalam nama
- Simpan hasil ke file baru (tanpa makanan haram)
"""

import pandas as pd
import os
from pathlib import Path

def load_haram_words(file_path):
    """
    Load list kata haram dari file txt
    
    Args:
        file_path (str): Path ke file txt berisi kata haram
        
    Returns:
        set: Set of haram words dalam uppercase
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        haram_words = {line.strip().upper() for line in f if line.strip()}
    return haram_words

def contains_haram_word(food_name, haram_words_set):
    """
    Check apakah nama makanan mengandung kata haram
    
    Args:
        food_name (str): Nama makanan
        haram_words_set (set): Set kata-kata haram
        
    Returns:
        bool: True jika mengandung kata haram, False jika tidak
    """
    if pd.isna(food_name):
        return False
    
    # Split nama makanan menjadi kata-kata individual
    # Menggunakan split() untuk memisahkan berdasarkan spasi dan karakter lain
    food_words = str(food_name).upper().replace(',', ' ').replace('/', ' ').split()
    
    # Check apakah ada kata yang match dengan haram words
    for word in food_words:
        if word in haram_words_set:
            return True
    
    return False

def filter_haram_foods(input_csv, haram_list_txt, output_csv):
    """
    Filter makanan yang mengandung kata haram
    
    Args:
        input_csv (str): Path ke cleaned_nutrition_table.csv
        haram_list_txt (str): Path ke listHaram.txt
        output_csv (str): Path untuk output file (halal foods only)
    """
    print("=" * 60)
    print("FILTERING MAKANAN HARAM")
    print("=" * 60)
    
    # Load haram words
    print(f"\n1. Loading haram words dari: {haram_list_txt}")
    haram_words = load_haram_words(haram_list_txt)
    print(f"   ✓ Total kata haram: {len(haram_words)}")
    print(f"   ✓ Contoh kata: {list(haram_words)[:5]}")
    
    # Load nutrition table
    print(f"\n2. Loading nutrition table dari: {input_csv}")
    print("   (File besar, mohon tunggu...)")
    df = pd.read_csv(input_csv, low_memory=False)
    print(f"   ✓ Total baris: {len(df):,}")
    print(f"   ✓ Kolom: {list(df.columns[:5])}...")
    
    # Filter haram foods
    print("\n3. Filtering makanan yang mengandung kata haram...")
    initial_count = len(df)
    
    # Buat kolom boolean untuk marking haram foods
    df['is_haram'] = df['Name'].apply(lambda x: contains_haram_word(x, haram_words))
    
    # Count haram vs halal
    haram_count = df['is_haram'].sum()
    halal_count = len(df) - haram_count
    
    print(f"   ✓ Makanan HARAM (dihapus): {haram_count:,} ({haram_count/initial_count*100:.2f}%)")
    print(f"   ✓ Makanan HALAL (disimpan): {halal_count:,} ({halal_count/initial_count*100:.2f}%)")
    
    # Show some examples of removed foods
    if haram_count > 0:
        print("\n   Contoh makanan yang dihapus:")
        haram_samples = df[df['is_haram']]['Name'].head(10).tolist()
        for i, food in enumerate(haram_samples, 1):
            print(f"      {i}. {food}")
    
    # Keep only halal foods and remove helper column
    df_halal = df[~df['is_haram']].drop('is_haram', axis=1)
    
    # Save to new file
    print(f"\n4. Menyimpan hasil ke: {output_csv}")
    df_halal.to_csv(output_csv, index=False)
    print(f"   ✓ File berhasil disimpan!")
    print(f"   ✓ Total baris di file baru: {len(df_halal):,}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Input file:      {input_csv}")
    print(f"Haram list:      {haram_list_txt}")
    print(f"Output file:     {output_csv}")
    print(f"Original rows:   {initial_count:,}")
    print(f"Removed rows:    {haram_count:,}")
    print(f"Remaining rows:  {len(df_halal):,}")
    print(f"Reduction:       {haram_count/initial_count*100:.2f}%")
    print("=" * 60)
    print("\n✅ Filtering selesai!")
    
    return df_halal

if __name__ == "__main__":
    # Define paths
    base_dir = Path(__file__).parent.parent
    data_processed = base_dir / "data" / "processed"
    
    input_csv = data_processed / "cleaned_nutrition_table.csv"
    haram_list_txt = data_processed / "listHaram.txt"
    output_csv = data_processed / "halal_food.csv"
    
    # Check if files exist
    if not input_csv.exists():
        print(f"❌ Error: File tidak ditemukan: {input_csv}")
        exit(1)
    
    if not haram_list_txt.exists():
        print(f"❌ Error: File tidak ditemukan: {haram_list_txt}")
        exit(1)
    
    # Run filtering
    df_halal = filter_haram_foods(str(input_csv), str(haram_list_txt), str(output_csv))
