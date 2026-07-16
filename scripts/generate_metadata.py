from pathlib import Path
import pandas as pd
import json
from datetime import datetime

# =====================================================
# Configuration
# =====================================================

COMPANY_INFO = {
    "apple": {
        "company": "Apple",
        "ticker": "AAPL",
        "industry": "Consumer Electronics",
        "country": "USA",
    },
    "amd": {
        "company": "AMD",
        "ticker": "AMD",
        "industry": "Semiconductor",
        "country": "USA",
    },
    "nvidia": {
        "company": "NVIDIA",
        "ticker": "NVDA",
        "industry": "Semiconductor",
        "country": "USA",
    },
    "intel": {
        "company": "Intel",
        "ticker": "INTC",
        "industry": "Semiconductor",
        "country": "USA",
    },
    "qualcomm": {
        "company": "Qualcomm",
        "ticker": "QCOM",
        "industry": "Semiconductor",
        "country": "USA",
    },
    "tsmc": {
        "company": "TSMC",
        "ticker": "TSM",
        "industry": "Semiconductor Foundry",
        "country": "Taiwan",
    },
    "foxconn": {
        "company": "Foxconn",
        "ticker": "2317.TW",
        "industry": "Electronics Manufacturing",
        "country": "Taiwan",
    },
    "flex": {
        "company": "Flex",
        "ticker": "FLEX",
        "industry": "Electronics Manufacturing",
        "country": "Singapore",
    },
    "jabil": {
        "company": "Jabil",
        "ticker": "JBL",
        "industry": "Electronics Manufacturing",
        "country": "USA",
    },
    "broadcom": {
        "company": "Broadcom",
        "ticker": "AVGO",
        "industry": "Semiconductor",
        "country": "USA",
    },
}

# =====================================================
# Folder Mapping
# =====================================================

DOCUMENT_TYPES = {
    "annual_reports": "annual_report",
    "company_profiles": "company_profile",
    "wikipedia": "wikipedia",
}

SOURCE_MAPPING = {
    "annual_reports": "Investor Relations",
    "company_profiles": "Official Website",
    "wikipedia": "Wikipedia",
}

RAW_DATA = Path("data/raw")
OUTPUT_DIR = RAW_DATA / "metadata"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

metadata = []

# =====================================================
# Scan Files
# =====================================================

for folder_name, document_type in DOCUMENT_TYPES.items():

    folder = RAW_DATA / folder_name

    if not folder.exists():
        continue

    for file in folder.glob("*.pdf"):

        filename = file.stem.lower()

        company_key = filename.split("_")[0]

        if company_key not in COMPANY_INFO:
            print(f"Skipping unknown company: {file.name}")
            continue

        company = COMPANY_INFO[company_key]

        year = None

        for part in filename.split("_"):
            if part.isdigit() and len(part) == 4:
                year = int(part)
                break

        if year is None:
            year = datetime.now().year

        metadata.append({
            "document_id": filename,
            "company": company["company"],
            "ticker": company["ticker"],
            "industry": company["industry"],
            "country": company["country"],
            "document_type": document_type,
            "source": SOURCE_MAPPING[folder_name],
            "year": year,
            "language": "English",
            "file_name": file.name,
            "file_path": str(file).replace("\\", "/"),
            "status": "raw",
        })

# =====================================================
# Save CSV
# =====================================================

df = pd.DataFrame(metadata)

csv_path = OUTPUT_DIR / "metadata.csv"

df.to_csv(csv_path, index=False)

# =====================================================
# Save JSON
# =====================================================

json_path = OUTPUT_DIR / "metadata.json"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4)

# =====================================================
# Summary
# =====================================================

print("=" * 50)
print("Metadata Generation Completed")
print("=" * 50)
print(f"Documents Found : {len(metadata)}")
print(f"CSV Saved       : {csv_path}")
print(f"JSON Saved      : {json_path}")
print("=" * 50)