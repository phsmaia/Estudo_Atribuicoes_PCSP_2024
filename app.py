import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import importlib
import explanations
importlib.reload(explanations)
import pandas as pd
import data_loader
import data_processing
import visualizations
import logger
import os
import explanations
import importlib
importlib.reload(explanations)

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
    background: radial-gradient(circle at 50% 0%, #121c2b 0%, #0e1117 60%) !important;
}

/* Atrasos escalonados */
div[data-testid="stVerticalBlock"] > div:nth-child(1) { animation-delay: 0.05s; }
div[data-testid="stVerticalBlock"] > div:nth-child(2) { animation-delay: 0.15s; }
div[data-testid="stVerticalBlock"] > div:nth-child(3) { animation-delay: 0.25s; }
div[data-testid="stVerticalBlock"] > div:nth-child(4) { animation-delay: 0.35s; }
div[data-testid="stVerticalBlock"] > div:nth-child(5) { animation-delay: 0.45s; }

/* Sticky Container Header */
div[data-testid="stLayoutWrapper"]:has(div#sticky-header-anchor):has(div[data-testid="stRadio"]) {
    position: sticky;
    top: 0;
    z-index: 999;
    background-color: rgba(14, 17, 23, 0.95);
    padding: 15px 20px 10px 20px;
    border-radius: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 25px;
    backdrop-filter: blur(10px);
}

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

# --- CABEÇALHO GLOBAL E ROTEAMENTO ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem !important; 
        padding-bottom: 1rem !important;
    }
    
    header[data-testid="stHeader"] {
        display: none;
    }
    
    </style>
""", unsafe_allow_html=True)

# Container Exclusivo para o Header Sticky
with st.container():
    st.markdown("<div id='sticky-header-anchor'></div>", unsafe_allow_html=True)
    status_bar_placeholder = st.empty()
    status_bar_placeholder.markdown("""
    <div id='sticky-header-anchor'></div>
    <div style='display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 10px; flex-wrap: wrap; gap: 10px;'>
        <h3 style='margin: 0; padding: 0; font-size: 1.4rem; color: #E0E0E0;'>Painel Interativo: Estudo de Atribuições da PCSP (2024)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_label, col_radio = st.columns([2, 8])
    with col_label:
        st.markdown("<h4 style='margin:0; margin-top:5px; font-size:1.1rem; color:#ccc;'>Modos de Visão:</h4>", unsafe_allow_html=True)
    with col_radio:
        modo_visao = st.radio(
            "Navegação Analítica:",
            ["1. Explorador Individual", "2. Análise de Cenários (Comparativo A x B)", "3. Comparação Global (Macro)", "4. Rastreamento Longitudinal (Micro)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
    col_exp_1, col_exp_2 = st.columns([3, 7])
    with col_exp_1:
        st.toggle("📖 Modo de Explicações Detalhadas", key="show_explanations")
    with col_exp_2:
        if st.session_state.get('show_explanations', False):
            st.radio("Tom de Leitura:", ["👨‍🔬 Acadêmico / Técnico", "🗣️ Leigo / Simplificado"], horizontal=True, label_visibility="collapsed", key="explanation_tone")
        
    is_sample_biased_global = False
    
    # --- CONTROLES SUPERIORES (APENAS EXPLORADOR INDIVIDUAL) ---
    if modo_visao == "1. Explorador Individual":
        with st.popover("⚙️ Configurações Analíticas e Controles", use_container_width=True):
            col1, col2, col3 = st.columns([1, 1, 1.5])
            
            with col1:
                cenario_sel = st.selectbox("Selecione o Cenário:", opcoes_cenarios)
                df_cenario = mapa_cenarios.get(cenario_sel)
                cargos_disponiveis = df_cenario['Carreira'].tolist() if df_cenario is not None and 'Carreira' in df_cenario.columns else (df_cenario.index.tolist() if df_cenario is not None else [])
                
                cientifica_keywords = ["Perito", "Médico", "Fotógrafo", "Desenhista", "Necropsia", "Necrópsia", "Atendente"]
                cargos_cientifica = [c for c in cargos_disponiveis if any(k in c for k in cientifica_keywords)]
                cargos_pc = [c for c in cargos_disponiveis if c not in cargos_cientifica]
                
            with col2:
                grupo_sel = st.selectbox(
                    "Filtro Rápido de Cargos:",
                    ["Todos os cargos da Polícia Civil", "Polícia Civil sem cargos da Polícia Científica", "Polícia Civil com somente Polícia Científica", "Personalizado"]
                )
                
                if grupo_sel == "Todos os cargos da Polícia Civil":
                    default_cargos = cargos_disponiveis
                elif grupo_sel == "Polícia Civil sem cargos da Polícia Científica":
                    default_cargos = cargos_pc
                elif grupo_sel == "Polícia Civil com somente Polícia Científica":
                    default_cargos = cargos_cientifica
                else:
                    default_cargos = []
                    
                incluir_comuns = st.checkbox("Incluir Atribuições Genéricas a Todos", value=False)
                
            with col1:
                tipo_matriz_raw = st.selectbox(
                    "Formato da Matriz:", 
                    ["Condensada (Aglutina repetições)", "Original (Dados brutos)"], 
                    disabled=incluir_comuns
                )
                tipo_matriz = "Original" if "Original" in tipo_matriz_raw or incluir_comuns else "Condensada"
                
            with col2:
                expandir_textos = st.checkbox("Expandir textos nos tooltips", value=True)
                
            with col3:
                filtro_cargos = st.multiselect(
                    "Cargos para Analisar:", 
                    cargos_disponiveis,
                    default=default_cargos
                )
                cargos_destaque = st.multiselect(
                    "🎨 Destaque Visual (Opcional):",
                    filtro_cargos if filtro_cargos else cargos_disponiveis
                )
                
                if cargos_destaque:
                    css_tags = ""
                    for cargo in cargos_destaque:
                        css_tags += f'''
                        span[data-baseweb="tag"][aria-label^="{cargo}"] {{
                            background-color: rgba(255, 152, 0, 0.3) !important;
                            border: 1px solid #ff9800 !important;
                        }}
                        span[data-baseweb="tag"][aria-label^="{cargo}"] span {{
                            color: #ffb74d !important;
                        }}
                        '''
                    st.markdown(f"<style>{css_tags}</style>", unsafe_allow_html=True)
                    
            if 'filtro_cargos' in locals() and 'cargos_disponiveis' in locals():
                if filtro_cargos and len(filtro_cargos) < len(cargos_disponiveis):
                    is_sample_biased_global = True

    # --- CONTROLES MODO 2 ---
    elif modo_visao == "2. Análise de Cenários (Comparativo A x B)":
        with st.popover("⚙️ Configurações do Comparativo A x B", use_container_width=True):
            col_a, col_b = st.columns(2)
            cenario_a = col_a.selectbox("📌 Cenário A (Base):", opcoes_cenarios, index=0)
            cenario_b = col_b.selectbox("📌 Cenário B (Comparação):", opcoes_cenarios, index=1)
            
            df_a = mapa_cenarios.get(cenario_a)
            if df_a is not None and 'Carreira' in df_a.columns:
                cargos_base = df_a['Carreira'].tolist()
            else:
                cargos_base = df_a.index.tolist() if df_a is not None else []
                
            col_c, col_d = st.columns(2)
            carreira_sel_comparativo = col_c.selectbox("🔎 Selecione a Carreira para Análise Detalhada:", cargos_base, index=None, placeholder="Nenhuma (Visão Geral)")
            cargos_destaque_2 = col_d.multiselect("🎨 Destaque Visual (Opcional):", cargos_base, help="Realça essas carreiras nos gráficos e tabelas.")
            
        if carreira_sel_comparativo:
            import json
            with open('csv_dump.json', 'r', encoding='utf-8') as f:
                mapa_dict = json.load(f)
            cargo_foco_b = carreira_sel_comparativo
            for row in mapa_dict:
                val_a = row.get(cenario_a)
                if val_a == "Investigador de Polícia (+ Agente de Telecomunicações Policial + Agente Policial + Carcereiro Policial)":
                    val_a = "Investigador de Polícia (+ Apoio)"
                if val_a == carreira_sel_comparativo:
                    val_b = row.get(cenario_b)
                    if val_b == "Investigador de Polícia (+ Agente de Telecomunicações Policial + Agente Policial + Carcereiro Policial)":
                        val_b = "Investigador de Polícia (+ Apoio)"
                    cargo_foco_b = val_b
                    break
            rastreio_html = f"<div title='Rastreia as perdas e ganhos funcionais de uma carreira específica entre os dois cenários escolhidos.' style='cursor: help; background: rgba(0, 114, 178, 0.2); border: 1px solid #0072B2; padding: 6px 15px; border-radius: 8px; font-size: 0.85rem; color: #E0E0E0; width: 100%; margin-top: 5px;'>🔍 Rastreando carreira principal: <strong style='color: #4da6ff;'>{carreira_sel_comparativo}</strong> ({cenario_a}) ➔ <strong style='color: #4da6ff;'>{cargo_foco_b}</strong> ({cenario_b}) <span style='float:right'>ℹ️</span></div>"
        else:
            rastreio_html = ""
            
        badge_destaque_2 = ""
        if cargos_destaque_2:
            str_dest_2 = ", ".join([c.replace(' de Polícia', '').replace(' Policial', '') for c in cargos_destaque_2])
            badge_destaque_2 = f" <div class='status-badge' style='background: rgba(255, 152, 0, 0.2); border: 1px solid rgba(255, 152, 0, 0.5); color: #ffb74d;'>🎨 Destaques: <strong>{str_dest_2}</strong></div>"

        badge_vies_html = "<div class='status-badge' style='background: rgba(220, 53, 69, 0.2); border: 1px solid rgba(220, 53, 69, 0.5); color: #ff6b6b;'>⚠️ VIÉS AMOSTRAL</div>" if is_sample_biased_global else ""
        status_bar_placeholder.markdown(f"""
        <div id='sticky-header-anchor'></div>
        <div style='display: flex; flex-direction: column;'>
            <div style='display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 5px; flex-wrap: wrap; gap: 10px;'>
                <h3 style='margin: 0; padding: 0; font-size: 1.4rem; color: #E0E0E0;'>Painel Interativo: Estudo de Atribuições da PCSP (2024)</h3>
                <div style='display: flex; gap: 5px; flex-wrap: wrap;'>{badge_vies_html}
                    <div class='status-badge' title='Modo 2: Permite comparar o grau de distanciamento, afinidade e fluxo de funções normativas entre as carreiras policiais nos dois cenários temporais.' style='cursor: help;'>⚙️ Modo: <strong>Análise de Cenários (A x B)</strong> <span style='font-size:0.7rem'>ℹ️</span></div>
                    <div class='status-badge' title='Cenário de Origem da comparação (De onde os cargos partiram)' style='cursor: help;'>📌 A: <strong>{cenario_a}</strong></div>
                    <div class='status-badge' title='Cenário de Destino da comparação (Para onde os cargos foram)' style='cursor: help;'>📌 B: <strong>{cenario_b}</strong></div>{badge_destaque_2}
                </div>
            </div>
            {rastreio_html}
        </div>
        """, unsafe_allow_html=True)
            
    # --- CONTROLES MODO 3 ---
    elif modo_visao == "3. Comparação Global (Macro)":
        badge_vies_html = "<div class='status-badge' style='background: rgba(220, 53, 69, 0.2); border: 1px solid rgba(220, 53, 69, 0.5); color: #ff6b6b;'>⚠️ VIÉS AMOSTRAL</div>" if is_sample_biased_global else ""
        status_bar_placeholder.markdown(f"""
        <div id='sticky-header-anchor'></div>
        <div style='display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 10px; flex-wrap: wrap; gap: 10px;'>
            <h3 style='margin: 0; padding: 0; font-size: 1.4rem; color: #E0E0E0;'>Painel Interativo: Estudo de Atribuições da PCSP (2024)</h3>
            <div style='display: flex; gap: 5px; flex-wrap: wrap;'>{badge_vies_html}
                <div class='status-badge'>⚙️ Modo: <strong>Comparação Global (Macro)</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- CONTROLES MODO 4 ---
    elif modo_visao == "4. Rastreamento Longitudinal (Micro)":
        import json
        import os
        cargos_base_long = []
        try:
            if os.path.exists('csv_dump.json'):
                with open('csv_dump.json', 'r', encoding='utf-8') as f:
                    lista_mapa = json.load(f)
                    cargos_base_long = [row['Atual Sem Correção'] for row in lista_mapa]
        except Exception:
            pass
            
        with st.popover("⚙️ Configurações de Rastreamento Longitudinal", use_container_width=True):
            st.markdown("<p style='margin-top:-10px; color:#aaa; font-size:0.9rem;'>Isola carreiras específicas ou ofusca o restante para visualizar rotas evolutivas com clareza.</p>", unsafe_allow_html=True)
            filtro_cargos_long = st.multiselect("🔍 Filtrar Carreiras:", cargos_base_long, default=cargos_base_long)
            cargos_destaque_long = st.multiselect("💡 Destacar Carreiras (Realce Visual):", cargos_base_long, help="Se preenchido, ofusca as carreiras não marcadas no gráfico e aplica cores na tabela.")
            
        if 'filtro_cargos_long' in locals() and 'cargos_base_long' in locals():
            if filtro_cargos_long and len(filtro_cargos_long) < len(cargos_base_long):
                is_sample_biased_global = True

        badge_vies_html = "<div class='status-badge' style='background: rgba(220, 53, 69, 0.2); border: 1px solid rgba(220, 53, 69, 0.5); color: #ff6b6b;'>⚠️ VIÉS AMOSTRAL</div>" if is_sample_biased_global else ""
        status_bar_placeholder.markdown(f"""
        <div id='sticky-header-anchor'></div>
        <div style='display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 10px; flex-wrap: wrap; gap: 10px;'>
            <h3 style='margin: 0; padding: 0; font-size: 1.4rem; color: #E0E0E0;'>Painel Interativo: Estudo de Atribuições da PCSP (2024)</h3>
            <div style='display: flex; gap: 5px; flex-wrap: wrap;'>{badge_vies_html}
                <div class='status-badge'>⚙️ Modo: <strong>Rastreamento Longitudinal (Micro)</strong></div>
                <div class='status-badge'>🔍 Carreiras Filtradas: <strong>{len(filtro_cargos_long)}</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)



if is_sample_biased_global:
    st.warning(explanations.get_bias_warning(), icon="⚠️")

if modo_visao == "2. Análise de Cenários (Comparativo A x B)":
    import comparative_view
    import importlib
    importlib.reload(comparative_view)
    comparative_view.render_comparativo_axb(opcoes_cenarios, mapa_cenarios, cenario_a, cenario_b, carreira_sel_comparativo, cargos_destaque_2)
    st.stop()
    
elif modo_visao == "3. Comparação Global (Macro)":
    import timeline_view
    import importlib
    importlib.reload(timeline_view)
    timeline_view.render_timeline_mode(opcoes_cenarios, mapa_cenarios)
    st.stop()
    
elif modo_visao == "4. Rastreamento Longitudinal (Micro)":
    import longitudinal_view
    import importlib
    importlib.reload(longitudinal_view)
    longitudinal_view.render_longitudinal_mode(opcoes_cenarios, mapa_cenarios, filtro_cargos_long, cargos_destaque_long)
    st.stop()
    

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
    if filtro_cargos:
        if 'Carreira' in df_cenario.columns:
            df_cenario = df_cenario[df_cenario['Carreira'].isin(filtro_cargos)]
        else:
            df_cenario = df_cenario.loc[filtro_cargos]
            
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
    lbl_cargos = "Todos" if not filtro_cargos else f"{len(filtro_cargos)} Selecionados"
    lbl_genericas = "ON" if incluir_comuns else "OFF"
    lbl_textos = "ON" if expandir_textos else "OFF"
    
    lista_cargos_html = ""
    if filtro_cargos and len(filtro_cargos) < len(cargos_disponiveis):
        lista_cargos_html = f"<div style='text-align: right; color: #C0C0C0; font-size: 0.9rem; margin-top: 5px; margin-bottom: 5px;'><strong>Cargos ativos:</strong> {', '.join(filtro_cargos)}</div>"
    
    badge_destaque = ""
    if cargos_destaque:
        str_dest = ", ".join([c.replace(' de Polícia', '').replace(' Policial', '') for c in cargos_destaque])
        badge_destaque = f" <div class='status-badge' style='background: rgba(255, 152, 0, 0.2); border: 1px solid rgba(255, 152, 0, 0.5); color: #ffb74d;'>🎨 Destaques: <strong>{str_dest}</strong></div>"

    badge_vies_html = "<div class='status-badge' style='background: rgba(220, 53, 69, 0.2); border: 1px solid rgba(220, 53, 69, 0.5); color: #ff6b6b;'>⚠️ VIÉS AMOSTRAL</div>" if is_sample_biased_global else ""
    header_html = f"""
    <div id='sticky-header-anchor'></div>
    <div style='display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 10px; flex-wrap: wrap; gap: 10px;'>
        <h3 style='margin: 0; padding: 0; font-size: 1.4rem; color: #E0E0E0;'>Painel Interativo: Estudo de Atribuições da PCSP (2024)</h3>
        <div style='display: flex; gap: 5px; flex-wrap: wrap;'>{badge_vies_html}
            <div class='status-badge'>⚙️ Cenário: <strong>{cenario_sel}</strong></div>
            <div class='status-badge'>📊 Matriz: <strong>{tipo_matriz}</strong></div>
            <div class='status-badge'>👥 Genéricas: <strong>{lbl_genericas}</strong></div>
            <div class='status-badge'>🏷️ Textos Extensos: <strong>{lbl_textos}</strong></div>
            <div class='status-badge'>🚓 Cargos: <strong>{lbl_cargos}</strong></div>{badge_destaque}
        </div>
    </div>
    {lista_cargos_html}
    """
    status_bar_placeholder.markdown(header_html, unsafe_allow_html=True)

    # --- INJEÇÃO DOS KPIs DENTRO DA GAVETA ---
    is_sample_biased = filtro_cargos and len(filtro_cargos) < len(cargos_disponiveis)

    reducao = len(df_original_limpo.columns) - len(df_condensado.columns)
    pct_reducao = (reducao / len(df_original_limpo.columns)) * 100 if len(df_original_limpo.columns) > 0 else 0
    
    html_kpis = f"""
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
        <div style="flex: 1; min-width: 140px; text-align: center; background: #1E1E1E; padding: 10px; border-radius: 8px; border: 1px solid #333;" title="Total de atribuições únicas extraídas dos editais para os cargos selecionados, antes de aglutinar as redundâncias.">
            <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Atribuições Originais <span style="cursor:help; color:#888; font-size:0.75rem;">ⓘ</span></div>
            <div style="font-size: 1.1rem; line-height: 1.2;">{len(df_original_limpo.columns)}</div>
        </div>
        <div style="flex: 1; min-width: 140px; text-align: center; background: #1E1E1E; padding: 10px; border-radius: 8px; border: 1px solid #333;" title="Quantidade de colunas exclusivas na matriz após juntar numa só as atribuições idênticas que eram comuns a múltiplos cargos.">
            <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Atribuições Condensadas <span style="cursor:help; color:#888; font-size:0.75rem;">ⓘ</span></div>
            <div style="font-size: 1.1rem; line-height: 1.2;">{len(df_condensado.columns)}</div>
        </div>
        <div style="flex: 1; min-width: 140px; text-align: center; background: #1E1E1E; padding: 10px; border-radius: 8px; border: 1px solid #333;" title="Diferença absoluta entre as atribuições originais e as condensadas (quantidade de ruído/redundância eliminada).">
            <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Redução <span style="cursor:help; color:#888; font-size:0.75rem;">ⓘ</span></div>
            <div style="font-size: 1.1rem; color: #00C851; line-height: 1.2; font-weight: bold;">{reducao}</div>
        </div>
        <div style="flex: 1; min-width: 140px; text-align: center; background: #1E1E1E; padding: 10px; border-radius: 8px; border: 1px solid #333;" title="Percentual que representa o nível de redundância normativa que foi superada pela metodologia na comparação.">
            <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Porcentagem de Redução <span style="cursor:help; color:#888; font-size:0.75rem;">ⓘ</span></div>
            <div style="font-size: 1.1rem; color: #00C851; line-height: 1.2; font-weight: bold;">{pct_reducao:.1f}%</div>
        </div>
    </div>
    """

    # 1.1. Matriz de Atribuições
    with st.expander("ⓘ Suposição Matemática Ativa (Metodologia de Condensação)"):
        st.markdown("As matrizes abaixo transformam listas de atribuições textuais em coordenadas numéricas. Ao passarem pela **Condensação**, repetições exatas entre os mesmos cargos viram uma única coluna. Isso impede que atribuições divididas em 10 itens no edital (mas que significam a mesma coisa) causem um 'peso estatístico artificial' que aproxime duas carreiras de forma incorreta.")

    st.markdown(html_kpis, unsafe_allow_html=True)

    if is_sample_biased:
        st.warning(explanations.get_short_bias_warning(), icon="🚨")
    st.subheader(f"1.1. Matriz de Atribuições ({tipo_matriz})", help="**Como interpretar:** Exibe o valor '1' se o cargo possui a atribuição normativa e '0' caso não possua. \n\n**Cálculo:** Construída lendo os manuais e editais. No modo 'Condensada', a matriz aglutina atribuições que possuem o exato mesmo padrão de repetição (ex: atribuições comuns a um mesmo grupo de cargos viram uma única coluna com peso 1) para evitar que redundâncias documentais criem distorções de peso estatístico.")
    st.markdown("<p style='font-size: 0.85rem; color: #9E9E9E; margin-top: -15px; margin-bottom: 10px;'>💡 <em>Dica: Passe o mouse sobre as células (quadrados coloridos) para ler a atribuição normativa completa.</em></p>", unsafe_allow_html=True)
    fig_bin = visualizations.plot_binary_heatmap(df_to_use_siglas, f"Matriz {tipo_matriz} - {cenario_sel}", colorscale="Teal", dic_reverso=dic_reverso, cargos_destaque=cargos_destaque)
    st.plotly_chart(fig_bin, use_container_width=True)
    if st.session_state.get('show_explanations', False):
        st.info(explanations.get_explanation("matriz", st.session_state.get('explanation_tone', 'tecnico')))
    
    # 1.2. Matriz de Adjacência
    if is_sample_biased:
        st.warning(explanations.get_short_bias_warning(), icon="🚨")
    st.subheader("1.2. Matriz de Adjacência (Atribuições Compartilhadas)", help="**Como interpretar:** Exibe a contagem absoluta de quantas atribuições normativas dois cargos distintos compartilham entre si. Valores mais altos (cores fortes) indicam forte justaposição funcional.\n\n**Cálculo:** Feito através do Produto Escalar cruzando a Matriz de Atribuições contra si própria (sua transposta).")
    adj_matrix = data_processing.gerar_matriz_adjacencia(df_to_use)
    fig_adj = visualizations.plot_adjacency_heatmap(adj_matrix, f"Adjacência - {cenario_sel}", text_matrix=text_matrix, cargos_destaque=cargos_destaque)
    st.plotly_chart(fig_adj, use_container_width=True)
    if st.session_state.get('show_explanations', False):
        st.info(explanations.get_explanation("adjacencia", st.session_state.get('explanation_tone', 'tecnico')))

    st.markdown("---")

    # 1.3. Explorador Dinâmico
    if is_sample_biased:
        st.warning(explanations.get_short_bias_warning(), icon="🚨")
    st.subheader("1.3. Explorador Dinâmico de Atribuições", help="**Como interpretar:** Permite cruzar dados manualmente simulando as tabelas dinâmicas do estudo original. Nota: No artigo o cruzamento limitou-se a 3 carreiras por falta de espaço em página, mas aqui o sistema calcula e confronta todas as carreiras ativas simultaneamente.\n\n**Porcentagens:** Exibe o volume de atribuições que cada cargo representa em relação ao somatório total de atribuições únicas na Polícia Civil.")
    
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
            
            df_stats = pd.DataFrame(stats).set_index("Cargo")
            
            def highlight_stats(row):
                if cargos_destaque and row.name in cargos_destaque:
                    return ['background-color: rgba(255, 152, 0, 0.2); color: #ffb74d; font-weight: bold;'] * len(row)
                return [''] * len(row)
                
            st.dataframe(df_stats.style.apply(highlight_stats, axis=1), use_container_width=True)
            st.markdown("##### Quadro de Cruzamento de Atribuições")
            
            for c in filtro_cargos:
                if c in df_resultado.columns:
                    df_resultado[c] = df_resultado[c].apply(lambda x: '✔️' if isinstance(x, (int, float)) and x > 0 else '❌' if isinstance(x, (int, float)) and x == 0 else x)

            def highlight_cruzamento(row):
                styles = []
                for col in df_resultado.columns:
                    if cargos_destaque and col in cargos_destaque:
                        if row[col] == '✔️':
                            styles.append('background-color: rgba(255, 152, 0, 0.25); color: #ffb74d; font-weight: bold;')
                        else:
                            styles.append('background-color: rgba(255, 152, 0, 0.05);')
                    else:
                        styles.append('')
                return styles

            st.dataframe(df_resultado.style.apply(highlight_cruzamento, axis=1), use_container_width=True)
            
    with aba2:
        st.markdown("Selecione uma ou mais atribuições para descobrir quais carreiras policiais as possuem formalmente em seus escopos.")
        todas_atrib = df_explorer.columns.tolist()
        filtro_atrib = st.multiselect("Atribuições:", todas_atrib, key="filtro_atrib_aba2")
        if filtro_atrib:
            df_filtro_atrib = df_explorer[filtro_atrib].copy()
            df_filtro_atrib = df_filtro_atrib[(df_filtro_atrib > 0).any(axis=1)]
            df_filtro_atrib.columns = filtro_atrib
            df_filtro_atrib.index.name = "Carreira Policial"
            
            for col in df_filtro_atrib.columns:
                df_filtro_atrib[col] = df_filtro_atrib[col].apply(lambda x: '✔️' if isinstance(x, (int, float)) and x > 0 else '❌')
                
            def highlight_aba2(row):
                if cargos_destaque and row.name in cargos_destaque:
                    return ['background-color: rgba(255, 152, 0, 0.25); color: #ffb74d; font-weight: bold;' if v == '✔️' else 'background-color: rgba(255, 152, 0, 0.05);' for v in row]
                return [''] * len(row)

            st.dataframe(df_filtro_atrib.style.apply(highlight_aba2, axis=1), use_container_width=True)

    if st.session_state.get('show_explanations', False):
        st.info(explanations.get_explanation("explorador", st.session_state.get('explanation_tone', 'tecnico')))

    st.markdown("---")

    # 1.4. Grafo de Similaridade
    if is_sample_biased:
        st.warning(explanations.get_short_bias_warning(), icon="🚨")
    st.subheader("1.4. Grafo de Similaridade (Baseado em Adjacência)", help="**Como interpretar:** Representação de rede onde as 'bolas' (nós) representam as carreiras policiais e as 'linhas' (arestas) indicam que há uma intersecção de funções. A espessura da linha simboliza a quantidade de funções compartilhadas.\n\n**Cálculo:** Renderizado pelo motor NetworkX com física Fruchterman-Reingold (Spring Layout), que cria forças de repulsão magnética entre os nós, permitindo que cargos altamente conectados 'puxem' uns aos outros para o centro do agrupamento (cluster).")
    threshold_adj = st.slider("Corte de Adjacência (Threshold de Conexões):", min_value=1, max_value=15, value=1, step=1)
    nodes_data, edges_data, pos = data_processing.gerar_dados_grafo(adj_matrix, threshold=threshold_adj, text_matrix=text_matrix)
    fig_grafo = visualizations.plot_network_graph(nodes_data, edges_data, f"Rede de Carreiras (Adjacência >= {threshold_adj})", cargos_destaque=cargos_destaque)
    st.plotly_chart(fig_grafo, use_container_width=True)
    if st.session_state.get('show_explanations', False):
        st.info(explanations.get_explanation("grafo", st.session_state.get('explanation_tone', 'tecnico')))

    st.markdown("---")

    # 1.5. Mapa de Calor Gower
    if is_sample_biased:
        st.warning(explanations.get_short_bias_warning(), icon="🚨")
    st.subheader("1.5. Mapa de Calor de Similaridade (Distância de Gower)", help="**Como interpretar o Mapa:** Visão térmica do distanciamento. Áreas vermelhas representam cargos idênticos (Distância próxima de 0.0).\n\n**Cálculo:** Diferente da adjacência (contagem bruta), este usa o Coeficiente de Gower entre 0 e 1, cruzando arrays de presenças (1) e ausências (0) penalizando distorções.")
    
    df_para_gower = df_to_use.copy()
    if incluir_comuns:
        num_cargos_reais = len(df_para_gower)
        numeric_cols = df_para_gower.select_dtypes(include='number').columns
        pseudo_row = (df_para_gower[numeric_cols].sum(axis=0) == num_cargos_reais).astype(int)
        if 'Carreira' in df_para_gower.columns:
            pseudo_row['Carreira'] = "Policial Civil (todos os cargos)"
        pseudo_row.name = "Policial Civil (todos os cargos)"
        df_para_gower.loc[pseudo_row.name] = pseudo_row
        
    df_gower = data_processing.calcular_distancias_gower(df_para_gower)
    
    fig_gower_heat = visualizations.plot_gower_heatmap(df_gower, f"Matriz de Distância de Gower - {cenario_sel}", cargos_destaque=cargos_destaque)
    st.plotly_chart(fig_gower_heat, use_container_width=True)
    if st.session_state.get('show_explanations', False):
        st.info(explanations.get_explanation("gower", st.session_state.get('explanation_tone', 'tecnico')))

    st.markdown("---")
    
    # 1.6. Régua Gower
    if is_sample_biased:
        st.warning(explanations.get_short_bias_warning(), icon="🚨")
    st.subheader("1.6. Régua de Similaridade Relativa (Distância de Gower)", help="**Como interpretar a Régua:** Fixando um cargo central na marca 'Zero', mapeia o afastamento de todas as outras carreiras.\n\n**Cálculo:** Diferente da adjacência (contagem bruta), este usa o Coeficiente de Gower entre 0 e 1, cruzando arrays de presenças (1) e ausências (0) penalizando distorções.")

    ref_cargo = st.selectbox(
        "Selecione o Cargo de Referência para a Régua:", 
        df_gower.columns, 
        index=0,
        format_func=lambda x: f"{x} (usado no artigo)" if x == "Delegado de Polícia" else x
    )
    fig_gower_ruler = visualizations.plot_gower_ruler(df_gower, reference_career=ref_cargo, cargos_destaque=cargos_destaque)
    st.plotly_chart(fig_gower_ruler, use_container_width=True)
    if st.session_state.get('show_explanations', False):
        st.info(explanations.get_explanation("regua", st.session_state.get('explanation_tone', 'tecnico')))

    st.markdown("---")

    # 1.7. Dendograma
    if is_sample_biased:
        st.warning(explanations.get_short_bias_warning(), icon="🚨")
    st.subheader("1.7. Árvore Hierárquica (Dendograma)", help="**Como interpretar:** Classifica e agrupa sub-blocos de carreiras que possuem alta afinidade. Se duas carreiras se conectam mais para baixo (mais à esquerda nos eixos X), significa que são funcionalmente muito idênticas e foram agrupadas primeiro na base.\n\n**Cálculo:** Utiliza Algoritmo de Clusterização Hierárquica sobre as métricas da Matriz de Gower. Foi utilizado o método aglomerativo *Single-linkage*, que calcula a distância mínima entre membros de grupos adjacentes.")
    st.markdown("Agrupamento hierárquico das distâncias de Gower usando o método *single*.")
    if len(df_gower.columns) > 1:
        fig_dendro = visualizations.plot_dendrogram(df_gower, f"Dendograma Gower - {cenario_sel}", cargos_destaque=cargos_destaque)
        st.plotly_chart(fig_dendro, use_container_width=True)
    else:
        st.warning("Selecione mais de um cargo para gerar a árvore hierárquica.")

    if st.session_state.get('show_explanations', False):
        st.info(explanations.get_explanation("dendograma", st.session_state.get('explanation_tone', 'tecnico')))

    st.markdown("---")

    # 1.8. UpSet Plot (Alternativa ao Venn)
    if is_sample_biased:
        st.warning(explanations.get_short_bias_warning(), icon="🚨")
    st.subheader("1.8. Diagrama de Conjuntos (Interseções Exatas)", help="**Como interpretar:** Funciona como um 'Diagrama de Venn' escalável. Ele varre as centenas de combinações possíveis entre os cargos e lista as maiores fatias em comum. A barra revela exatamente quantas atribuições aquele 'bloco' de cargos exclusivo possui.\n\n**Por que não usar um Diagrama de Venn circular?** Matematicamente, círculos só conseguem se sobrepor em todas as permutações para, no máximo, 4 conjuntos. Como possuímos 14 cargos diferentes, um Venn seria geometricamente impossível de ser desenhado sem violar as leis espaciais. Este formato (UpSet Plot) é o padrão ouro na visualização multicamadas na Ciência de Dados.")
    
    df_upset = df_original_limpo.set_index('Carreira') if 'Carreira' in df_original_limpo.columns else df_original_limpo.copy()
    fig_upset = visualizations.plot_upset_bar_chart(df_upset, f"Top Interseções Normativas (Granular) - {cenario_sel}", cargos_destaque=cargos_destaque)
    st.plotly_chart(fig_upset, use_container_width=True)
    
    if st.session_state.get('show_explanations', False):
        st.info(explanations.get_explanation("upset", st.session_state.get('explanation_tone', 'tecnico')))

else:
    st.error("Cenário indisponível.")

# Padding para não esconder gráficos atrás do botão de rodapé
st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)


