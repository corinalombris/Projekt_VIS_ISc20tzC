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

    # Aktualisiertes Balkendiagramm mit Education und Politics für jedes Land
    dcc.Graph(id='bar_chart_education_politics', figure={}),

    # Zweites Balkendiagramm mit Education und Violence für jedes Land
    dcc.Graph(id='bar_chart_education_violence', figure={}),

    # Scatter Plot mit ggpi und wei-Werten
    dcc.Graph(id='scatter_plot_wei_ggpi', figure={}),

    # Scatter Plot mit birth_rate und education-Werten
    dcc.Graph(id='scatter_plot_birth_rate_education', figure={}),

    # Scatter Plot mit birth_rate und family-Werten
    dcc.Graph(id='scatter_plot_birth_rate_family', figure={}),

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

# Funktion für die Datenfilterung
def filter_data(df, selected_countries, selected_weg, wei_slider_value):
    if 'all' in selected_countries:
        filtered_df = df[
            (df['wei'] >= wei_slider_value[0]) & (df['wei'] <= wei_slider_value[1])]
    else:
        filtered_df = df[
            (df['country'].isin(selected_countries)) & (df['wei'] >= wei_slider_value[0]) & (
                        df['wei'] <= wei_slider_value[1])]

    if 'all' not in selected_weg:
        filtered_df = filtered_df[filtered_df['weg'] == selected_weg]

    return filtered_df

# Verbinde die Plotly-Diagramme mit den Dash-Komponenten für das zweite Dashboard
@app.callback(
    [Output(component_id='country_map', component_property='figure'),
     Output(component_id='bar_chart_education_politics', component_property='figure'),
     Output(component_id='bar_chart_education_violence', component_property='figure'),
     Output(component_id='scatter_plot_wei_ggpi', component_property='figure'),
     Output(component_id='scatter_plot_birth_rate_education', component_property='figure'),
     Output(component_id='scatter_plot_birth_rate_family', component_property='figure')],
    [Input(component_id='slct_country', component_property='value'),
     Input(component_id='slct_weg', component_property='value'),
     Input(component_id='wei_slider', component_property='value'),
     Input(component_id='wei_input_min', component_property='value'),
     Input(component_id='wei_input_max', component_property='value')]
)
def update_graph(selected_countries, selected_weg, wei_slider_value, wei_input_min_value, wei_input_max_value):
    filtered_df = filter_data(df, selected_countries, selected_weg, wei_slider_value)

    # Aktualisierte Weltkarte: Farbe nach Women's Empowerment Group
    choropleth_fig = px.choropleth(
        filtered_df,
        locations='country',
        locationmode='country names',
        color='weg',
        hover_name='country',
        color_discrete_map={
            'High': 'darkblue',
            'Low': 'lightblue',
            'Upper-middle': 'orange',
            'Lower-middle': 'yellow'
        }
    )

    bar_chart_education_politics_fig = go.Figure()

    if not filtered_df.empty:
        bar_chart_education_politics_fig.add_trace(go.Bar(
            x=filtered_df['country'],
            y=filtered_df['education'],
            text=filtered_df['education'].round(2),
            name='Education'
        ))

        bar_chart_education_politics_fig.add_trace(go.Bar(
            x=filtered_df['country'],
            y=filtered_df['politics'],
            text=filtered_df['politics'].round(2),
            name='Politics'
        ))

        bar_chart_education_politics_fig.update_layout(xaxis_title='Countries', yaxis_title="Indices",
                                                       barmode='group', bargap=0.15, bargroupgap=0.1)
    else:
        bar_chart_education_politics_fig.update_layout(
            annotations=[dict(text='No data available for selected filters', showarrow=False)]
        )

    # Zusätzliches Balkendiagramm mit Education und Violence für jedes Land
    bar_chart_education_violence_fig = go.Figure()

    if not filtered_df.empty:
        bar_chart_education_violence_fig.add_trace(go.Bar(
            x=filtered_df['country'],
            y=filtered_df['education'],
            text=filtered_df['education'].round(2),
            name='Education'
        ))

        bar_chart_education_violence_fig.add_trace(go.Bar(
            x=filtered_df['country'],
            y=filtered_df['violence'],
            text=filtered_df['violence'].round(2),
            name='Violence'
        ))

        bar_chart_education_violence_fig.update_layout(xaxis_title='Countries', yaxis_title="Indices",
                                                       barmode='group', bargap=0.15, bargroupgap=0.1)
    else:
        bar_chart_education_violence_fig.update_layout(
            annotations=[dict(text='No data available for selected filters', showarrow=False)]
        )

    # Scatter Plot mit ggpi und wei-Werten
    scatter_wei_ggpi_fig = px.scatter(
        filtered_df,
        x='ggpi',
        y='wei',
        hover_name='country',
        title='Scatter Plot: GGPI vs. WEI'
    )

    # Scatter Plot mit birth_rate und education-Werten
    scatter_birth_rate_education_fig = px.scatter(
        filtered_df,
        x='birth_rate',
        y='education',
        hover_name='country',
        title='Scatter Plot: Birth Rate vs. Education'
    )

    # Scatter Plot mit birth_rate und family-Werten
    scatter_birth_rate_family_fig = px.scatter(
        filtered_df,
        x='birth_rate',
        y='family',
        hover_name='country',
        title='Scatter Plot: Birth Rate vs. Family'
    )

    return choropleth_fig, bar_chart_education_politics_fig, bar_chart_education_violence_fig, scatter_wei_ggpi_fig, scatter_birth_rate_education_fig, scatter_birth_rate_family_fig

# Startet die Dash App
if __name__ == '__main__':
    app.run_server(debug=True)
