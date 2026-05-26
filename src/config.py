
"""
Configuration for Ethiopian Coffee Traceability & Responsible Sourcing GIS Project
Aligned with EUDR, Volcafe Responsible Sourcing, ECX & SCA standards.
"""

from pathlib import Path
import sys

# Add project root to Python path
BASE_DIR = Path(__file__).parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Data Paths
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

MOCK_DATA_CSV = DATA_DIR / "mock_traceability_data.csv"
PROCESSED_PICKLE = PROCESSED_DIR / "traceability_data.pkl"

# Industry Standards & Constants
EUDR_CUTOFF_DATE = "2020-12-31"
SPECIALTY_THRESHOLD = 80.0

# Standard Lists
REGIONS = ["Yirgacheffe", "Guji", "Sidama", "Limmu"]
TRACEABILITY_LEVELS = ["Full Farm", "Washing Station", "Exporter"]
SUSTAINABILITY_CERTS = ["Organic", "Volcafe Verified", "Rainforest Alliance", "None"]
DEFORESTATION_RISKS = ["Low", "Medium", "High"]
COMPLIANCE_STATUS = ["Compliant", "In Progress", "At Risk"]

# Color schemes for maps
COMPLIANCE_COLORS = {
    "Compliant": "green",
    "In Progress": "orange",
    "At Risk": "red"
}

print("Traceability & Responsible Sourcing Config loaded successfully!")
print(f"Project Root: {BASE_DIR}")
