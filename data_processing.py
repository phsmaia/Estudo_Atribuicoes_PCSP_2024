import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def remover_atribuicoes_comuns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica e remove atribuições (colunas) que possuam valor 1 em todas as carreiras.
    Essas atribuições são comuns a todos e não possuem valor discriminatório.
    """
    # Identifica as colunas que têm 1 em todas as linhas
    cols_all_ones = df.loc[:, (df == 1).all()].columns.tolist()
    if cols_all_ones:
        return df.drop(cols_all_ones, axis=1)
    return df

@st.cache_data(show_spinner=False)
def condensar_dataframe(df_original: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """
    Compara as colunas do dataframe e aglutina aquelas que possuem valores idênticos
    para todos os cargos. Reduz a dimensionalidade sem perda de informação estrutural.
    Retorna o DataFrame condensado e o histórico de reduções.
    """
    df_condensed = df_original.copy()
    
    # Remove colunas comuns antes de condensar, caso não tenha sido feito
    df_condensed = remover_atribuicoes_comuns(df_condensed)

    loop_keeper = 0
    historico_juncoes = []
    cont_reducoes = 0

    while loop_keeper == 0:
        loop_keeper = 1 
        columns = list(df_condensed.columns)

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)): 
                # Se as colunas são idênticas (mesmo vetor de distribuição)
                if df_condensed[columns[i]].equals(df_condensed[columns[j]]):
                    cont_reducoes += 1
                    nome_atribuicao_juntada = columns[i] + ' / ' +  columns[j]
                    historico_juncoes.append(f"Redução Nº {cont_reducoes}: ({columns[i]} / {columns[j]})")
                    
                    df_condensed = df_condensed.rename(columns={columns[i]: nome_atribuicao_juntada})
                    df_condensed = df_condensed.drop(columns[j], axis=1)
                    
                    loop_keeper = 0
                    break
            if loop_keeper == 0:
                break

    return df_condensed, historico_juncoes

@st.cache_data(show_spinner=False)
def gerar_matriz_correlacao(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera uma matriz de correlação baseada no dataframe binário.
    Cargos nas linhas e colunas serão transpostos se necessário.
    """
    # Set Carreira como index temporariamente para correlação
    df_temp = df.copy()
    if 'Carreira' in df_temp.columns:
        df_temp = df_temp.set_index('Carreira')
    
    # Garantir valores numéricos
    df_temp = df_temp.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # Correlacionar carreiras baseando-se nas atribuições
    # A correlação é feita entre as linhas (cargos), por isso transpomos (T)
    matriz_corr = df_temp.T.corr()
    return matriz_corr
