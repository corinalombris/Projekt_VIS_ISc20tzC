import pandas as pd
import plotly.express as px

# Daten einlesen
data = pd.read_csv('C:\\Users\\fabie\\kDrive\\FHGR\\HS23\\VIS\\projekt\\vis_projekt\\table_1.csv', delimiter=';')

# Daten ordnen und Rangplatzierung berechnen
data['Rank'] = data['global gender parity index'].rank(ascending=False)
sorted_data = data.sort_values('global gender parity index', ascending=False)

# Auswahl Top-10 und Bottom-10 Länder
top_10_high_with_rank = sorted_data.head(10)
top_10_low_with_rank = sorted_data.tail(10)
top_bottom_20_with_rank = pd.concat([top_10_high_with_rank, top_10_low_with_rank])

# Balkendiagramm
fig = px.bar(
    top_bottom_20_with_rank, 
    y='country', 
    x='global gender parity index', 
    orientation='h', 
    text='Rank',
    title='10 höchste und 10 tiefste GGPI-Werte mit Rangplatzierung',
    color='global gender parity index',
    labels={'country': 'Land', 'global gender parity index': 'GGPI', 'Rank': 'Rang'}
)

# Layout Diagramm
fig.update_layout(
    xaxis_title='GGPI',
    yaxis_title='Land',
    showlegend=False,  # Du kannst dies anpassen, je nachdem, ob du eine Legende anzeigen möchtest oder nicht
    height=600,  # Passe die Höhe des Diagramms nach Bedarf an
    margin=dict(l=0, r=0, t=40, b=0),  # Passe die Ränder nach Bedarf an
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    bargap=0.15
)

# Textposition und Textausrichtung
fig.update_traces(textangle=0, textposition='inside')

# höchste Werte oben
fig.update_yaxes(autorange="reversed")

fig.show()