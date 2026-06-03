import psycopg2
import streamlit as st
import os

def get_connection():
    """
    Estabelece conexao com o banco de dados PostgreSQL.
    Tenta primeiro ler a URL completa (DATABASE_URL), 
    se falhar, tenta ler as credenciais individuais.
    Retorna None se falhar.
    """
    try:
        db_url = st.secrets.get("DATABASE_URL", os.environ.get("DATABASE_URL"))
        if db_url:
            return psycopg2.connect(db_url)
            
        host = st.secrets.get("DB_HOST", os.environ.get("DB_HOST", "localhost"))
        dbname = st.secrets.get("DB_NAME", os.environ.get("DB_NAME", "postgres"))
        user = st.secrets.get("DB_USER", os.environ.get("DB_USER", "postgres"))
        password = st.secrets.get("DB_PASSWORD", os.environ.get("DB_PASSWORD", ""))
        port = st.secrets.get("DB_PORT", os.environ.get("DB_PORT", "5432"))
        
        return psycopg2.connect(
            host=host, 
            database=dbname, 
            user=user, 
            password=password, 
            port=port
        )
    except Exception as e:
        print(f"Erro ao conectar no banco de dados PostgreSQL: {e}")
        return None
