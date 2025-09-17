import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from pathlib import Path

def main(csv_file: str, out_png: str):
    # Load CSV (CoinGecko or CMC format: Date, Price, Volume)
    df = pd.read_csv(csv_file)

    # Standardize column names
    df.columns = [c.lower() for c in df.columns]

    # Try to detect relevant columns
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        df = df.set_index("date")
    else:
        raise ValueError("CSV must contain a 'Date' column")

    # Handle column naming differences
    price_col = [c for c in df.columns if "price" in c][0]
    volume_col = [c for c in df.columns if "volume" in c][0]

    # Compute rolling mean/std for anomaly detection
    df["vol_mean"] = df[volume_col].rolling(7, min_periods=3).mean()
    df["vol_std"] = df[volume_col].rolling(7, min_periods=3).std(ddof=0)
    df["zscore"] = (df[volume_col] - df["vol_mean"]) / df["vol_std"]
    df["anomaly"] = df["zscore"] > 3  # flag 3σ spikes

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(10,5))
    ax2 = ax1.twinx()

    ax1.plot(df.index, df[price_col], color="blue", label="Price (USD)")
    ax2.bar(df.index, df[volume_col], color="gray", alpha=0.3, label="Volume")

    # Highlight anomalies in red
    ax2.bar(df.index[df["anomaly"]], df.loc[df["anomaly"], volume_col],
            color="red", alpha=0.7, label="Anomaly")

    ax1.set_ylabel("Price (USD)")
    ax2.set_ylabel("Volume")
    ax1.set_title("Crypto Forensics Analysis — Price & Volume Anomalies")

    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.tight_layout()
    plt.savefig(out_png)
    print(f"Chart saved to {out_png}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Input CSV (from CoinGecko/CMC)")
    ap.add_argument("--out", default="chart.png", help="Output PNG filename")
    args = ap.parse_args()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    main(args.csv, args.out)
