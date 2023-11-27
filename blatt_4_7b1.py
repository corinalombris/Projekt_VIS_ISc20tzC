import pandas as pd
import plotly.express as px 

# Daten einlesen
data = pd.read_csv('https://github.com/corinalombris/Projekt_VIS_ISc20tzC/blob/main/table_1.csv', delimiter=';')

# Berechnung Korrelationswert
correlation = data['women empowerment index'].corr(data['global gender parity index'])
print(f'Korrelation zwischen WEI und GGPI: {correlation:.2f}')

# Scatter
fig = px.scatter(
    data,
    x='women empowerment index', 
    y='global gender parity index', 
    title=f'Korrelation zwischen WEI und GGPI:{correlation:.2f}', 
    trendline='ols')

fig.show()
