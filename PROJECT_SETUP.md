# Python Project Setup Guide

## 1. Open the folder

Open `math470_es_project` in VS Code or PyCharm.

## 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Build the cleaned dataset

```bash
python src/01_build_dataset.py
```

## 4. Check outputs

Main file:

```text
data/processed/modeling_dataset.csv
```

Dictionary for macro feature IDs:

```text
data/interim/macro_feature_dictionary.csv
```

Cleaning summary:

```text
data/processed/cleaning_report.txt
```

## 5. Recommended modeling target

Start with:

```text
high_risk_es_60d
```

This is a binary early-warning label. It equals 1 when the future 60-trading-day realized ES is above the 90th percentile threshold estimated from the training period.
