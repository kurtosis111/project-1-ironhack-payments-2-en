import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

from data_loader import load_data
from metrics import calc_metric

cash_req, fee = load_data(False)
metrics = calc_metric()

app = dash.Dash(__name__)
app.title = "Ironhack Payments Dashboard"
app.layout = html.Div([
    html.H1("Ironhack Payments Dashboard", style={'textAlign': 'center'}),

    html.Label("Select a metric"),

    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Frequency of Service Charge', 'value': 'frequency'},
            {'label': 'Incidence Rate of Direct Debit Rejection', 'value': 'incidence_rate'},
            {'label': 'Total Revenue', 'value': 'revenue'},
            {'label': 'Revenue Source', 'value': 'revenue_source'},
            {'label': 'Cash Request Amount', 'value': 'request_amount'},
            {'label': 'Outstanding Days', 'value': 'outstanding_days'}
        ],
        value='frequency',
        clearable=False
    ),
    
    dcc.Graph(id='metric-graph'),

])  

@app.callback(
    Output('metric-graph', 'figure'),
    Input('metric-dropdown', 'value')
)
def update_graph(selected_metric):
    df0 = metrics[selected_metric]
    df = pd.DataFrame(df0)
    df.reset_index(drop=False, inplace=True)
    if selected_metric == 'revenue_source':
        df.drop('created_year', axis=1, inplace=True)
        fig = px.bar(df, x = "created_month", y = ["incident", 'instant_payment', 'postpone'])
    else:
        df['year'] = df['created_year'].astype('category') 
        fig = px.line(df, x='created_month', y=df.columns[1:], color='year', title=f"{selected_metric.replace('_', ' ').title()} Over Time")

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title=selected_metric.replace('_', ' ').title(),
        legend_title='Year',
        template='plotly_white'
    )   

    return fig

if __name__ == '__main__':
    app.run(debug=True)
    # %%

