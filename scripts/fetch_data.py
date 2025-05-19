# Script to fetch economic and financial data
import os
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime

FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"

# Fetch FRED time series
def fetch_fred_series(series_id, start_data="2017-01-01", end_date="2024-12-31"):
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
    }
    response = requests.get(FRED_URL, params=params)
    response.raise_for_status()
    data = response.json()["observations"]
    df = pd.DataFrame(data)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    return df[["date", "value"]].rename(columns={"value": series_id})

# Fetch stock data with Yahoo Finance
def fetch_stock_data(ticker, start="2017-01-01", end="2024-12-31"):
    df = yf.download(ticker, start=start, end=end)
    df.reset_index(inplace=True)
    return df[["Date", "Close"]].rename(columns={"Close": ticker})

# Save all datasets
def save_all_data():
    os.makedirs("data", exist_ok=True)

    print("Fetching FRED data...")
    cpi = fetch_fred_series("CPIAUCSL")
    unemp = fetch_fred_series("UNRATE")
    gdp = fred_fred_series("GDP")

    cpi.to_csv("data/cpi.csv", index=False)
    unemp.to_csv("data/unemployment.csv", index=False)
    gdp.to_csv("data/gdp.csv", index=False)

    print("Fetching stock sector data from Yahoo Finance...")
    tech = fetch_stock_data("XLK")
    fin = fetch_stock_data("XLF")
    ind = fetch_stock_data("XLI")

    tech.to_csv("data/tech_sector.csv", index=False)
    fin.to_csv("data/financial_sector.csv", index=False)
    ind.to_csv("data/industrial_sector.csv", index=False)

    print("All data saved to /data")

    # Run the script
    if __name__ == "__main__":
        save_all_data()