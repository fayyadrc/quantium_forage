from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd


app = Dash(__name__)
df = pd.read_csv("Task One/soul_foods_pink_morsel_sales.csv")


df["Date"] = pd.to_datetime(df["Date"])


df = df.sort_values("Date")


df_grouped = df.groupby(["Date", "Region"], as_index=False)["Sales"].sum()


fig = px.line(
    df_grouped,
    x="Date",
    y="Sales",
    color="Region",
    title="Pink Morsel Sales Over Time"
)


fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales ($)"
)

#price increase on 15th jan 2021
price_increase_date = pd.to_datetime("2021-01-15")
fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    yref="paper",
    line=dict(color="red", width=2, dash="dash")
)

fig.add_annotation(
    x=price_increase_date,
    y=0.9,
    yref="paper",
    text="Price Increase<br>Jan 15, 2021",
    showarrow=True,
    arrowhead=2,
    arrowcolor="red"
)

#stats calculation
df_before = df[df["Date"] < price_increase_date]
df_after = df[df["Date"] >= price_increase_date]
avg_before = df_before["Sales"].mean()
avg_after = df_after["Sales"].mean()

# Layout
app.layout = html.Div([
    html.H1("Soul Foods - Pink Morsel Sales Analysis"),
    
    html.P("Were sales higher before or after the Pink Morsel price increase on January 15th, 2021?"),
    
    dcc.Graph(figure=fig),
    
    html.H3("Summary:"),
    html.P(f"Average sales before price increase: ${avg_before:.2f}"),
    html.P(f"Average sales after price increase: ${avg_after:.2f}"),
    html.P(f"Sales were {'higher' if avg_after > avg_before else 'lower'} after the price increase.")
])


if __name__ == "__main__":
    app.run(debug=True, port=8051)
