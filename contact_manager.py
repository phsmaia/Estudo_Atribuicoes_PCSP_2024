import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import os
from db import get_connection

def init_db():
    """Inicializa o banco de dados PostgreSQL de contatos."""
    conn = get_connection()
    if not conn:
        return
        
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_messages (
                id SERIAL PRIMARY KEY,
                timestamp TEXT,
                nome TEXT,
                email TEXT,
                instituicao TEXT,
                funcao TEXT,
                assunto TEXT,
                mensagem TEXT
            )
        ''')
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Erro ao inicializar o BD de contatos: {e}")
    finally:
        conn.close()

def save_contact_message(nome, email, instituicao, funcao, assunto, mensagem):
    """Salva a mensagem de contato no banco de dados local."""
    conn = get_connection()
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        agora = datetime.datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO contact_messages (timestamp, nome, email, instituicao, funcao, assunto, mensagem)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (agora, nome, email, instituicao, funcao, assunto, mensagem))
        
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao salvar mensagem no BD: {e}")
        return False
    finally:
        conn.close()

def send_contact_email(nome, email, instituicao, funcao, assunto, mensagem):
    """
    Tenta enviar o e-mail usando SMTP.
    Exige as chaves SMTP_USER e SMTP_PASSWORD configuradas no st.secrets ou os.environ.
    """
    # Tenta recuperar as credenciais de st.secrets primeiro, e depois de variáveis de ambiente
    try:
        smtp_user = st.secrets.get("SMTP_USER", os.environ.get("SMTP_USER"))
        smtp_pass = st.secrets.get("SMTP_PASSWORD", os.environ.get("SMTP_PASSWORD"))
    except FileNotFoundError:
        smtp_user = os.environ.get("SMTP_USER")
        smtp_pass = os.environ.get("SMTP_PASSWORD")
        
    if not smtp_user or not smtp_pass:
        # Se não houver credenciais, não vamos gerar exceção fatal para não quebrar a aplicação.
        # Retornamos False para indicar que o e-mail não foi enviado, 
        # mas os dados ainda estão seguros no banco de dados.
        return False, "Credenciais de e-mail (SMTP_USER / SMTP_PASSWORD) não configuradas no sistema."

    destinatario = "maia.phs@gmail.com"
    
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = destinatario
    msg['Subject'] = f"Novo Contato (App PCSP): {assunto}"
    
    corpo_email = f"""
Você recebeu uma nova mensagem através da aplicação Estudo de Atribuições PCSP.

DADOS DO REMETENTE:
-------------------
Nome: {nome}
E-mail: {email}
Instituição: {instituicao}
Função: {funcao}

MENSAGEM:
-------------------
{mensagem}

-------------------
Este é um e-mail automático gerado pelo sistema.
"""
    
    msg.attach(MIMEText(corpo_email, 'plain'))
    
    try:
        # Usando Gmail como servidor padrão
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        return True, "E-mail enviado com sucesso."
    except Exception as e:
        return False, f"Erro ao conectar com o servidor SMTP: {str(e)}"

# Garante que o banco de dados exista ao carregar o módulo
init_db()
