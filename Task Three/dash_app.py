from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd


app = Dash(__name__)


df = pd.read_csv("Task Two/soul_foods_pink_morsel_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")


price_increase_date = pd.to_datetime("2021-01-15")


app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Soul Foods - Pink Morsel Sales Analysis", 
                style={
                    'textAlign': 'center', 
                    'color': '#2c3e50',
                    'marginBottom': '10px'
                }),
        html.P("Were sales higher before or after the Pink Morsel price increase on January 15th, 2021?",
               style={
                   'textAlign': 'center',
                   'fontSize': '16px',
                   'color': '#7f8c8d',
                   'fontStyle': 'italic'
               })
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'marginBottom': '20px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }),
    
   
    html.Div([
        html.Label("Select Region:", 
                   style={
                       'fontSize': '16px', 
                       'fontWeight': 'bold',
                       'marginBottom': '10px',
                       'display': 'block'
                   }),
        dcc.RadioItems(
            id='region-selector',
            options=[
                {'label': ' All Regions', 'value': 'all'},
                {'label': ' North', 'value': 'north'},
                {'label': ' East', 'value': 'east'},
                {'label': ' South', 'value': 'south'},
                {'label': ' West', 'value': 'west'}
            ],
            value='all',
            style={'display': 'flex', 'gap': '20px'},
            inputStyle={'marginRight': '5px'}
        )
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'marginBottom': '20px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }),
    
 
    html.Div([
        dcc.Graph(id='sales-chart')
    ], style={
        'backgroundColor': 'white',
        'padding': '15px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'marginBottom': '20px'
    }),
    
  
    html.Div([
        html.H3("Summary", style={'color': '#2c3e50'}),
        html.Div(id='summary-content')
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })
    
], style={
    'maxWidth': '1000px',
    'margin': '0 auto',
    'padding': '20px',
    'backgroundColor': '#f5f5f5',
    'fontFamily': 'Arial, sans-serif'
})


@callback(
    [Output('sales-chart', 'figure'),
     Output('summary-content', 'children')],
    [Input('region-selector', 'value')]
)
def update_chart(selected_region):
    if selected_region == 'all':
       
        chart_data = df.groupby(["Date", "Region"], as_index=False)["Sales"].sum()
        fig = px.line(
            chart_data,
            x="Date",
            y="Sales",
            color="Region",
            title="Pink Morsel Sales - All Regions"
        )
    else:
        
        chart_data = df[df["Region"] == selected_region]
        fig = px.line(
            chart_data,
            x="Date",
            y="Sales",
            title=f"Pink Morsel Sales - {selected_region.title()} Region"
        )
        fig.update_traces(line_color='#3498db', line_width=3)
    
  
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        plot_bgcolor='white',
        title=dict(x=0.5, font=dict(size=16))
    )
    
    
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
    
    
    if selected_region == 'all':
        summary_data = df
        region_text = "All Regions"
    else:
        summary_data = df[df["Region"] == selected_region]
        region_text = f"{selected_region.title()} Region"
    
    df_before = summary_data[summary_data["Date"] < price_increase_date]
    df_after = summary_data[summary_data["Date"] >= price_increase_date]
    
    avg_before = df_before["Sales"].mean()
    avg_after = df_after["Sales"].mean()
    
   
    summary = [
        html.P(f"Region: {region_text}", style={'fontSize': '16px', 'fontWeight': 'bold'}),
        html.P(f"Average sales before price increase: ${avg_before:.2f}", style={'margin': '5px 0'}),
        html.P(f"Average sales after price increase: ${avg_after:.2f}", style={'margin': '5px 0'}),
        html.P(
            f"Sales were {'higher' if avg_after > avg_before else 'lower'} after the price increase.",
            style={
                'fontWeight': 'bold',
                'color': '#27ae60' if avg_after > avg_before else '#e74c3c',
                'fontSize': '16px',
                'marginTop': '15px'
            }
        )
    ]
    
    return fig, summary

if __name__ == "__main__":
    app.run(debug=True, port=8053)

