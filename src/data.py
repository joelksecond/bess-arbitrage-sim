"""Download and load NEM spot prices from AEMO."""
from pathlib import Path

import pandas as pd

RAW_CACHE = Path("data/raw")
CLEAN_FILE = Path("data/vic_prices.csv")


def download_prices(start, end, region="VIC1"):
    """Download 5-minute dispatch prices for one region and save a clean CSV.

    start, end: strings like "2024/10/01 00:00:00"
    """
    from nemosis import dynamic_data_compiler

    RAW_CACHE.mkdir(parents=True, exist_ok=True)
    raw = dynamic_data_compiler(
        start, end, "DISPATCHPRICE", str(RAW_CACHE),
        select_columns=["SETTLEMENTDATE", "REGIONID", "INTERVENTION", "RRP"],
        filter_cols=["REGIONID"], filter_values=([region],),
    )
    raw = raw[raw["INTERVENTION"] == 0]          # keep normal market runs only
    prices = (
        raw.rename(columns={"SETTLEMENTDATE": "timestamp", "RRP": "price"})
        [["timestamp", "price"]]
        .drop_duplicates("timestamp")
        .sort_values("timestamp")
    )
    CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    prices.to_csv(CLEAN_FILE, index=False)
    return load_prices()


def load_prices(path=CLEAN_FILE):
    """Load the clean price CSV as a Series indexed by timestamp ($/MWh)."""
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df.set_index("timestamp")["price"]