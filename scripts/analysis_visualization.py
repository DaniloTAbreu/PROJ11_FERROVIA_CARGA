# analysis_visualization.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

# Configurações
sns.set_style('whitegrid')
warnings.filterwarnings("ignore", category=FutureWarning)

def carregar_dados(caminho_pickle):
    """Carrega o DataFrame a partir de um arquivo pickle."""
    try:
        df = pd.read_pickle(caminho_pickle)
        print("DataFrame carregado com sucesso.")
        return df
    except FileNotFoundError:
        print(f"Erro: O arquivo {caminho_pickle} não foi encontrado.")
        raise
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        raise

def visualizar_dados(df):
    """Realiza a análise visual dos dados."""
    # Explorar variáveis numéricas    
    df_num = df.select_dtypes(include=['float64'])

    # Histograma para a coluna 'TU'
    plt.figure(figsize=(10, 6))
    df_num['TU'].hist(bins=30, color='green')
    plt.xlabel('Valor')
    plt.ylabel('Frequência')
    plt.title('Histograma do TU')
    plt.show()

    # Histograma para a coluna 'TKU'
    plt.figure(figsize=(10, 6))
    df_num['TKU'].hist(bins=30, color='orange')
    plt.xlabel('Valor')
    plt.ylabel('Frequência')
    plt.title('Histograma do TKU')
    plt.show()

    # Correlação
    plt.figure(figsize=(10, 8))
    sns.heatmap(df_num.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matriz de Correlação')
    plt.show()

    # Variáveis categóricas
    df_cat = df.select_dtypes(include=['object'])

    # Contagem e gráfico para 'Ferrovia'
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Ferrovia', order=df['Ferrovia'].value_counts().index, palette='Set2')
    plt.xticks(rotation=45, ha='right')
    plt.title('Distribuição de Ferrovia')
    plt.show()

    # Contagem e gráfico para 'Mercadoria_ANTT'
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Mercadoria_ANTT', order=df['Mercadoria_ANTT'].value_counts().index, palette='Set2')
    plt.xticks(rotation=45, ha='right')
    plt.title('Distribuição de Mercadorias')
    plt.show()

    # Contagem e gráfico para 'Estacao_Origem'
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Estacao_Origem', order=df['Estacao_Origem'].value_counts().index, palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.title('Estação de Origem')
    plt.show()

    # Contagem e gráfico para 'UF_Origem'
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='UF_Origem', order=df['UF_Origem'].value_counts().index, palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.title('UF de Origem')
    plt.show()

    # Contagem e gráfico para 'Estacao_Destino'
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Estacao_Destino', order=df['Estacao_Destino'].value_counts().index, color='orange')
    plt.xticks(rotation=45, ha='right')
    plt.title('Estação de Destino')
    plt.show()

    # Contagem e gráfico para 'UF_Destino'
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='UF_Destino', order=df['UF_Destino'].value_counts().index, palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.title('UF de Destino')
    plt.show()

    # Exploração da variável 'Mes_Ano'
    df['Mes'] = df['Mes_Ano'].dt.month
    df['Ano'] = df['Mes_Ano'].dt.year

    # Mercadoria mais transportada por mês
    resultados = df.groupby(['Ano', 'Mes', 'Mercadoria_ANTT']).agg({'TU': 'sum'}).reset_index()
    resultados_mais_transportada = resultados.groupby(['Ano', 'Mes']).apply(lambda x: x.loc[x['TU'].idxmax()]).reset_index(drop=True)

    plt.figure(figsize=(12, 8))
    sns.barplot(data=resultados_mais_transportada, x='Mes', y='TU', hue='Ano', palette='Set2')
    plt.title('Mercadoria Mais Transportada por Mês')
    plt.xlabel('Mês')
    plt.ylabel('Quantidade Transportada')
    plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Ano', bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=3)
    plt.show()

    # Ano com maior transporte para cada ferrovia
    agregado = df.groupby(['Ferrovia', 'Ano']).agg({'TU': 'sum'}).reset_index()
    max_transport = agregado.loc[agregado.groupby('Ferrovia')['TU'].idxmax()]
    max_transport_sorted = max_transport.sort_values(by='TU', ascending=False)

    plt.figure(figsize=(12, 8))
    sns.barplot(data=max_transport_sorted, x='TU', y='Ferrovia', hue='Ano', palette='Set2')
    plt.title('Ano com Maior Transporte para Cada Ferrovia')
    plt.xlabel('Quantidade Transportada')
    plt.ylabel('Ferrovia')
    plt.legend(title='Ano')
    plt.show()

    # Mês/Ano com maior transporte para cada ferrovia
    agregado = df.groupby(['Ferrovia', 'Mes_Ano']).agg({'TU': 'sum'}).reset_index()
    max_transport = agregado.loc[agregado.groupby('Ferrovia')['TU'].idxmax()]
    max_transport_sorted = max_transport.sort_values(by='TU', ascending=False)

    plt.figure(figsize=(12, 8))
    sns.barplot(data=max_transport_sorted, x='TU', y='Ferrovia', hue='Mes_Ano', palette='Set2')
    plt.title('Mês/Ano com Maior Transporte para Cada Ferrovia')
    plt.xlabel('Quantidade Transportada')
    plt.ylabel('Ferrovia')
    plt.legend(title='Mês/Ano', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def main():
    # Caminho para o arquivo pickle de entrada
    caminho_pickle = 'C:/Users/Danilo/PROJETOS/PROJETO11_FERROVIA_CARGA/data/final/df_final.pkl'
    
    # Carregar os dados
    df = carregar_dados(caminho_pickle)
    
    # Realizar a visualização dos dados
    visualizar_dados(df)

if __name__ == "__main__":
    main()