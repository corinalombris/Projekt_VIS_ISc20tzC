# Importe
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialisierung Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Daten einlesen (CSV-File)
df = pd.read_csv('Hauptprojekt/table_2.csv', delimiter=";")
df = df.groupby(['country', 'ggpi', 'weg', 'education', 'politics', 'violence', 'birth_rate', 'family'])[['wei']].mean().reset_index()

# Liste Länder (Dropdown)
country_options = [{'label': country, 'value': country} for country in df['country'].unique()]

# Liste "Women's Empowerment Group" (Dropdown)
weg_options = [{'label': 'All', 'value': 'all'}] + [
    {"label": "High", "value": "High"},
    {"label": "Low", "value": "Low"},
    {"label": "Lower-middle", "value": "Lower-middle"},
    {"label": "Upper-middle", "value": "Upper-middle"}
]

# Layout und Inhalt overlay Filter
offcanvas = html.Div(
    [
        dbc.Button("Filter", id="open-offcanvas", n_clicks=0, style={'background-color': '#d0b3f2', 'width': '100px', 'border': 'none', 'font-size': '20px', 'margin-top': '20px', 'font-weight': 'bold', 'color': 'black', 'margin-left': '20px'}),
        dbc.Offcanvas(

            html.Div([
                # Filter Länder
                html.Label("Select Countries:"),
                dcc.Dropdown(
                    id="slct_country",
                    options=[{'label': 'Select All', 'value': 'all'}] + country_options,
                    multi=True,
                    value='all',
                    style={"margin-bottom": "10%"}
                ),

                # Filter "Women's Empowerment Group"
                html.Label("Select Women's Empowerment Group (WEG):"),
                dcc.Dropdown(
                    id="slct_weg",
                    options=weg_options,
                    multi=False,
                    value='all',
                    style={"margin-bottom": "10%"}
                ),

                # RangeSlider "Women's Empowerment Index"
                html.Label("Select Women's Empowerment Index (WEI):"),
                dcc.RangeSlider(
                    id='wei_slider',
                    min=df['wei'].min(),
                    max=df['wei'].max(),
                    step=0.1,
                    marks={i: str(i) for i in range(int(df['wei'].min()), int(df['wei'].max()) + 1)},
                    value=[df['wei'].min(), df['wei'].max()],
                    tooltip={'placement': 'bottom', 'always_visible': True},
                ),

            html.Br(), # Zeilenumbruch

                # RangeSlider GGPI
                html.Label("Select Global Gender Parity Index (GGPI):"),
                dcc.RangeSlider(
                    id='ggpi_slider',
                    min=df['ggpi'].min(),
                    max=df['ggpi'].max(),
                    step=0.1,
                    marks={i: str(i) for i in range(int(df['ggpi'].min()), int(df['ggpi'].max()) + 1)},
                    value=[df['ggpi'].min(), df['ggpi'].max()],
                    tooltip={'placement': 'bottom', 'always_visible': True},
                ),

            html.Br(), # Zeilenumbruch

            # Button für das zurücksetzen von allen Filtern
            html.Button("Reset all Filters", id="btn_reset_filters", n_clicks=0, style={'margin-top': '10px', 'background-color': 'black', 'color': 'white', 'border': 'none', 'font-size': '20px', 'font-weight': 'bold'}),
            ]),

            id="offcanvas",
            title="Filter Options",
            is_open=False,
            style={'background-color': '#d0b3f2'}
        ),
    ]
)

# Layout und Inhalt Dashboard
app.layout = html.Div(style={'background-color': 'black', 'color': 'white'},
    children=[
        html.H1("The path to equal", style={'margin-left': '20px'}),

    offcanvas,

    # Streudiagramme
    html.Div([
        dcc.Graph(id='scatter_plot_wei_ggpi', figure={}),
        dcc.Graph(id='scatter_plot_birth_rate_education', figure={}),
        dcc.Graph(id='scatter_plot_birth_rate_family', figure={}),
    ], style={'width': '50%', 'float': 'left'}),

    # Balkendiagramme und Weltkarte
    html.Div([
        dcc.Graph(id='bar_chart_education_politics', figure={}),
        dcc.Graph(id='bar_chart_education_violence', figure={}),
        dcc.Graph(id='country_map', figure={}),
    ], style={'width': '50%', 'float': 'left'}),

])

# Callback beim zurücksetzen der Filter
@app.callback(
    [Output("slct_country", "value"),
     Output("slct_weg", "value"),
     Output("wei_slider", "value"),
     Output("ggpi_slider", "value")],
    [Input("btn_reset_filters", "n_clicks")]
)

# Filter zurücksetzen
def reset_filters(n_clicks):
    return 'all', 'all', [df['wei'].min(), df['wei'].max()], [df['ggpi'].min(), df['ggpi'].max()]

# Callback Overlay
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Funktion für die Filterung der Daten
def filter_data(df, selected_countries, selected_weg, wei_slider_value, ggpi_slider_value):
    if 'all' in selected_countries:
        filtered_df = df[
            (df['wei'] >= wei_slider_value[0]) & (df['wei'] <= wei_slider_value[1]) &
            (df['ggpi'] >= ggpi_slider_value[0]) & (df['ggpi'] <= ggpi_slider_value[1])
        ]
    else:
        filtered_df = df[
            (df['country'].isin(selected_countries)) &
            (df['wei'] >= wei_slider_value[0]) & (df['wei'] <= wei_slider_value[1]) &
            (df['ggpi'] >= ggpi_slider_value[0]) & (df['ggpi'] <= ggpi_slider_value[1])
        ]

    if 'all' not in selected_weg:
        filtered_df = filtered_df[filtered_df['weg'] == selected_weg]

    return filtered_df

# Callback beim ändern der Filter
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
     Input(component_id='ggpi_slider', component_property='value')]
)


def update_graph(selected_countries, selected_weg, wei_slider_value, ggpi_slider_value):
    filtered_df = filter_data(df, selected_countries, selected_weg, wei_slider_value, ggpi_slider_value)

    # Weltkarte
    choropleth_fig = px.choropleth(
        filtered_df,
        locations='country',
        locationmode='country names',
        title='Women`s empowerment group',
        color='weg',
        hover_name='country',
        color_discrete_map={
            'none': '#D4D4D4', # Grau 
            'High': '#9400D3',  # Dunkelviolett
            'Low': '#d0b3f2', # Hellviolett
            'Upper-middle': '#134f5c', # Dunkelgrün
            'Lower-middle': '#9fc5e8' # Hellblau
        }
    )

    # Balkendiagramme
    bar_chart_education_politics_fig = go.Figure()

    if not filtered_df.empty:
        bar_chart_education_politics_fig.add_trace(go.Bar(
            x=filtered_df['country'],
            y=filtered_df['education'],
            text=filtered_df['education'].round(2),
            name='Education',
            marker=dict(color='#9400D3')  # Dunkelviolett
        ))

        bar_chart_education_politics_fig.add_trace(go.Bar(
            x=filtered_df['country'],
            y=filtered_df['politics'],
            text=filtered_df['politics'].round(2),
            name='Politics',
            marker=dict(color='#d0b3f2') # Hellviolett
        ))

        bar_chart_education_politics_fig.update_layout(xaxis_title='Countries', yaxis_title="Indices", barmode='group', bargap=0.15, bargroupgap=0.1, title='Women`s education and politics')
    
    else:
        bar_chart_education_politics_fig.update_layout(
            annotations=[dict(text='No data available for selected filters', showarrow=False)]
        )

    bar_chart_education_violence_fig = go.Figure()

    if not filtered_df.empty:
        bar_chart_education_violence_fig.add_trace(go.Bar(
            x=filtered_df['country'],
            y=filtered_df['education'],
            text=filtered_df['education'].round(2),
            name='Education',
            marker=dict(color='#9400D3'),  # Dunkelviolett
        ))

        bar_chart_education_violence_fig.add_trace(go.Bar(
            x=filtered_df['country'],
            y=filtered_df['violence'],
            text=filtered_df['violence'].round(2),
            name='Violence',
            marker=dict(color='#d0b3f2')
        ))

        bar_chart_education_violence_fig.update_layout(xaxis_title='Countries', yaxis_title="Indices", barmode='group', bargap=0.15, bargroupgap=0.1, title='Women`s education and violence')
    
    else:
        bar_chart_education_violence_fig.update_layout(
            annotations=[dict(text='No data available for selected filters', showarrow=False)]
        )

    # Streudiagramme
    scatter_wei_ggpi_fig = px.scatter(
        filtered_df,
        x='ggpi',
        y='wei',
        hover_name='country',
        title='Correlation WEI and GGPI'
    )

    scatter_wei_ggpi_fig.update_traces(marker=dict(color='#d0b3f2', size=6), selector=dict(mode='markers'))  # Hellviolett

    scatter_birth_rate_education_fig = px.scatter(
        filtered_df,
        x='birth_rate',
        y='education',
        hover_name='country',
        title='Correlation education and birth rate',
    )

    scatter_birth_rate_education_fig.update_traces(marker=dict(color='#d0b3f2', size=6), selector=dict(mode='markers'))  # Hellviolett

    scatter_birth_rate_family_fig = px.scatter(
        filtered_df,
        x='birth_rate',
        y='family',
        hover_name='country',
        title='Correlation family planning and birth rate '
    )

    scatter_birth_rate_family_fig.update_traces(marker=dict(color='#d0b3f2', size=6), selector=dict(mode='markers'))  # Dunkelviolett

    # Hintergrund der Grafiken auf schwarz wechseln
    for fig in [choropleth_fig, bar_chart_education_politics_fig, bar_chart_education_violence_fig,
                scatter_wei_ggpi_fig, scatter_birth_rate_education_fig, scatter_birth_rate_family_fig]:
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white'
        )

    return choropleth_fig, bar_chart_education_politics_fig, bar_chart_education_violence_fig, scatter_wei_ggpi_fig, scatter_birth_rate_education_fig, scatter_birth_rate_family_fig

# Startet Dash
if __name__ == '__main__':
    app.run_server(debug=True)
