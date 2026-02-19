# Data Directory

Folder ini berisi semua dataset untuk project Tugas Akhir.

## Struktur Folder:

### 📁 `raw/`
Data mentah yang belum diolah. Jangan edit file di folder ini!
- Source data asli
- Backup data original

### 📁 `interim/`
Data intermediate/sementara selama proses cleaning dan transformasi.
- Data yang sedang dalam proses cleaning
- File temporary hasil preprocessing
- Eksperimen data transformation

### 📁 `processed/`
Data yang sudah bersih dan siap digunakan untuk modeling/analysis.
- Data final yang sudah dibersihkan
- Data yang siap untuk training model
- Data untuk visualisasi

## Notes:
- File CSV >100MB sudah di-handle dengan Git LFS
- Semua file `.csv` otomatis di-track oleh LFS (lihat `.gitattributes`)
