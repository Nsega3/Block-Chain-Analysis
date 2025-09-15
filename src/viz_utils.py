import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

def plot_wallet_graph(edges_df: pd.DataFrame, out_path: str):
    if edges_df.empty:
        print("No edges to plot.")
        return
    G = nx.DiGraph()
    for _, r in edges_df.iterrows():
        G.add_edge(r["from"], r["to"], weight=r.get("weight", 1))
    plt.figure(figsize=(8,6))
    pos = nx.spring_layout(G, seed=42)  # deterministic layout
    nx.draw(G, pos, with_labels=False, node_size=300, arrows=True)
    plt.title("Wallet Transaction Graph (subset)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved graph -> {out_path}")
