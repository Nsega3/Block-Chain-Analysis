import requests
import pandas as pd
from typing import List
from .config import BASE_URL, CHAIN_ID, ETHERSCAN_API_KEY, ETHER_VALUE

def make_api_url(module: str, action: str, address: str, **kwargs) -> str:
    url = f"{BASE_URL}?chainid={CHAIN_ID}&module={module}&action={action}&address={address}&apikey={ETHERSCAN_API_KEY}"
    for k, v in kwargs.items():
        url += f"&{k}={v}"
    return url

def fetch_normal_transactions(address: str, offset: int = 20, sort: str = "desc") -> List[dict]:
    url = make_api_url("account", "txlist", address,
                       startblock=0, endblock=99999999, page=1,
                       offset=offset, sort=sort)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("result", [])

def txs_to_dataframe(txs: list) -> pd.DataFrame:
    if not txs: return pd.DataFrame()
    df = pd.DataFrame(txs)
    for col in ("value","gasPrice","gasUsed","timeStamp"):
        if col in df: df[col] = pd.to_numeric(df[col], errors="coerce")
    if "timeStamp" in df:
        df["timestamp"] = pd.to_datetime(df["timeStamp"], unit="s", utc=True)
    if "value" in df:
        df["value_eth"] = df["value"] / ETHER_VALUE
    if {"gasUsed","gasPrice"}.issubset(df.columns):
        df["gas_cost_eth"] = (df["gasUsed"] * df["gasPrice"]) / ETHER_VALUE
    keep = ["hash","from","to","value_eth","gas_cost_eth","timestamp"]
    return df[[c for c in keep if c in df.columns]].copy()

