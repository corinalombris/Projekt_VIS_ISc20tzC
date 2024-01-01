# Importe
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback

# Einbindung externes Stylesheet
external_stylesheets = ['style.css']

# Initialisiere die Dash-App
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Datenimport
df = pd.read_csv('table_1.csv', delimiter=";")
df = df.groupby(['country', 'ggpi', 'weg', 'education', 'politics', 'violence', 'birth_rate', 'family'])[['wei']].mean().reset_index()

# Liste mit Ländern für das Dropdown
country_options = [{'label': 'Select All', 'value': 'all'}] + [{'label': country, 'value': country} for country in df['country'].unique()]

# Layout der Dash-App
app.layout = html.Div([
    html.H1("The path to equal"),

    html.Label("Select Countries:"),  # Beschriftung für Dropdown mit Ländern
    dcc.Dropdown(
        id="slct_country",
        options=country_options,
        multi=True,  # Mehrfachauswahl möglich
        value='all',  # Als Standardwert sind alle Länder ausgewählt
        style={'width': "50%"},
    ),

    # Button Filter Länderdropdown zurücksetzen
    html.Button("Reset", id="btn_reset_country", n_clicks=0, style={'margin-top': '10px', 'margin-bottom': '30px'}),

    html.Br(), # Zeilenumbruch

    html.Label("Select Women's Empowerment Group:"),  # Beschriftung WEG Dropdown
    dcc.Dropdown(
        id="slct_weg",
        options=[  # legt die Auswahloptionen fest
            {"label": "High", "value": "High"},
            {"label": "Low", "value": "Low"},
            {"label": "Lower-middle", "value": "Lower-middle"},
            {"label": "Upper-middle", "value": "Upper-middle"}],
        multi=False,
        value="default",  # Standardwert ist leer
        style={'width': "50%"}  # Weite des Dropdowns
    ),

    # Button Filter Länderdropdown zurücksetzen
    html.Button("Reset", id="btn_reset_WEG", n_clicks=0, style={'margin-top': '10px', 'margin-bottom': '30px'}),

    html.Br(), # Zeilenumbruch

    # Schieberegler WEI
    html.Label("Select Women's Empowerment Index:"),  # Beschriftung für Schieberegler
    dcc.RangeSlider(
        id='wei_slider',
        min=df['wei'].min(),  # minimaler Wert je nach Datensatz
        max=df['wei'].max(),  # maximaler Wert je nach Datensatz
        step=0.05,  # Schritte innerhalb des Schiebereglers
        marks={i: str(i) for i in range(int(df['wei'].min()), int(df['wei'].max()) + 1)},  # Beschriftungen
        value=[df['wei'].min(), df['wei'].max()]  # Standardwerte
    ),

    ## Funktioniert noch nicht
    dcc.Input(
        id='wei_input_min',
        type='number',  # man kann nur Zahlen eingeben
        placeholder='Min wei',  # Text im Feld
        value=df['wei'].min(),  # minimaler Wert je nach Datensatz
        style={'width': '48%', 'display': 'inline-block'}
    ),

    ## Funktioniert noch nicht
    dcc.Input(
        id='wei_input_max',
        type='number',  # man kann nur Zahlen eingeben
        placeholder='Max wei',  # Text im Feld
        value=df['wei'].max(),  # maximaler Wert je nach Datensatz
        style={'width': '48%', 'display': 'inline-block', 'float': 'right'}
    ),

    html.Br(),

    # Button Filter WEI zurücksetzen
    html.Button("Reset", id="btn_reset_wei", n_clicks=0, style={'margin-top': '10px', 'margin-bottom': '30px'}),

    html.Br(),

    # Schieberegler für GGPI
    html.Label("Global Gender Parity Index:"),  # Beschriftung für Schieberegler
    dcc.RangeSlider(
        id='ggpi_slider',
        min=df['ggpi'].min(),  # minimaler Wert je nach Datensatz
        max=df['ggpi'].max(),  # maximaler Wert je nach Datensatz
        step=0.05,  # Schritte innerhalb des Schiebereglers
        marks={i: str(i) for i in range(int(df['ggpi'].min()), int(df['ggpi'].max()) + 1)},  # Beschriftungen
        value=[df['ggpi'].min(), df['ggpi'].max()]  # Standardwerte
    ),

    ## Funktioniert noch nicht
    dcc.Input(
        id='ggpi_input_min',
        type='number',  # man kann nur Zahlen eingeben
        placeholder='Min ggpi',  # Text im Feld
        value=df['ggpi'].min(),  # minimaler Wert je nach Datensatz
        style={'width': '48%', 'display': 'inline-block'}
    ),

    ## Funktioniert noch nicht
    dcc.Input(
        id='ggpi_input_max',
        type='number',  # man kann nur Zahlen eingeben
        placeholder='Max ggpi',  # Text im Feld
        value=df['ggpi'].max(),  # maximaler Wert je nach Datensatz
        style={'width': '48%', 'display': 'inline-block', 'float': 'right'}
    ),

    html.Br(),

    # Button Filter GGPI zurücksetzen
    html.Button("Reset", id="btn_reset_ggpi", n_clicks=0, style={'margin-top': '10px', 'margin-bottom': '30px'}),

    html.Br(),

    # Button alle Filter zurücksetzen
    html.Button("Reset all Filters", id="btn_reset_filters", n_clicks=0, style={'margin-top': '10px'}),

    dcc.Graph(id='country_map', figure={}),
    dcc.Graph(id='scatterplot', figure={}),
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
    # Standardwerte für die Filter zurückgeben
    return 'all', 'default', [df['wei'].min(), df['wei'].max()], df['wei'].min(), df['wei'].max(), [df['ggpi'].min(), df['ggpi'].max()], df['ggpi'].min(), df['ggpi'].max()


# Verbinde die Plotly-Diagramme mit den Dash-Komponenten
@app.callback(
    [Output(component_id='country_map', component_property='figure'),
     Output(component_id='scatterplot', component_property='figure')],
    [Input(component_id='slct_country', component_property='value'),
     Input(component_id='slct_weg', component_property='value'),
     Input(component_id='wei_slider', component_property='value'),
     Input(component_id='wei_input_min', component_property='value'),
     Input(component_id='wei_input_max', component_property='value')]
)
def update_graph(selected_countries, selected_weg, wei_slider_value, wei_input_min_value, wei_input_max_value):
    # Filtert den Datensatz je nach Auswahl
    if 'all' in selected_countries:
        filtered_df = df[
            (df['weg'] == selected_weg) & (df['wei'] >= wei_slider_value[0]) & (df['wei'] <= wei_slider_value[1])]
    else:
        filtered_df = df[
            (df['country'].isin(selected_countries)) & (df['weg'] == selected_weg) & (df['wei'] >= wei_slider_value[0]) & (
                        df['wei'] <= wei_slider_value[1])]

    # Weltkarte
    choropleth_fig = px.choropleth(
        filtered_df,
        locations='country',
        locationmode='country names',
        color='wei',
        hover_name='country',  # Zeige Ländernamen beim Überfahren mit der Maus
    )

    # Scatterplot
    scatterplot_fig = px.scatter(
        df,
        x='ggpi',
        y='wei',
        hover_data=['country'],
    )

    # Gibt aktualisierte Diagramme aus
    return choropleth_fig, scatterplot_fig


# Startet die Dash App
if __name__ == '__main__':
    app.run_server(debug=True)
