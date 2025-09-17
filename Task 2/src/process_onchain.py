# src/process_onchain.py
import pandas as pd
from pathlib import Path
import numpy as np

def build_matrix(transfers_df, min_amount=5e9):
    # transfers_df should have columns: from, to, value (in token units), timeStamp (datetime)
    df = transfers_df.copy()
    df = df.rename(columns={"from":"sender","to":"receiver"})
    # Filter by amount threshold to reduce noise (tune min_amount)
    df = df[df["value"] >= min_amount]
    # aggregate
    agg = df.groupby(["sender","receiver"], as_index=False)["value"].sum()
    # pivot
    pivot = agg.pivot(index="sender", columns="receiver", values="value").fillna(0)
    return pivot, agg

if __name__ == "__main__":
    df = pd.read_csv("../data/shib_tokentx_sample.csv", parse_dates=["timeStamp"])
    pivot, agg = build_matrix(df, min_amount=1e9)  # tune
    pivot.to_csv("../data/shib_sender_receiver_matrix.csv")
    print("matrix saved, shape", pivot.shape)
