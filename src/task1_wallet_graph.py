import argparse
import pandas as pd
from .viz_utils import plot_wallet_graph
from .io_utils import fetch_normal_transactions, txs_to_dataframe, pretty_print_txs

def build_edges(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return df
    edges = df.rename(columns={"from":"src","to":"dst"}).copy()
    edges["weight"] = 1
    edges = edges.rename(columns={"src":"from","dst":"to"})
    return edges[["from","to","weight"]]

def main():
    p = argparse.ArgumentParser(description="Task 1: wallet transaction graph")
    p.add_argument("--wallet", required=True, help="ETH address")
    p.add_argument("--limit", type=int, default=20, help="max txs")
    p.add_argument("--out-csv", default="data/outputs/edges.csv")
    p.add_argument("--out-png", default="data/outputs/wallet_graph.png")
    args = p.parse_args()

    txs = fetch_normal_transactions(args.wallet, args.limit, "desc")
    pretty_print_txs(df, args.limit)
    df = txs_to_dataframe(txs)
    edges = build_edges(df.head(args.limit))
    edges.to_csv(args.out_csv, index=False)
    print(f"Saved edges -> {args.out_csv}")
    plot_wallet_graph(edges, args.out_png)

if __name__ == "__main__":
    main()
