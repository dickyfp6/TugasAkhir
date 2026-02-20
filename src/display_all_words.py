import pandas as pd
import sys

# Set encoding untuk output
sys.stdout.reconfigure(encoding='utf-8')

# Baca file CSV
file_path = r"c:\Users\USERR\Documents\0. Mata Kuliah\7 - Pra-TA\Tugas Akhir\data\processed\word_variations_with_frequency.csv"
df = pd.read_csv(file_path)

print("=" * 70)
print(f"DAFTAR LENGKAP SEMUA {len(df)} KATA UNIK DARI KOLOM NAME")
print("=" * 70)
print()

# Tampilkan semua kata dengan nomor urut
for idx, row in df.iterrows():
    print(f"{idx+1:5d}. {row['Word']:30s} - {row['Frequency']:,} kali")

print()
print("=" * 70)
print(f">> Total: {len(df)} kata unik")
print(f">> Total kemunculan: {df['Frequency'].sum():,} kali")
print("=" * 70)
