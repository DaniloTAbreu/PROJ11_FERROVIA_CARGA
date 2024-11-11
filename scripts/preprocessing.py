import pandas as pd
import warnings

# Configurações
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

def preprocessar_dados(df):
    """Realiza o pré-processamento dos dados."""
    print("Iniciando o pré-processamento dos dados...")
    
    # Corrigir tipos de variáveis
    df['Mes_Ano'] = pd.to_datetime(df['Mes_Ano'], format='%m/%Y', errors='coerce')
    
    # Remover pontos usados como separadores de milhar e converter para float
    for col in ['TU', 'TKU']:
        if col in df.columns:
            # Converter para string para evitar erro ao usar .str
            df[col] = df[col].astype(str).str.replace('.', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    
    df['TU'] = df['TU'].astype(float)
    df['TKU'] = df['TKU'].astype(float)

    # Verificar valores únicos para diagnóstico
    print("\nValores únicos em 'Ferrovia':", df['Ferrovia'].unique())
    print("Valores únicos em 'Mercadoria_ANTT':", df['Mercadoria_ANTT'].unique())
    print("Valores únicos em 'Estacao_Origem':", df['Estacao_Origem'].unique())
    print("Valores únicos em 'UF_Origem':", df['UF_Origem'].unique())
    print("Valores únicos em 'Estacao_Destino':", df['Estacao_Destino'].unique())
    print("Valores únicos em 'UF_Destino':", df['UF_Destino'].unique())
    
    # Verificar valores nulos e duplicados
    print("\nNúmero de valores nulos por coluna:")
    print(df.isnull().sum())
    
    num_duplicatas = df.duplicated().sum()
    print(f"\nNúmero de linhas duplicadas: {num_duplicatas}")
    
    # Remover linhas duplicadas
    df = df.drop_duplicates()
    
    return df

def salvar_dados(df, caminho_pickle_final, caminho_excel_final):
    """Salva o DataFrame processado em arquivos pickle e Excel."""
    try:
        # Salvar como arquivo pickle
        df.to_pickle(caminho_pickle_final)
        print(f"DataFrame salvo em {caminho_pickle_final}")
        
        # Salvar como arquivo Excel
        df.to_excel(caminho_excel_final, index=False)
        print(f"DataFrame salvo em {caminho_excel_final}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")
        raise

def main():
    # Caminho para o arquivo pickle de entrada
    caminho_pickle = 'C:/Users/Danilo/PROJETOS/PROJETO11_FERROVIA_CARGA/data/joined/df_combinado.pkl'
    
    # Caminho para os arquivos de saída
    caminho_pickle_final = 'C:/Users/Danilo/PROJETOS/PROJETO11_FERROVIA_CARGA/data/final/df_final.pkl'
    caminho_excel_final = 'C:/Users/Danilo/PROJETOS/PROJETO11_FERROVIA_CARGA/data/final/df_final.xlsx'
    
    # Carregar os dados
    df = carregar_dados(caminho_pickle)
    
    # Processar dados
    df_processado = preprocessar_dados(df)
    
    # Salvar dados
    salvar_dados(df_processado, caminho_pickle_final, caminho_excel_final)

if __name__ == "__main__":
    main()
