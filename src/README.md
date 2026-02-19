# Source Code Directory

Folder untuk source code algoritma dan utility functions.

## Struktur yang Disarankan:
```
src/
├── data/
│   ├── load_data.py          # Functions untuk load data
│   └── preprocessing.py      # Data preprocessing functions
├── features/
│   └── feature_engineering.py # Feature engineering
├── models/
│   ├── train.py              # Training scripts
│   └── predict.py            # Prediction scripts
└── utils/
    └── helpers.py            # Helper functions
```

## Guidelines:
- Pisahkan code ke modules yang logical
- Buat functions yang reusable
- Dokumentasi dengan docstrings
- Unit tests untuk functions penting
