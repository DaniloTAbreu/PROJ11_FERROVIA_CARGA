# streamlit_app.py
# para rodar: streamlit run streamlit_app.py --server.port 8502
# abrir http:localhost/8502, se não abrir automaticamente
import streamlit as st
import pandas as pd
import plotly.express as px

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
    color='Volume',  # Colorir as barras conforme o volume
    color_continuous_scale='Viridis'  # Use uma escala de cores contínua válida
)

fig.update_layout(
    xaxis_title='Mercadoria',
    yaxis_title='Volume (Toneladas)',
    xaxis_tickangle=-45
)

# Configurar o aplicativo Streamlit
st.set_page_config(page_title="Distribuição das Mercadorias", layout="wide")

# Título da página
st.title("Distribuição das Mercadorias")

# Exibir o gráfico
st.plotly_chart(fig)
