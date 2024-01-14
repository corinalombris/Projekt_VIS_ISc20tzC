# Importe
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback

# Einbindung externes Stylesheet
external_stylesheets = ['style.css']

# Initialisiere die Dash-App
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Datenimport für das zweite Dashboard
df = pd.read_csv('Hauptprojekt/table_1.csv', delimiter=";")
df = df.groupby(['country', 'ggpi', 'weg', 'education', 'politics', 'violence', 'birth_rate', 'family'])[['wei']].mean().reset_index()

# Liste mit Ländern für das Dropdown
country_options = [{'label': country, 'value': country} for country in df['country'].unique()]

# Liste mit Women's Empowerment Group für das Dropdown
weg_options = [{'label': 'All', 'value': 'all'}] + [
    {"label": "High", "value": "High"},
    {"label": "Low", "value": "Low"},
    {"label": "Lower-middle", "value": "Lower-middle"},
    {"label": "Upper-middle", "value": "Upper-middle"}
]

# Layout der Dash-App
app.layout = html.Div([
    html.H1("The path to equal"),

    html.Label("Select Countries:"),
    dcc.Dropdown(
        id="slct_country",
        options=[{'label': 'Select All', 'value': 'all'}] + country_options,
        multi=True,
        value='all',
        style={'width': "50%"},
    ),

    html.Button("Reset", id="btn_reset_country", n_clicks=0, style={'margin-top': '10px', 'margin-bottom': '30px'}),

    html.Br(),

    html.Label("Select Women's Empowerment Group:"),
    dcc.Dropdown(
        id="slct_weg",
        options=weg_options,
        multi=False,
        value='all',
        style={'width': "50%"}
    ),

    html.Button("Reset", id="btn_reset_WEG", n_clicks=0, style={'margin-top': '10px', 'margin-bottom': '30px'}),

    html.Br(),

    html.Label("Select Women's Empowerment Index:"),
    dcc.RangeSlider(
        id='wei_slider',
        min=df['wei'].min(),
        max=df['wei'].max(),
        step=0.05,
        marks={i: str(i) for i in range(int(df['wei'].min()), int(df['wei'].max()) + 1)},
        value=[df['wei'].min(), df['wei'].max()]
    ),

    dcc.Input(
        id='wei_input_min',
        type='number',
        placeholder='Min wei',
        value=df['wei'].min(),
        style={'width': '48%', 'display': 'inline-block'}
    ),

    dcc.Input(
        id='wei_input_max',
        type='number',
        placeholder='Max wei',
        value=df['wei'].max(),
        style={'width': '48%', 'display': 'inline-block', 'float': 'right'}
    ),

    html.Br(),

    html.Button("Reset", id="btn_reset_wei", n_clicks=0, style={'margin-top': '10px', 'margin-bottom': '30px'}),

    html.Br(),

    html.Label("Global Gender Parity Index:"),
    dcc.RangeSlider(
        id='ggpi_slider',
        min=df['ggpi'].min(),
        max=df['ggpi'].max(),
        step=0.05,
        marks={i: str(i) for i in range(int(df['ggpi'].min()), int(df['ggpi'].max()) + 1)},
        value=[df['ggpi'].min(), df['ggpi'].max()]
    ),

    dcc.Input(
        id='ggpi_input_min',
        type='number',
        placeholder='Min ggpi',
        value=df['ggpi'].min(),
        style={'width': '48%', 'display': 'inline-block'}
    ),

    dcc.Input(
        id='ggpi_input_max',
        type='number',
        placeholder='Max ggpi',
        value=df['ggpi'].max(),
        style={'width': '48%', 'display': 'inline-block', 'float': 'right'}
    ),

    html.Br(),

    html.Button("Reset", id="btn_reset_ggpi", n_clicks=0, style={'margin-top': '10px', 'margin-bottom': '30px'}),

    html.Br(),

    html.Button("Reset all Filters", id="btn_reset_filters", n_clicks=0, style={'margin-top': '10px'}),

    dcc.Graph(id='country_map', figure={}),

    # Aktualisiertes Balkendiagramm mit zwei Balken für jedes Land
    dcc.Graph(id='bar_chart', figure={  
        'data': [
            {'x': df['country'],
             'y': [df[(df['country'] == country) & (df['weg'] == 'High')]['wei'].values[0],
                   df[(df['country'] == country) & (df['weg'] == 'High')]['ggpi'].values[0]] if not df[(df['country'] == country) & (df['weg'] == 'High')].empty and ('all' == 'all' or df[(df['country'] == country) & (df['weg'] == 'High')]['weg'].values[0] == 'all') else [0, 0],
             'name': 'High',
             'type': 'bar'} for country in df['country'].unique()
        ] + [
            {'x': df['country'],
             'y': [df[(df['country'] == country) & (df['weg'] == 'Low')]['wei'].values[0],
                   df[(df['country'] == country) & (df['weg'] == 'Low')]['ggpi'].values[0]] if not df[(df['country'] == country) & (df['weg'] == 'Low')].empty and ('all' == 'all' or df[(df['country'] == country) & (df['weg'] == 'Low')]['weg'].values[0] == 'all') else [0, 0],
             'name': 'Low',
             'type': 'bar'} for country in df['country'].unique()
        ] + [
            {'x': df['country'],
             'y': [df[(df['country'] == country) & (df['weg'] == 'Lower-middle')]['wei'].values[0],
                   df[(df['country'] == country) & (df['weg'] == 'Lower-middle')]['ggpi'].values[0]] if not df[(df['country'] == country) & (df['weg'] == 'Lower-middle')].empty and ('all' == 'all' or df[(df['country'] == country) & (df['weg'] == 'Lower-middle')]['weg'].values[0] == 'all') else [0, 0],
             'name': 'Lower-middle',
             'type': 'bar'} for country in df['country'].unique()
        ] + [
            {'x': df['country'],
             'y': [df[(df['country'] == country) & (df['weg'] == 'Upper-middle')]['wei'].values[0],
                   df[(df['country'] == country) & (df['weg'] == 'Upper-middle')]['ggpi'].values[0]] if not df[(df['country'] == country) & (df['weg'] == 'Upper-middle')].empty and ('all' == 'all' or df[(df['country'] == country) & (df['weg'] == 'Upper-middle')]['weg'].values[0] == 'all') else [0, 0],
             'name': 'Upper-middle',
             'type': 'bar'} for country in df['country'].unique()
        ],
        'layout': {
            'xaxis': {'title': 'Countries'},
            'yaxis': {'title': 'Index Values'},
            'barmode': 'group',
            'title': "Women's Empowerment and GGPI by Country"
        }
    }),
])

# Callback für das Zurücksetzen der Filter
@app.callback(
    [Output("slct_country", "value"),
     Output("slct_weg", "value"),
     Output("wei_slider", "value"),
     Output("wei_input_min", "value"),
     Output("wei_input_max", "value"),
     Output("ggpi_slider", "value"),
     Output("ggpi_input_min", "value"),
     Output("ggpi_input_max", "value")],
    [Input("btn_reset_filters", "n_clicks")]
)
def reset_filters(n_clicks):
    return 'all', 'all', [df['wei'].min(), df['wei'].max()], df['wei'].min(), df['wei'].max(), [df['ggpi'].min(), df['ggpi'].max()], df['ggpi'].min(), df['ggpi'].max()

# Verbinde die Plotly-Diagramme mit den Dash-Komponenten für das zweite Dashboard
@app.callback(
    [Output(component_id='country_map', component_property='figure'),
     Output(component_id='bar_chart', component_property='figure')],
    [Input(component_id='slct_country', component_property='value'),
     Input(component_id='slct_weg', component_property='value'),
     Input(component_id='wei_slider', component_property='value'),
     Input(component_id='wei_input_min', component_property='value'),
     Input(component_id='wei_input_max', component_property='value')]
)
def update_graph(selected_countries, selected_weg, wei_slider_value, wei_input_min_value, wei_input_max_value):
    if 'all' in selected_countries:
        filtered_df = df[
            (df['wei'] >= wei_slider_value[0]) & (df['wei'] <= wei_slider_value[1])]
    else:
        filtered_df = df[
            (df['country'].isin(selected_countries)) & (df['wei'] >= wei_slider_value[0]) & (
                        df['wei'] <= wei_slider_value[1])]

    choropleth_fig = px.choropleth(
        filtered_df,
        locations='country',
        locationmode='country names',
        color='wei',
        hover_name='country',
    )

    bar_chart_fig = go.Figure()

    if not filtered_df.empty:
        for weg_value in weg_options:
            if 'all' in selected_weg or weg_value['value'] == selected_weg:
                bar_chart_fig.add_trace(go.Bar(
                    x=filtered_df['country'],
                    y=filtered_df[filtered_df['weg'] == weg_value['value']]['wei'],
                    text=filtered_df[filtered_df['weg'] == weg_value['value']]['wei'].round(2),
                    name=weg_value['label']
                ))

        bar_chart_fig.update_layout(xaxis_title='Countries', yaxis_title="Women's Empowerment Index", barmode='stack')
    else:
        bar_chart_fig.update_layout(
            annotations=[dict(text='No data available for selected filters', showarrow=False)]
        )

    return choropleth_fig, bar_chart_fig

# Startet die Dash App
if __name__ == '__main__':
    app.run_server(debug=True)
