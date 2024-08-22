
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff


df = pd.read_csv('gyroscope1.csv')


app = Dash()


app.layout = [
    html.Div(children='Week 6 Gyroscope App with Data, Graph, and Controls'),
    html.Hr(),
    dcc.Dropdown(options=['Line Graph', 'Scatter Plot', 'Distribution Plot', 'Area Plot'], value='Timestamp', id='controls-and-dropdown-item', clearable=False),
    dcc.Dropdown(options=['X', 'Y', 'Z'], value = ['X', 'Y', 'Z'], id='controls-and-dropdown-variable', clearable=False, multi=True),
    html.Div([html.Label('Number of Samples to Display:'),
    dcc.Input(id='sample-size-input', type='number', value=376, min=1)]),
    html.Div([html.Button('Previous', id='prev-button', n_clicks=0),html.Button('Next', id='next-button', n_clicks=0),]),
    dcc.Store(id='start-n', data=0), 
    dash_table.DataTable(data=df.to_dict('records'), page_size=5),
    dcc.Graph(figure={}, id='controls-and-graph'),
    dash_table.DataTable(id='summary', page_size=5)
]

@callback(
    Output('start-n', 'data'),
    [Input('prev-button', 'n_clicks'), Input('next-button', 'n_clicks')],
    [State('start-n', 'data'), State('sample-size-input', 'value')]
)

def update_start_n(back_n, next_n, current_start_n, n_size):
    total_n = len(df)
    if back_n > 0:
        new_start_n = max(current_start_n - n_size, 0)
    elif next_n > 0:
        new_start_n = min(current_start_n + n_size, total_n - n_size)
    else:
        new_start_n = current_start_n
    
    return new_start_n
    
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-dropdown-item', component_property='value'),
    Input(component_id='controls-and-dropdown-variable', component_property='value'),
    Input('sample-size-input', 'value'),
    Input('start-n', 'data')
)
def update_graph(graph_chosen, var_chosen, n_size, start_n):
    fig = {}
    if n_size is None:
        n_size = 376
    end_n = start_n + n_size
    df_n = df.iloc[start_n:end_n]
    if graph_chosen == 'Line Graph':
        fig = px.line(df_n, x='Timestamp', y=var_chosen)
    elif graph_chosen == 'Scatter Plot':
        fig = px.scatter(df_n, x='Timestamp', y=var_chosen)
    elif graph_chosen == 'Distribution Plot':
        fig = ff.create_distplot([df_n[variable] for variable in var_chosen], group_labels=var_chosen, show_hist=False)
    elif graph_chosen == 'Area Plot':
        fig = px.area(df_n, x='Timestamp', y=['X', 'Y', 'Z'])
    return fig
    
@callback(
    Output('summary', 'data'),
    [Input(component_id='controls-and-dropdown-variable', component_property='value'),
     Input('sample-size-input', 'value'),
     Input('start-n', 'data')]
)

def update_table(var_chosen, n_size, start_n):
    if n_size is None:
        n_size = 376
    
    end_n = start_n + n_size
    df_n = df.iloc[start_n:end_n]
    
    summary = {}
    for variable in var_chosen:
        summary[variable] = {
            'Mean': np.mean(df_n[variable]),
            'Median': np.median(df_n[variable]),
            'Min': np.min(df_n[variable]),
            'Max': np.max(df_n[variable])
        }
    
    summary_df = pd.DataFrame(summary).T.reset_index().rename(columns={'index': 'Variable'})
    
    return summary_df.to_dict('records')


if __name__ == '__main__':
    app.run(debug=True, jupyter_mode="tab")

