import streamlit as st
import pandas as pd
import data_loader
import data_processing
import visualizations
import logger
import contact_manager

# Iniciar o banco de dados de log
logger.init_db()

# Configuração Básica da Página
st.set_page_config(page_title="Estudo de Atribuições PCSP", layout="wide", initial_sidebar_state="expanded")

# Injeção de CSS para destaques críticos (Transparência Matemática)
st.markdown("""
<style>
/* Animação Premium: Fade & Focus (Sem alteração geométrica) */
@keyframes smoothCascadeFocus {
    0% { 
        opacity: 0; 
        filter: blur(5px); 
    }
    100% { 
        opacity: 1; 
        filter: blur(0); 
    }
}

div[data-testid="stVerticalBlock"] > div {
    opacity: 0; 
    animation: smoothCascadeFocus 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Trava global contra barras de rolagem artificiais induzidas por transformações geométricas */
.stApp {
    overflow-x: hidden;
}

/* Atrasos escalonados para criar o efeito cascata premium */
div[data-testid="stVerticalBlock"] > div:nth-child(1) { animation-delay: 0.05s; }
div[data-testid="stVerticalBlock"] > div:nth-child(2) { animation-delay: 0.15s; }
div[data-testid="stVerticalBlock"] > div:nth-child(3) { animation-delay: 0.25s; }
div[data-testid="stVerticalBlock"] > div:nth-child(4) { animation-delay: 0.35s; }
div[data-testid="stVerticalBlock"] > div:nth-child(5) { animation-delay: 0.45s; }
div[data-testid="stVerticalBlock"] > div:nth-child(6) { animation-delay: 0.55s; }
div[data-testid="stVerticalBlock"] > div:nth-child(7) { animation-delay: 0.65s; }
div[data-testid="stVerticalBlock"] > div:nth-child(8) { animation-delay: 0.75s; }
div[data-testid="stVerticalBlock"] > div:nth-child(9) { animation-delay: 0.85s; }
div[data-testid="stVerticalBlock"] > div:nth-child(10) { animation-delay: 0.95s; }

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

/* Sidebar QoL e Compactação Visual */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.5rem !important; 
}
[data-testid="stSidebar"] hr {
    margin: 0.2em 0 !important; 
}
[data-testid="stSidebar"] .block-container {
    padding-top: 2rem !important;
    padding-bottom: 0.5rem !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
    position: absolute !important;
    top: 0;
    right: 0;
    padding: 0.5rem !important;
    z-index: 999;
}
[data-testid="stSidebar"] h3 {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
/* Redução do tamanho das badges (imagens de contato) */
[data-testid="stSidebar"] [data-testid="stExpander"] img {
    transform: scale(0.85);
    transform-origin: left center;
    margin-bottom: -5px;
}
/* Mantém o ícone de interrogação colado no texto do toggle */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    align-items: center !important;
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

# --- CONTROLES LATERAIS (SIDEBAR) ---
with st.sidebar:
    st.markdown("### ⚙️ Painel de Controle")
    
    cenario_sel = st.selectbox("Selecione o Cenário:", opcoes_cenarios)
    df_cenario = mapa_cenarios.get(cenario_sel)
    
    st.markdown("---")
    
    st.markdown("**Opções**")
    incluir_comuns = st.toggle("Incluir Atribuições Genéricas a Todos", value=False, help="Se ativado, não oculta as atribuições normativas comuns a todos os cargos e desabilita o formato Condensado.")
    tipo_matriz_raw = st.radio(
        "Formato da Matriz:", 
        ["Condensada (Aglutina repetições)", "Original (Dados brutos)"], 
        horizontal=True, 
        disabled=incluir_comuns,
        help="**Condensada:** Junta funções que aparecem no mesmo exato grupo de cargos em uma única coluna com peso concentrado, para que dezenas de atribuições redundantes não distorçam os cálculos matemáticos.\n\n**Original:** Mantém os dados da base exatamente como foram extraídos dos manuais e editais normativos."
    )
    
    tipo_matriz = "Original" if "Original" in tipo_matriz_raw else "Condensada"
    
    # Se incluir comuns está ativo, forçamos Original
    if incluir_comuns:
        tipo_matriz = "Original"
        
    expandir_textos = st.checkbox("Expandir textos nos tooltips", value=False, help="Se ativo, renderiza os nomes completos das atribuições no hover (pode gerar grandes blocos de texto). Se inativo, exibe as siglas matemáticas (A_01, A_02).")
    
    st.markdown("---")
    
    if df_cenario is not None and not df_cenario.empty:
        cargos_disponiveis = df_cenario['Carreira'].tolist() if 'Carreira' in df_cenario.columns else df_cenario.index.tolist()
        cargos_selecionados = st.multiselect("Cargos a Analisar (vazio = todos):", cargos_disponiveis)
        
        # Loga a visita de forma invisível via backend
        logger.log_visit(cenario_sel)

# --- MÓDULO DE DASHBOARD VERTICAL ---
st.title("Painel Interativo: Estudo de Atribuições da PCSP (2024)")
st.markdown("<div class='transparency-box'><h4>Suposição Matemática Ativa</h4><p>As matrizes abaixo transformam listas de atribuições textuais em coordenadas numéricas. Ao passarem pela 'Condensação', repetições exatas entre os mesmos cargos viram uma única coluna. Isso impede que atribuições divididas em 10 itens no edital mas que significam a mesma coisa causem 'peso artificial' que aproxima duas carreiras incorretamente.</p></div>", unsafe_allow_html=True)

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
        # Se comum, o DataFrame limpo é o próprio cenário com tudo!
        # Mas vamos ordenar as colunas comuns para o início
        col_sums = df_cenario.sum(axis=0)
        num_reais = len(df_cenario)
        colunas_comuns = df_cenario.columns[col_sums == num_reais].tolist()
        colunas_outras = [c for c in df_cenario.columns if c not in colunas_comuns]
        df_original_limpo = df_cenario[colunas_comuns + colunas_outras].copy()
        
        # O Condensado é desabilitado visualmente, mas deixamos preenchido para evitar quebra de variável
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
    
    # Matriz de Textos para Tooltips
    text_matrix = data_processing.obter_atribuicoes_comuns_textuais(df_to_use, dic_siglas, expandir_textos)

    # 1. KPIs (Sidebar)
    with st.sidebar:
        st.markdown("---")
        reducao = len(df_original_limpo.columns) - len(df_condensado.columns)
        pct_reducao = (reducao / len(df_original_limpo.columns)) * 100 if len(df_original_limpo.columns) > 0 else 0
        
        # Uso de Flexbox nativo para garantir a mesma linha de altura e evitar truncamento "Condensa..."
        html_kpis = f"""
        <div style="display: flex; justify-content: space-between; align-items: center; text-align: center; margin-bottom: 0.5rem;">
            <div>
                <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Originais</div>
                <div style="font-size: 1.1rem; line-height: 1.2;">{len(df_original_limpo.columns)}</div>
            </div>
            <div>
                <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Condensadas</div>
                <div style="font-size: 1.1rem; line-height: 1.2;">{len(df_condensado.columns)}</div>
            </div>
            <div>
                <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Redução</div>
                <div style="font-size: 1.1rem; color: #00C851; line-height: 1.2; font-weight: bold;">{reducao}</div>
            </div>
            <div>
                <div style="font-size: 0.65rem; color: #9E9E9E; font-weight: 600; text-transform: uppercase;">Eficácia</div>
                <div style="font-size: 1.1rem; color: #00C851; line-height: 1.2; font-weight: bold;">{pct_reducao:.1f}%</div>
            </div>
        </div>
        """
        st.markdown(html_kpis, unsafe_allow_html=True)
        
        st.markdown("---")
        with st.expander("🔗 Referências e Contato", expanded=False):
            st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/phsmaia/Estudo_Atribuicoes_PCSP_2024)")
            st.markdown("[![Artigo](https://img.shields.io/badge/Artigo_Científico-0056D2?style=for-the-badge&logo=googlescholar&logoColor=white)](https://periodicos.pf.gov.br/index.php/RBCP/pt_BR/article/view/4693)")
            st.markdown("[![Zenodo](https://img.shields.io/badge/Zenodo-024E70?style=for-the-badge&logo=zenodo&logoColor=white)](https://zenodo.org/records/14284483)")
            st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedromaiapapilodata/)")
            
            st.markdown("---")
            st.markdown("**✉️ Fale com o Autor**")
            with st.form("contact_form", clear_on_submit=True):
                c_nome = st.text_input("Nome*")
                c_email = st.text_input("E-mail*")
                c_inst = st.text_input("Instituição")
                c_func = st.text_input("Função")
                c_assunto = st.text_input("Assunto*")
                c_msg = st.text_area("Mensagem*")
                enviou = st.form_submit_button("Enviar Mensagem")
                
            if enviou:
                if not c_nome or not c_email or not c_assunto or not c_msg:
                    st.error("Preencha todos os campos obrigatórios (*).")
                else:
                    with st.spinner("Processando..."):
                        salvou_db = contact_manager.save_contact_message(
                            c_nome, c_email, c_inst, c_func, c_assunto, c_msg
                        )
                        if salvou_db:
                            st.success("Salvo no banco de dados com segurança!")
                            # Tenta enviar o email
                            email_ok, email_status = contact_manager.send_contact_email(
                                c_nome, c_email, c_inst, c_func, c_assunto, c_msg
                            )
                            if email_ok:
                                st.success("E-mail disparado para o autor!")
                            else:
                                st.warning(f"Salvo localmente, mas falha no e-mail: {email_status}")
                        else:
                            st.error("Falha ao acessar o banco de dados interno.")

    # 2. Matriz de Atribuições
    st.subheader(f"1. Matriz de Atribuições ({tipo_matriz})", help="**Como interpretar:** Exibe o valor '1' se o cargo possui a atribuição normativa e '0' caso não possua. \n\n**Cálculo:** Construída lendo os manuais e editais. No modo 'Condensada', a matriz aglutina atribuições que possuem o exato mesmo padrão de repetição (ex: atribuições comuns a um mesmo grupo de cargos viram uma única coluna com peso 1) para evitar que redundâncias documentais criem distorções de peso estatístico.")
    st.info("Passe o mouse nas células para ler a atribuição completa.")
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
        filtro_cargos = st.multiselect("Cargos:", df_explorer.index.tolist(), key="filtro_cargos_aba1")
        if filtro_cargos:
            # Filtra e transpõe
            df_filtro = df_explorer.loc[filtro_cargos]
            colunas_ativas = df_filtro.columns[(df_filtro > 0).any()]
            df_resultado = df_filtro[colunas_ativas].T
            
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
    threshold_adj = st.slider("Corte de Adjacência (Threshold de Conexões):", min_value=1, max_value=15, value=2, step=1)
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
