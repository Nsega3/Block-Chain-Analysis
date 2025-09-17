# src/plot_charts.py
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def annotated_price_volume(df, anomalies_idx=None, events=[]):
    # df indexed by datetime with columns price, volume
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["price"], name="Price (USD)", yaxis="y1"))
    fig.add_trace(go.Bar(x=df.index, y=df["volume"], name="Volume", yaxis="y2", opacity=0.4))
    # add anomaly markers
    if anomalies_idx is not None and len(anomalies_idx)>0:
        fig.add_trace(go.Scatter(x=anomalies_idx, y=df.loc[anomalies_idx,"price"],
                                 mode="markers", marker=dict(size=8, color="red"),
                                 name="Anomaly"))
    # annotate events: list of (dt, label)
    for dt,label in events:
        fig.add_vline(x=dt, line_dash="dash")
        fig.add_annotation(x=dt, y=df["price"].max(), text=label, showarrow=False, yshift=10)
    # layout
    fig.update_layout(legend=dict(orientation="h"),
                      yaxis=dict(title="Price (USD)"),
                      yaxis2=dict(title="Volume", overlaying="y", side="right"))
    return fig

def sender_receiver_heatmap(pivot_df, top_n=20):
    # reduce to top N rows+cols by total flow
    rows_sum = pivot_df.sum(axis=1).sort_values(ascending=False)
    cols_sum = pivot_df.sum(axis=0).sort_values(ascending=False)
    rows = rows_sum.head(top_n).index
    cols = cols_sum.head(top_n).index
    small = pivot_df.reindex(index=rows, columns=cols).fillna(0)
    # normalize or log scale
    mat = np.log1p(small.values)
    fig = go.Figure(data=go.Heatmap(
        z=mat,
        x=[c[:10]+'...' for c in cols],
        y=[r[:10]+'...' for r in rows],
        colorbar=dict(title="log(1+SHIB)")
    ))
    fig.update_layout(title="Sender → Receiver heatmap (log1p)")
    return fig
