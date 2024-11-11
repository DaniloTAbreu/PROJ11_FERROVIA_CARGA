# dash_app.py
# para rodar via terminal, digite: python dash_app.py
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Carregar os dados
caminho_pickle = 'C:/Users/Danilo/PROJETOS/PROJETO11_FERROVIA_CARGA/data/final/df_final.pkl'
df = pd.read_pickle(caminho_pickle)

# Processar os dados
mercadoria_distribuicao = df.groupby('Mercadoria_ANTT').agg({'TU': 'sum'}).reset_index()
mercadoria_distribuicao.columns = ['Mercadoria', 'Volume']
mercadoria_distribuicao_sorted = mercadoria_distribuicao.sort_values(by='Volume', ascending=False)

# Limitar ao top 20 mercadorias por volume
top_20_mercadorias = mercadoria_distribuicao_sorted.head(20)

# Criar o gráfico para a distribuição das mercadorias
fig = px.bar(
    top_20_mercadorias,
    x='Mercadoria',
    y='Volume',
    title='Top 20 Mercadorias por Volume de Carga Transportada',
    labels={'Mercadoria': 'Mercadoria', 'Volume': 'Volume (Toneladas)'},
    color='Volume',  # Aqui, `color` pode ser a coluna com a qual você deseja colorir as barras
    color_continuous_scale='Viridis'  # Use uma escala de cores contínua válida
)

fig.update_layout(
    xaxis_title='Mercadoria',
    yaxis_title='Volume (Toneladas)',
    xaxis_tickangle=-45
)

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Definir o layout
app.layout = html.Div(children=[
    html.H1(children='Distribuição das Mercadorias'),
    dcc.Graph(
        id='mercadoria-distribuicao',
        figure=fig
    )
])

# Rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)

