# src/app_streamlit.py
import streamlit as st
import pandas as pd
from plot_charts import annotated_price_volume, sender_receiver_heatmap
from process_onchain import build_matrix

st.title("SHIB — Anomaly & Wallet Flow Explorer (student demo)")

# load price
price_file = st.sidebar.text_input("Price CSV", "../data/shib_price_oct2021.csv")
df = pd.read_csv(price_file, parse_dates=["datetime"], index_col="datetime")
st.write("Price head", df.head())

# compute hourly and zscore anomalies
h = df.resample("1H").agg({"price":"last","volume":"sum"}).dropna()
roll = st.sidebar.number_input("rolling_hours", value=24, min_value=1)
h["vol_mean"] = h["volume"].rolling(roll, min_periods=roll//2).mean()
h["vol_std"]  = h["volume"].rolling(roll, min_periods=roll//2).std(ddof=0)
h["vol_z"]    = (h["volume"] - h["vol_mean"]) / h["vol_std"]
h["anomaly"]  = (h["vol_z"] >= 3)

events = []
if st.sidebar.checkbox("Add event: Oct 28 ATH"):
    events.append((pd.to_datetime("2021-10-28T00:00:00Z"), "Oct 28 ATH"))

fig = annotated_price_volume(h, anomalies_idx=h[h["anomaly"]].index, events=events)
st.plotly_chart(fig, use_container_width=True)

# load transfers matrix
if st.sidebar.checkbox("Show heatmap (requires transfers CSV)"):
    txfile = st.sidebar.text_input("Transfers CSV", "../data/shib_tokentx_sample.csv")
    tx = pd.read_csv(txfile, parse_dates=["timeStamp"])
    pivot, agg = build_matrix(tx, min_amount=1e9)
    hm = sender_receiver_heatmap(pivot, top_n=25)
    st.plotly_chart(hm, use_container_width=True)
