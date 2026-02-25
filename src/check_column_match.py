"""
Script untuk checking apakah kolom di listNutriens.txt match dengan kolom di CSV
"""

import pandas as pd
from pathlib import Path

def check_column_match(csv_file, nutrient_list_file):
    """
    Check apakah semua kolom di nutrient list ada di CSV
    """
    print("=" * 70)
    print("CHECKING KOLOM MATCH")
    print("=" * 70)
    
    # Load nutrient list
    print(f"\n1. Loading nutrient list dari: {nutrient_list_file}")
    with open(nutrient_list_file, 'r', encoding='utf-8') as f:
        desired_columns = [line.strip() for line in f if line.strip()]
    
    print(f"   ✓ Total kolom yang diinginkan: {len(desired_columns)}")
    
    # Load CSV header (only first row to save memory)
    print(f"\n2. Loading header dari CSV: {csv_file}")
    df_columns = pd.read_csv(csv_file, nrows=0).columns.tolist()
    print(f"   ✓ Total kolom di CSV: {len(df_columns)}")
    
    # Check matching
    print(f"\n3. Checking matching...")
    
    # Find columns that exist in desired list but NOT in CSV
    missing_in_csv = []
    exact_matches = []
    
    for desired_col in desired_columns:
        if desired_col in df_columns:
            exact_matches.append(desired_col)
        else:
            missing_in_csv.append(desired_col)
    
    # Print results
    print(f"\n{'='*70}")
    print(f"HASIL CHECKING:")
    print(f"{'='*70}")
    print(f"✅ Kolom yang MATCH: {len(exact_matches)}/{len(desired_columns)}")
    print(f"❌ Kolom yang TIDAK MATCH: {len(missing_in_csv)}/{len(desired_columns)}")
    
    if missing_in_csv:
        print(f"\n{'='*70}")
        print(f"⚠️  KOLOM YANG TIDAK DITEMUKAN DI CSV:")
        print(f"{'='*70}")
        
        for missing_col in missing_in_csv:
            print(f"\n❌ '{missing_col}'")
            
            # Try to find similar column names (case-insensitive, fuzzy match)
            similar = []
            missing_lower = missing_col.lower()
            
            for csv_col in df_columns:
                csv_col_lower = csv_col.lower()
                
                # Check if very similar
                if missing_lower in csv_col_lower or csv_col_lower in missing_lower:
                    similar.append(csv_col)
                # Check word overlap
                elif any(word in csv_col_lower for word in missing_lower.split() if len(word) > 3):
                    similar.append(csv_col)
            
            if similar:
                print(f"   💡 Mungkin maksudnya salah satu dari ini:")
                for sim in similar[:5]:  # Show max 5 suggestions
                    print(f"      - '{sim}'")
            else:
                print(f"   ⚠️  Tidak ada kolom yang mirip ditemukan")
    
    else:
        print(f"\n✅ SEMUA KOLOM MATCH! Aman untuk proceed ke filtering.")
    
    # Show some matched columns as confirmation
    if exact_matches:
        print(f"\n{'='*70}")
        print(f"✅ CONTOH KOLOM YANG MATCH:")
        print(f"{'='*70}")
        for col in exact_matches[:10]:
            print(f"   ✓ {col}")
        if len(exact_matches) > 10:
            print(f"   ... dan {len(exact_matches) - 10} kolom lainnya")
    
    print(f"\n{'='*70}")
    
    return {
        'exact_matches': exact_matches,
        'missing_in_csv': missing_in_csv,
        'all_csv_columns': df_columns
    }

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    data_processed = base_dir / "data" / "processed"
    
    csv_file = data_processed / "3rd_halalFood.csv"
    nutrient_list = data_processed / "C. listNutriens.txt"
    
    if not csv_file.exists():
        print(f"❌ Error: File tidak ditemukan: {csv_file}")
        exit(1)
    
    if not nutrient_list.exists():
        print(f"❌ Error: File tidak ditemukan: {nutrient_list}")
        exit(1)
    
    result = check_column_match(str(csv_file), str(nutrient_list))
    
    # Save hasil ke file untuk reference
    output_file = data_processed / "column_check_result.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("COLUMN MATCHING RESULT\n")
        f.write("="*70 + "\n\n")
        f.write(f"Matched columns ({len(result['exact_matches'])}):\n")
        for col in result['exact_matches']:
            f.write(f"  ✓ {col}\n")
        f.write(f"\nMissing columns ({len(result['missing_in_csv'])}):\n")
        for col in result['missing_in_csv']:
            f.write(f"  ✗ {col}\n")
    
    print(f"\n💾 Hasil checking juga disimpan di: {output_file}")
