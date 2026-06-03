import hashlib
from datetime import datetime
import os
import streamlit as st
from db import get_connection

def init_db():
    """Inicializa as tabelas do banco de dados PostgreSQL para log silencioso."""
    conn = get_connection()
    if not conn:
        return
        
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS visits
                     (id SERIAL PRIMARY KEY, 
                      timestamp TEXT, 
                      hashed_ip TEXT, 
                      cenario TEXT,
                      session_id TEXT)''')
        conn.commit()
        c.close()
    except Exception as e:
        print(f"Erro ao inicializar DB logger: {e}")
    finally:
        conn.close()

def _get_client_ip():
    """Tenta capturar o IP do cliente através dos headers do Streamlit."""
    try:
        from streamlit import context
        # Em versões recentes (>=1.37) do Streamlit, os headers estão disponíveis
        if hasattr(context, "headers") and context.headers:
            headers = context.headers
            # X-Forwarded-For pega o IP original através de proxies/Nginx
            if "X-Forwarded-For" in headers:
                return headers["X-Forwarded-For"].split(",")[0].strip()
            if "Remote-Addr" in headers:
                return headers["Remote-Addr"]
    except Exception:
        pass
    
    return "0.0.0.0"

def log_visit(cenario):
    """
    Registra a visita silenciosamente no banco de dados.
    Para adequação à LGPD, o IP é convertido em um hash irreversível (SHA-256),
    garantindo a métrica de usuários únicos sem armazenar o dado pessoal.
    """
    # Para não sobrecarregar o DB em cada refresh de interface, usamos session_state
    if "visit_logged" not in st.session_state:
        ip = _get_client_ip()
        
        # Salt simples e fixo para hashing
        salt = "pcsp_2024_"
        hashed_ip = hashlib.sha256((salt + ip).encode('utf-8')).hexdigest()
        
        # Pega ID temporário da sessão se possível para métricas de re-navegação (opcional)
        try:
            from streamlit.runtime.scriptrunner import get_script_run_ctx
            ctx = get_script_run_ctx()
            session_id = ctx.session_id if ctx else "unknown"
        except Exception:
            session_id = "unknown"
        
        conn = get_connection()
        if not conn:
            return
            
        try:
            c = conn.cursor()
            c.execute("INSERT INTO visits (timestamp, hashed_ip, cenario, session_id) VALUES (%s, %s, %s, %s)", 
                      (datetime.now().isoformat(), hashed_ip, cenario, session_id))
            conn.commit()
            c.close()
            st.session_state["visit_logged"] = True
        except Exception as e:
            # Em caso de falha no banco de dados, morre silenciosamente sem quebrar o app
            pass
        finally:
            conn.close()
