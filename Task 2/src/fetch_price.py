# src/fetch_price.py
import requests, time
import pandas as pd
from dateutil import parser
from pathlib import Path

COINGECKO_ID = "shiba-inu"
VS_CURRENCY = "usd"

def fetch_range(start_unix, end_unix):
    url = "https://api.coingecko.com/api/v3/coins/{id}/market_chart/range".format(id=COINGECKO_ID)
    params = {"vs_currency": VS_CURRENCY, "from": int(start_unix), "to": int(end_unix)}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
  
    # prices and volumes are lists of [ts_ms, value]
    dfp = pd.DataFrame(data["prices"], columns=["ts","price"])
    dfv = pd.DataFrame(data["total_volumes"], columns=["ts","volume"])
    df = dfp.merge(dfv, on="ts")
    df["datetime"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    df = df.set_index("datetime").drop(columns=["ts"])
    return df

if __name__ == "__main__":
    import os
    # example: Oct 1 2021 - Oct 31 2021
    start = "2021-10-01T00:00:00+00:00"
    end   = "2021-10-31T23:59:59+00:00"
    s_unix = int(parser.isoparse(start).timestamp())
    e_unix = int(parser.isoparse(end).timestamp())
    df = fetch_range(s_unix, e_unix)
    outdir = Path("../data")
    outdir.mkdir(parents=True, exist_ok=True)
    df.to_csv(outdir / "shib_price_oct2021.csv")
    print("Saved", len(df), "rows")
