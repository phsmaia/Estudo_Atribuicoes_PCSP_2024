import pandas as pd
import streamlit as st
import os

@st.cache_data(show_spinner=False)
def load_csv_data(filepath: str) -> pd.DataFrame:
    """
    Carrega dados de um arquivo CSV, utilizando os padrões de encoding e separador do projeto.
    Utiliza cache do Streamlit para evitar re-leitura de disco em cada iteração.
    """
    if not os.path.exists(filepath):
        st.error(f"Arquivo não encontrado: {filepath}")
        return pd.DataFrame()
        
    try:
        return pd.read_csv(filepath, encoding='iso-8859-1', sep=';')
    except Exception as e:
        st.error(f"Erro ao ler o arquivo {filepath}: {e}")
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def get_all_datasets(base_dir: str = ".") -> dict:
    """
    Carrega os principais datasets mapeados no projeto.
    Retorna um dicionário com os DataFrames.
    """
    datasets = {
        "editais": load_csv_data(os.path.join(base_dir, "Atribuicoes_Carreiras_Editais.CSV")),
        "atual_sem_correcao": load_csv_data(os.path.join(base_dir, "01 - Atrib Atual No Cor.CSV")),
        "atual_com_correcao": load_csv_data(os.path.join(base_dir, "02 - Atrib Atual With Cor.CSV")),
        "lonpc_sem_correcao": load_csv_data(os.path.join(base_dir, "03 - Atrib LONPC No Cor.CSV")),
        "lonpc_com_correcao": load_csv_data(os.path.join(base_dir, "04 - Atrib LONPC With Cor.CSV")),
        "reestruturacao": load_csv_data(os.path.join(base_dir, "05 - Atrib Rest Rem Pericia.CSV"))
    }
    return datasets
