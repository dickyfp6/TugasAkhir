import pandas as pd
import re
from collections import Counter
import os

# Path ke file
input_file = r"c:\Users\USERR\Documents\0. Mata Kuliah\7 - Pra-TA\Tugas Akhir\data\processed\cleaned_nutrition_table.csv"
output_file = r"c:\Users\USERR\Documents\0. Mata Kuliah\7 - Pra-TA\Tugas Akhir\data\processed\word_variations_with_frequency.csv"

print("📊 Memulai ekstraksi kata dari kolom Name...")
print(f"Input file: {input_file}")

# Baca CSV
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"✅ Total baris data: {len(df)}")

# Stopwords dan kata yang ingin diabaikan
stopwords = {
    'AND', 'WITH', 'THE', 'FOR', 'FROM', 'HAS', 'ARE', 'WAS', 'WERE',
    'WILL', 'CAN', 'COULD', 'WOULD', 'SHOULD', 'MAY', 'MIGHT',
    'THIS', 'THAT', 'THESE', 'THOSE', 'THAN', 'THEN', 'WHEN', 'WHERE',
    'WHO', 'WHY', 'HOW', 'ALL', 'ANY', 'SOME', 'FEW', 'MORE', 'MOST'
}

# Unit ukuran dan kata umum lainnya yang ingin diabaikan
units = {
    'OZ', 'GAL', 'LB', 'LBS', 'ML', 'MG', 'KG', 'GM', 'GR', 'CUP', 'CUPS',
    'TSP', 'TBSP', 'PINT', 'QUART', 'LITER', 'PCT', 'PERCENT'
}

# Ekstrak semua kata
all_words = []

for name in df['Name'].dropna():
    # Konversi ke uppercase untuk konsistensi
    name = str(name).upper()
    
    # Split berdasarkan spasi dan karakter non-alfabet
    words = re.findall(r'[A-Z]+', name)
    
    for word in words:
        # Filter kata
        if (len(word) >= 3 and  # Panjang minimal 3 karakter
            not word.isdigit() and  # Bukan angka
            word not in stopwords and  # Bukan stopword
            word not in units):  # Bukan unit ukuran
            all_words.append(word)

print(f"✅ Total kata yang diekstrak (dengan duplikat): {len(all_words)}")

# Hitung frekuensi
word_freq = Counter(all_words)
print(f"✅ Total kata unik: {len(word_freq)}")

# Konversi ke DataFrame dan sort berdasarkan frekuensi
result_df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
result_df = result_df.sort_values('Frequency', ascending=False).reset_index(drop=True)

# Simpan ke CSV
result_df.to_csv(output_file, index=False, encoding='utf-8')
print(f"✅ Hasil disimpan ke: {output_file}")

# Tampilkan statistik
print("\n" + "="*60)
print("📈 STATISTIK:")
print("="*60)
print(f"Total kata unik: {len(result_df)}")
print(f"Total kemunculan kata: {result_df['Frequency'].sum()}")
print(f"Rata-rata frekuensi: {result_df['Frequency'].mean():.2f}")
print(f"Median frekuensi: {result_df['Frequency'].median():.0f}")

# Tampilkan 30 kata teratas
print("\n" + "="*60)
print("🔝 TOP 30 KATA YANG PALING SERING MUNCUL:")
print("="*60)
for idx, row in result_df.head(30).iterrows():
    print(f"{idx+1:3d}. {row['Word']:25s} - {row['Frequency']:,} kali")

print("\n✅ Proses selesai!")
