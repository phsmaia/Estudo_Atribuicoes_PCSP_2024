import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import data_loader
import data_processing
import visualizations
import logger
import os

try:
    df_conv = pd.read_csv('Tabela_Conversao_Cargos.CSV', sep=';', encoding='iso-8859-1')
    df_conv.to_json('csv_dump.json', orient='records', force_ascii=False)
except Exception as e:
    with open('erro.txt', 'w') as f: f.write(str(e))
    pass

# Iniciar o banco de dados de log
logger.init_db()

# Configuração Básica da Página
st.set_page_config(page_title="Estudo de Atribuições PCSP", layout="wide")

# --- RODAPÉ FLUTUANTE DE CONTATOS E REFERÊNCIAS (Injeção Direta no DOM) ---
components.html("""
<script>
    // Tenta remover o footer antigo caso o Streamlit faça um re-run da tela
    const oldFooter = window.parent.document.getElementById('hud-floating-footer');
    if (oldFooter) {
        oldFooter.remove();
    }

    // Constrói o HUD puro no root do navegador, imune aos containers do Streamlit
    const footer = window.parent.document.createElement('div');
    footer.id = 'hud-floating-footer';
    footer.innerHTML = `
        <style>
        #hud-floating-footer {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: rgba(14, 17, 23, 0.90);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 30px;
            padding: 0 20px;
            z-index: 999999;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            width: 240px;
            height: 50px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            font-family: sans-serif;
        }
        #hud-floating-footer:hover {
            width: 320px;
            height: max-content;
            border-radius: 15px;
            padding: 20px;
            align-items: flex-start;
        }
        .hud-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 50px;
            cursor: pointer;
            flex-shrink: 0;
            color: #E0E0E0;
            font-weight: bold;
            font-size: 0.95rem;
            gap: 8px;
        }
        #hud-floating-footer:hover .hud-icon {
            display: none;
        }
        .hud-content {
            opacity: 0;
            transition: opacity 0.3s ease;
            transition-delay: 0.1s;
            display: none;
            width: 100%;
        }
        #hud-floating-footer:hover .hud-content {
            opacity: 1;
            display: block;
        }
        .hud-content a {
            color: #4da6ff;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 0.95rem;
            padding: 6px;
            border-radius: 5px;
            transition: background 0.2s;
        }
        .hud-content a:hover {
            text-decoration: underline;
            background: rgba(255,255,255,0.05);
        }
        .hud-content h4 {
            margin: 0 0 10px 0;
            color: #E0E0E0;
            font-size: 1rem;
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
        }
        </style>
        
        <div class="hud-icon">
            <span style="font-size: 1.2rem;">💬</span> Referências e Contato
        </div>
        <div class="hud-content">
            <h4>Referências do Estudo</h4>
            <span style="font-size: 0.75rem; color: #A0A0A0; display: block; margin: -5px 0 8px 0; font-style: italic;">Material para consulta, teste e checagem</span>
            <a href="https://github.com/phsmaia/Estudo_Atribuicoes_PCSP_2024" target="_blank">💻 Repositório GitHub</a>
            <a href="https://periodicos.pf.gov.br/index.php/RBCP/pt_BR/article/view/4693" target="_blank">📜 Artigo Científico</a>
            <a href="https://zenodo.org/records/14284483" target="_blank">📊 Dados Brutos (Zenodo)</a>
            <h4 style="margin-top: 15px;">Fale com o Autor</h4>
            <span style="font-size: 0.75rem; color: #A0A0A0; display: block; margin: -5px 0 8px 0; font-style: italic;">Críticas, sugestões, elogios ou outros</span>
            <a href="mailto:maia.phs@gmail.com">📧 maia.phs@gmail.com</a>
            <a href="https://www.linkedin.com/in/pedromaiapapilodata/" target="_blank">🔗 LinkedIn (Pedro Maia)</a>
        </div>
    `;
    window.parent.document.body.appendChild(footer);
</script>
""", height=0)

# Injeção de CSS para destaques críticos (Transparência Matemática e Status Bar)
st.markdown("""
<style>
/* Animação Premium: Fade & Focus (Sem alteração geométrica) */
@keyframes smoothCascadeFocus {
    0% { opacity: 0; filter: blur(5px); }
    100% { opacity: 1; filter: blur(0); }
}

div[data-testid="stVerticalBlock"] > div {
    opacity: 0; 
    animation: smoothCascadeFocus 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Fundo Elegante e Trava contra barras de rolagem artificiais */
.stApp {
    overflow-x: hidden;
    background: radial-gradient(circle at 50% 0%, #121c2b 0%, #0e1117 60%) !important;
}

/* Atrasos escalonados */
div[data-testid="stVerticalBlock"] > div:nth-child(1) { animation-delay: 0.05s; }
div[data-testid="stVerticalBlock"] > div:nth-child(2) { animation-delay: 0.15s; }
div[data-testid="stVerticalBlock"] > div:nth-child(3) { animation-delay: 0.25s; }
div[data-testid="stVerticalBlock"] > div:nth-child(4) { animation-delay: 0.35s; }
div[data-testid="stVerticalBlock"] > div:nth-child(5) { animation-delay: 0.45s; }

.transparency-box {
    background-color: #2D2D2D;
    border-left: 5px solid #0072B2;
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 20px;
}
.transparency-box h4 {
    margin-top: 0;
    color: #0072B2;
}

/* Estilo da Barra de Status Discreta */
.status-bar-container {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    padding: 5px 0px 10px 0px;
    margin-bottom: 5px;
    border-bottom: 1px solid #333;
}
.status-badge {
    background-color: #1E1E1E;
    color: #A0A0A0;
    border: 1px solid #444;
    border-radius: 12px;
    padding: 4px 10px;
    font-size: 0.75rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 5px;
}
.status-badge strong {
    color: #E0E0E0;
    font-weight: 600;
}

/* CSS para o Sticky Header (Glassmorphism) */
div[data-testid="stVerticalBlock"] > div:has(#sticky-header-anchor) {
    position: sticky;
    top: 2.875rem; /* Ajuste para não conflitar com a barra do topo do Streamlit */
    z-index: 999;
    background: rgba(14, 17, 23, 0.65); /* Fundo um pouco mais transparente */
    backdrop-filter: blur(12px); /* Efeito de Vidro (Glassmorphism) */
    -webkit-backdrop-filter: blur(12px);
    padding: 10px 15px;
    border-radius: 12px; /* Bordas arredondadas tiram o aspecto de tijolo */
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS ---
datasets = data_loader.get_all_datasets()
opcoes_cenarios = [
    "Atual Sem Correção",
    "Atual Com Correção",
    "LONPC Sem Correção",
    "LONPC Com Correção",
    "Reestruturação 2024"
]

mapa_cenarios = {
    "Atual Sem Correção": datasets["atual_sem_correcao"],
    "Atual Com Correção": datasets["atual_com_correcao"],
    "LONPC Sem Correção": datasets["lonpc_sem_correcao"],
    "LONPC Com Correção": datasets["lonpc_com_correcao"],
    "Reestruturação 2024": datasets["reestruturacao"]
}

# --- CONTROLES SUPERIORES EXPANSÍVEIS E FIXOS ---
with st.container():
    st.markdown('<div id="sticky-header-anchor"></div>', unsafe_allow_html=True)
    
    # Placeholder Dinâmico que começa só com o título e depois carrega os status ao lado
    status_bar_placeholder = st.empty()
    status_bar_placeholder.markdown("<h3 style='margin:0; padding-bottom:10px; font-size:1.4rem;'>Painel Interativo: Estudo de Atribuições da PCSP (2024)</h3>", unsafe_allow_html=True)
    
    with st.popover("⚙️ Configurações Analíticas e Controles", use_container_width=False):
        col1, col2, col3 = st.columns([1.5, 1.5, 2])
        
        with col1:
            cenario_sel = st.selectbox("Selecione o Cenário:", opcoes_cenarios)
            df_cenario = mapa_cenarios.get(cenario_sel)
            cargos_disponiveis = df_cenario['Carreira'].tolist() if df_cenario is not None and 'Carreira' in df_cenario.columns else (df_cenario.index.tolist() if df_cenario is not None else [])
            
            # Filtros Macros (Polícia Científica vs PCSP)
            cientifica_keywords = ["Perito", "Médico", "Fotógrafo", "Desenhista", "Necropsia", "Necrópsia", "Atendente"]
            cargos_cientifica = [c for c in cargos_disponiveis if any(k in c for k in cientifica_keywords)]
            cargos_pc = [c for c in cargos_disponiveis if c not in cargos_cientifica]
            
            grupo_sel = st.radio(
                "Filtro Rápido de Cargos:",
                ["Todos os cargos da Polícia Civil", "Polícia Civil sem cargos da Polícia Científica", "Polícia Civil com somente Polícia Científica", "Personalizado"]
            )
    
    with col2:
        incluir_comuns = st.toggle("Incluir Atribuições Genéricas a Todos", value=False, help="Se ativado, não oculta as atribuições normativas comuns a todos os cargos e desabilita o formato Condensado.")
        tipo_matriz_raw = st.radio(
            "Formato da Matriz:", 
            ["Condensada (Aglutina repetições)", "Original (Dados brutos)"], 
            horizontal=False, 
            disabled=incluir_comuns,
            help="**Condensada:** Junta funções redundantes em uma única coluna.\n\n**Original:** Mantém os dados brutos."
        )
        tipo_matriz = "Original" if "Original" in tipo_matriz_raw or incluir_comuns else "Condensada"
        expandir_textos = st.checkbox("Expandir textos nos tooltips", value=True)
        
        kpi_placeholder = col3.empty()
        
        if grupo_sel == "Todos os cargos da Polícia Civil":
            cargos_selecionados = []
        elif grupo_sel == "Polícia Civil sem cargos da Polícia Científica":
            cargos_selecionados = cargos_pc
        elif grupo_sel == "Polícia Civil com somente Polícia Científica":
            cargos_selecionados = cargos_cientifica
        else:
            cargos_selecionados = st.multiselect("Cargos a Analisar (Personalizado):", cargos_disponiveis)
            
        st.markdown("<div style='text-align: center; color: #666; font-size: 0.8rem; margin-top: 15px;'><em>Clique em qualquer área externa para recolher este painel</em></div>", unsafe_allow_html=True)


# Registrar log invisível de visita
if 'visit_logged' not in st.session_state:
    logger.log_visit(cenario_sel)


if df_cenario is not None and not df_cenario.empty:
    # Higienização de Nomes Longos que quebram a interface
    if 'Carreira' in df_cenario.columns:
        df_cenario['Carreira'] = df_cenario['Carreira'].replace({
            "Investigador de Polícia (+ Agente de Telecomunicações Policial + Agente Policial + Carcereiro Policial)": "Investigador de Polícia (+ Apoio)"
        })

    # Aplicação de Filtros de Cargos
    if cargos_selecionados:
        if 'Carreira' in df_cenario.columns:
            df_cenario = df_cenario[df_cenario['Carreira'].isin(cargos_selecionados)]
        else:
            df_cenario = df_cenario.loc[cargos_selecionados]
            
    # Processamento Matemático Principal
    if incluir_comuns:
        col_sums = df_cenario.sum(axis=0)
        num_reais = len(df_cenario)
        colunas_comuns = df_cenario.columns[col_sums == num_reais].tolist()
        colunas_outras = [c for c in df_cenario.columns if c not in colunas_comuns]
        df_original_limpo = df_cenario[colunas_comuns + colunas_outras].copy()
        df_condensado = df_original_limpo
    else:
        df_original_limpo = data_processing.remover_atribuicoes_comuns(df_cenario)
        df_condensado, historico = data_processing.condensar_dataframe(df_cenario)
    
    # Switch Lógico
    df_to_use = df_original_limpo if tipo_matriz == "Original" else df_condensado
    
    # Siglas e Textos
    dic_siglas = data_processing.gerar_dicionario_siglas(df_to_use.columns)
    dic_reverso = {v: k for k, v in dic_siglas.items()}
    df_to_use_siglas = data_processing.aplicar_siglas_dataframe(df_to_use, dic_siglas)
    text_matrix = data_processing.obter_atribuicoes_comuns_textuais(df_to_use, dic_siglas, expandir_textos)

    # --- INJEÇÃO DO HEADER COMBINADO (Título + Status) ---
    lbl_cargos = "Todos" if not cargos_selecionados else f"{len(cargos_selecionados)} Selecionados"
    lbl_genericas = "ON" if incluir_comuns else "OFF"
    lbl_textos = "ON" if expandir_textos else "OFF"
    
    lista_cargos_html = ""
    if cargos_selecionados:
        lista_cargos_html = f"<div style='text-align: right; color: #C0C0C0; font-size: 0.9rem; margin-top: 5px; margin-bottom: 5px;'><strong>Cargos ativos:</strong> {', '.join(cargos_selecionados)}</div>"
    
    header_html = f"""
    <div style='display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 10px; flex-wrap: wrap; gap: 10px;'>
        <h3 style='margin: 0; padding: 0; font-size: 1.4rem; color: #E0E0E0;'>Painel Interativo: Atribuições PCSP</h3>
        <div style='display: flex; gap: 5px; flex-wrap: wrap;'>
            <div class='status-badge'>⚙️ Cenário: <strong>{cenario_sel}</strong></div>
            <div class='status-badge'>📊 Matriz: <strong>{tipo_matriz}</strong></div>
            <div class='status-badge'>👥 Genéricas: <strong>{lbl_genericas}</strong></div>
            <div class='status-badge'>🏷️ Textos Extensos: <strong>{lbl_textos}</strong></div>
            <div class='status-badge'>🚓 Cargos: <strong>{lbl_cargos}</strong></div>
        </div>
    </div>
    {lista_cargos_html}
    """
    status_bar_placeholder.markdown(header_html, unsafe_allow_html=True)

    # --- INJEÇÃO DOS KPIs DENTRO DA GAVETA ---
    reducao = len(df_original_limpo.columns) - len(df_condensado.columns)
    pct_reducao = (reducao / len(df_original_limpo.columns)) * 100 if len(df_original_limpo.columns) > 0 else 0
    
    html_kpis = f"""
    <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 10px;">
        <div style="display: flex; justify-content: space-between; text-align: center; background: #1E1E1E; padding: 10px; border-radius: 8px; border: 1px solid #333;">
            <div title="Total de atribuições únicas extraídas dos editais para os cargos selecionados, antes de aglutinar as redundâncias.">
                <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Atribuições Originais <span style="cursor:help; color:#888; font-size:0.75rem;">ⓘ</span></div>
                <div style="font-size: 1.1rem; line-height: 1.2;">{len(df_original_limpo.columns)}</div>
            </div>
            <div title="Quantidade de colunas exclusivas na matriz após juntar numa só as atribuições idênticas que eram comuns a múltiplos cargos.">
                <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Atribuições Condensadas <span style="cursor:help; color:#888; font-size:0.75rem;">ⓘ</span></div>
                <div style="font-size: 1.1rem; line-height: 1.2;">{len(df_condensado.columns)}</div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; text-align: center; background: #1E1E1E; padding: 10px; border-radius: 8px; border: 1px solid #333;">
            <div title="Diferença absoluta entre as atribuições originais e as condensadas (quantidade de ruído/redundância eliminada).">
                <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Redução <span style="cursor:help; color:#888; font-size:0.75rem;">ⓘ</span></div>
                <div style="font-size: 1.1rem; color: #00C851; line-height: 1.2; font-weight: bold;">{reducao}</div>
            </div>
            <div title="Percentual que representa o nível de redundância normativa que foi superada pela metodologia na comparação.">
                <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Porcentagem de Redução <span style="cursor:help; color:#888; font-size:0.75rem;">ⓘ</span></div>
                <div style="font-size: 1.1rem; color: #00C851; line-height: 1.2; font-weight: bold;">{pct_reducao:.1f}%</div>
            </div>
        </div>
    </div>
    """
    kpi_placeholder.markdown(html_kpis, unsafe_allow_html=True)


    # 1. Matriz de Atribuições
    with st.expander("ⓘ Suposição Matemática Ativa (Metodologia de Condensação)"):
        st.markdown("As matrizes abaixo transformam listas de atribuições textuais em coordenadas numéricas. Ao passarem pela **Condensação**, repetições exatas entre os mesmos cargos viram uma única coluna. Isso impede que atribuições divididas em 10 itens no edital (mas que significam a mesma coisa) causem um 'peso estatístico artificial' que aproxime duas carreiras de forma incorreta.")

    st.subheader(f"1. Matriz de Atribuições ({tipo_matriz})", help="**Como interpretar:** Exibe o valor '1' se o cargo possui a atribuição normativa e '0' caso não possua. \n\n**Cálculo:** Construída lendo os manuais e editais. No modo 'Condensada', a matriz aglutina atribuições que possuem o exato mesmo padrão de repetição (ex: atribuições comuns a um mesmo grupo de cargos viram uma única coluna com peso 1) para evitar que redundâncias documentais criem distorções de peso estatístico.")
    st.markdown("<p style='font-size: 0.85rem; color: #9E9E9E; margin-top: -15px; margin-bottom: 10px;'>💡 <em>Dica: Passe o mouse sobre as células (quadrados coloridos) para ler a atribuição normativa completa.</em></p>", unsafe_allow_html=True)
    fig_bin = visualizations.plot_binary_heatmap(df_to_use_siglas, f"Matriz {tipo_matriz} - {cenario_sel}", colorscale="Teal", dic_reverso=dic_reverso)
    st.plotly_chart(fig_bin, use_container_width=True)
    
    # 2. Matriz de Adjacência
    st.subheader("2. Matriz de Adjacência (Atribuições Compartilhadas)", help="**Como interpretar:** Exibe a contagem absoluta de quantas atribuições normativas dois cargos distintos compartilham entre si. Valores mais altos (cores fortes) indicam forte justaposição funcional.\n\n**Cálculo:** Feito através do Produto Escalar cruzando a Matriz de Atribuições contra si própria (sua transposta).")
    adj_matrix = data_processing.gerar_matriz_adjacencia(df_to_use)
    fig_adj = visualizations.plot_adjacency_heatmap(adj_matrix, f"Adjacência - {cenario_sel}", text_matrix=text_matrix)
    st.plotly_chart(fig_adj, use_container_width=True)

    st.markdown("---")

    # 3. Explorador Dinâmico
    st.subheader("3. Explorador Dinâmico de Atribuições", help="**Como interpretar:** Permite cruzar dados manualmente simulando as tabelas dinâmicas do estudo original. Nota: No artigo o cruzamento limitou-se a 3 carreiras por falta de espaço em página, mas aqui o sistema calcula e confronta todas as carreiras ativas simultaneamente.\n\n**Porcentagens:** Exibe o volume de atribuições que cada cargo representa em relação ao somatório total de atribuições únicas na Polícia Civil.")
    
    df_explorer = df_original_limpo.set_index('Carreira') if 'Carreira' in df_original_limpo.columns else df_original_limpo.copy()
        
    # Total de atribuições na base (para a porcentagem)
    total_atribuicoes_base = len(df_explorer.columns)
    
    aba1, aba2 = st.tabs(["Filtro por Cargo (O que eles compartilham?)", "Filtro por Atribuição (Quem faz isso?)"])
    
    with aba1:
        st.markdown(f"**Base Total de Análise:** {total_atribuicoes_base} atribuições normativas possíveis na matriz de dados.")
        @st.cache_data(show_spinner=False)
        def carregar_tabela_conversao():
            try:
                df_t = pd.read_excel('Tabela_Conversao_Cargos.xlsx')
                if not df_t.empty and len(df_t.columns) > 1: return df_t
            except: pass
            
            for sep in [';', ',']:
                for enc in ['utf-8', 'iso-8859-1', 'cp1252']:
                    try:
                        df_t = pd.read_csv('Tabela_Conversao_Cargos.CSV', sep=sep, encoding=enc)
                        if not df_t.empty and len(df_t.columns) > 1: return df_t
                    except: pass
            return None

        df_conv = carregar_tabela_conversao()
        
        def mapear_trio_base(old_sel_list, new_list, cenario_antigo, cenario_novo):
            if df_conv is None or df_conv.empty: return []
            
        cargos_default_aba1 = []

        if 'last_cenario_aba1' not in st.session_state:
            st.session_state.last_cenario_aba1 = cenario_sel

        # Hook de mudança de cenário (agora apenas limpa o filtro)
        mudou_cenario = st.session_state.last_cenario_aba1 != cenario_sel
        if mudou_cenario:
            st.session_state["filtro_cargos_aba1"] = []
            st.session_state.last_cenario_aba1 = cenario_sel
        filtro_cargos = st.multiselect("Cargos:", df_explorer.index.tolist(), default=cargos_default_aba1, key="filtro_cargos_aba1")
        if filtro_cargos:
            # Filtra e transpõe
            df_filtro = df_explorer.loc[filtro_cargos]
            colunas_ativas = df_filtro.columns[(df_filtro > 0).any()]
            df_resultado = df_filtro[colunas_ativas].T
            
            # Seletor de Visibilidade (Exclusivas vs Compartilhadas)
            op_todas = "🌟 Mostrar Todas"
            op_excl_selecao = "🔸 Somente Exclusivas da Seleção (Nenhum cargo de fora faz)"
            op_comp_fora = "🔹 Somente Compartilhadas (Cargos de fora também fazem)"
            op_comp_dentro = "✅ Somente Compartilhadas (Cargos selecionados)"
            
            tipo_exclusividade = st.radio(
                "Filtro de Atribuições:", 
                [op_todas, op_excl_selecao, op_comp_fora, op_comp_dentro], 
                horizontal=True
            )
            
            somas_globais = df_explorer[df_resultado.index].sum(axis=0)
            somas_selecao = df_resultado.sum(axis=1)
            
            if tipo_exclusividade == op_excl_selecao:
                df_resultado = df_resultado[somas_globais == somas_selecao]
            elif tipo_exclusividade == op_comp_fora:
                df_resultado = df_resultado[somas_globais > somas_selecao]
            elif tipo_exclusividade == op_comp_dentro:
                df_resultado = df_resultado[somas_selecao > 1]
                
            if len(filtro_cargos) > 1:
                def status_compartilhamento(row):
                    if row.sum() == len(filtro_cargos):
                        return "✅ Compartilhada por Todos"
                    elif row.sum() == 1:
                        return "🔸 Exclusiva de 1 Cargo"
                    else:
                        return "🔹 Compartilhada por Alguns"
                df_resultado['Status'] = df_resultado.apply(status_compartilhamento, axis=1)
                
            # Restaura Nomes
            df_resultado.index = [dic_reverso.get(col, col) for col in df_resultado.index]
            df_resultado.index.name = "Atribuição Normativa"
            
            # Mostra estatísticas de carga por cargo
            st.markdown("##### Peso Normativo (Montante de Atribuições por Cargo)")
            stats = []
            for c in filtro_cargos:
                qtd = df_filtro.loc[c].sum()
                pct = (qtd / total_atribuicoes_base) * 100
                stats.append({"Cargo": c, "Qtd Atribuições": int(qtd), "Representatividade (%)": f"{pct:.1f}%"})
            
            st.dataframe(pd.DataFrame(stats).set_index("Cargo"), use_container_width=True)
            st.markdown("##### Quadro de Cruzamento de Atribuições")
            st.dataframe(df_resultado, use_container_width=True)
            
    with aba2:
        st.markdown("Selecione uma ou mais atribuições para descobrir quais carreiras policiais as possuem formalmente em seus escopos.")
        todas_atrib = df_explorer.columns.tolist()
        filtro_atrib = st.multiselect("Atribuições:", todas_atrib, key="filtro_atrib_aba2")
        if filtro_atrib:
            df_filtro_atrib = df_explorer[filtro_atrib].copy()
            df_filtro_atrib = df_filtro_atrib[(df_filtro_atrib > 0).any(axis=1)]
            df_filtro_atrib.columns = filtro_atrib
            df_filtro_atrib.index.name = "Carreira Policial"
            st.dataframe(df_filtro_atrib, use_container_width=True)

    st.markdown("---")

    # 4. Mapa de Calor de Similaridade (Gower)
    st.subheader("4. Mapa de Calor de Similaridade (Distância de Gower)", help="**Como interpretar:** Esta é uma visão térmica do distanciamento. Áreas vermelhas representam cargos praticamente idênticos (Distância próxima de 0.0). Áreas azuis evidenciam o extremo oposto.\n\n**Cálculo:** Diferente do mapa de adjacência (que usa contagem bruta), este usa o Coeficiente de Gower entre 0 e 1, penalizando estatisticamente grandes disparidades.")
    
    df_para_gower = df_to_use.copy()
    if incluir_comuns:
        # Injeta o pseudo-cargo apenas para os cálculos de similaridade relativos
        num_cargos_reais = len(df_para_gower)
        
        # Calcula soma ignorando a coluna 'Carreira' que é string
        numeric_cols = df_para_gower.select_dtypes(include='number').columns
        pseudo_row = (df_para_gower[numeric_cols].sum(axis=0) == num_cargos_reais).astype(int)
        
        # Como o Gower usa a coluna Carreira para nomear o índice, precisamos setar explicitamente
        if 'Carreira' in df_para_gower.columns:
            pseudo_row['Carreira'] = "Policial Civil (todos os cargos)"
            
        pseudo_row.name = "Policial Civil (todos os cargos)"
        df_para_gower.loc[pseudo_row.name] = pseudo_row
        
    df_gower = data_processing.calcular_distancias_gower(df_para_gower)
    fig_gower_heat = visualizations.plot_gower_heatmap(df_gower, f"Matriz de Distância de Gower - {cenario_sel}")
    st.plotly_chart(fig_gower_heat, use_container_width=True)

    st.markdown("---")

    # 5. Régua Gower
    st.subheader("5. Régua de Similaridade Relativa (Distância de Gower)", help="**Como interpretar:** Fixando um cargo central na marca 'Zero', mapeia o afastamento estatístico de todas as outras carreiras. Valores próximos de Zero demonstram alta comunhão de atribuições, enquanto valores que tangenciam 1.0 (ou mais distantes) revelam carreiras completamente díspares.\n\n**Cálculo:** Emprega o Coeficiente de Distância de Gower para dados mistos, cruzando os arrays de presenças (1) e ausências (0) de cada binômio de cargos na matriz.")
    ref_cargo = st.selectbox(
        "Selecione o Cargo de Referência:", 
        df_gower.columns, 
        index=0,
        format_func=lambda x: f"{x} (usado no artigo)" if x == "Delegado de Polícia" else x
    )
    fig_gower = visualizations.plot_gower_ruler(df_gower, reference_career=ref_cargo)
    st.plotly_chart(fig_gower, use_container_width=True)

    st.markdown("---")

    # 6. Dendograma
    st.subheader("6. Árvore Hierárquica (Dendograma)", help="**Como interpretar:** Classifica e agrupa sub-blocos de carreiras que possuem alta afinidade. Se duas carreiras se conectam mais para baixo (mais à esquerda nos eixos X), significa que são funcionalmente muito idênticas e foram agrupadas primeiro na base.\n\n**Cálculo:** Utiliza Algoritmo de Clusterização Hierárquica sobre as métricas da Matriz de Gower. Foi utilizado o método aglomerativo *Single-linkage*, que calcula a distância mínima entre membros de grupos adjacentes.")
    st.markdown("Agrupamento hierárquico das distâncias de Gower usando o método *single*.")
    if len(df_gower.columns) > 1:
        fig_dendro = visualizations.plot_dendrogram(df_gower, f"Dendograma Gower - {cenario_sel}")
        st.plotly_chart(fig_dendro, use_container_width=True)
    else:
        st.warning("Selecione mais de um cargo para gerar a árvore hierárquica.")

    st.markdown("---")

    # 7. Grafo de Similaridade
    st.subheader("7. Grafo de Similaridade (Baseado em Adjacência)", help="**Como interpretar:** Representação de rede onde as 'bolas' (nós) representam as carreiras policiais e as 'linhas' (arestas) indicam que há uma intersecção de funções. A espessura da linha simboliza a quantidade de funções compartilhadas.\n\n**Cálculo:** Renderizado pelo motor NetworkX com física Fruchterman-Reingold (Spring Layout), que cria forças de repulsão magnética entre os nós, permitindo que cargos altamente conectados 'puxem' uns aos outros para o centro do agrupamento (cluster).")
    threshold_adj = st.slider("Corte de Adjacência (Threshold de Conexões):", min_value=1, max_value=15, value=1, step=1)
    nodes_data, edges_data, pos = data_processing.gerar_dados_grafo(adj_matrix, threshold=threshold_adj, text_matrix=text_matrix)
    fig_grafo = visualizations.plot_network_graph(nodes_data, edges_data, f"Rede de Carreiras (Adjacência >= {threshold_adj})")
    st.plotly_chart(fig_grafo, use_container_width=True)

    st.markdown("---")

    # 8. UpSet Plot (Alternativa ao Venn)
    st.subheader("8. Diagrama de Conjuntos (Interseções Exatas)", help="**Como interpretar:** Funciona como um 'Diagrama de Venn' escalável. Ele varre as centenas de combinações possíveis entre os cargos e lista as maiores fatias em comum. A barra revela exatamente quantas atribuições aquele 'bloco' de cargos exclusivo possui.\n\n**Por que não usar um Diagrama de Venn circular?** Matematicamente, círculos só conseguem se sobrepor em todas as permutações para, no máximo, 4 conjuntos. Como possuímos 14 cargos diferentes, um Venn seria geometricamente impossível de ser desenhado sem violar as leis espaciais. Este formato (UpSet Plot) é o padrão ouro na visualização multicamadas na Ciência de Dados.")
    
    # O Diagrama de Conjuntos sempre usa os dados originais (não-condensados) para manter a precisão geométrica das fatias.
    df_upset = df_original_limpo.set_index('Carreira') if 'Carreira' in df_original_limpo.columns else df_original_limpo.copy()
    fig_upset = visualizations.plot_upset_bar_chart(df_upset, f"Top Interseções Normativas (Granular) - {cenario_sel}")
    st.plotly_chart(fig_upset, use_container_width=True)

else:
    st.error("Cenário indisponível.")


