import sqlite3
from pathlib import Path
from sources.census import CensusConfig
from normalization.normalize import Normalize

DB_PATH = Path(__file__).parent.parent / "data" / "smart_living.db"
SCHEMA_PATH = Path(__file__).parent.parent / "data" / "schema.sql"

METRIC_TYPES = [
    ("median_household_income", "Median Household Income", "economy", "USD", True),
    ("median_gross_rent", "Median Gross Rent", "housing", "USD", False),
    ("poverty_rate", "Poverty Rate", "economy", "percent", False),
    ("unemployment_rate", "Unemployment Rate", "economy", "percent", False),
    ("bachelor_degree_or_higher", "Bachelor's Degree or Higher", "education", "percent", True),
]

def bootstrap_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())
    conn.close()

def seed_metric_types():
    conn = sqlite3.connect(DB_PATH)
    conn.executemany(
        "INSERT OR IGNORE INTO metric_types (code, name, category, unit, higher_is_better) "
        "VALUES (?, ?, ?, ?, ?)",
        METRIC_TYPES,
    )
    conn.commit()
    conn.close()

def main():
    bootstrap_db()
    seed_metric_types()
    config = CensusConfig()
    config.merge(DB_PATH)
    norm = Normalize()
    norm.normalize_metrics(DB_PATH)

if __name__ == "__main__":
    main()