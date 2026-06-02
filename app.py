import streamlit as st
import data_loader
import data_processing
import visualizations
import logger

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
    st.title("⚙️ Painel de Controle")
    st.markdown("Configure a renderização analítica do modelo de Atribuições da PCSP.")
    
    cenario_sel = st.selectbox("Selecione o Cenário:", opcoes_cenarios)
    df_cenario = mapa_cenarios.get(cenario_sel)
    
    st.markdown("---")
    
    tipo_matriz = st.radio("Formato da Matriz:", ["Condensada", "Original"], horizontal=True)
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
        st.markdown("**Indicadores de Redução**")
        kpi1, kpi2 = st.columns(2)
        kpi1.metric(label="Originais", value=len(df_original_limpo.columns))
        kpi2.metric(label="Condensadas", value=len(df_condensado.columns), delta=f"{len(df_condensado.columns) - len(df_original_limpo.columns)}", delta_color="inverse")
        
        st.markdown("---")
        st.markdown("### 🔗 Referências e Contato")
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/phsmaia/Estudo_Atribuicoes_PCSP_2024)")
        st.markdown("[![Artigo](https://img.shields.io/badge/Artigo_Científico-0056D2?style=for-the-badge&logo=googlescholar&logoColor=white)](https://periodicos.pf.gov.br/index.php/RBCP/pt_BR/article/view/4693)")
        st.markdown("[![Zenodo](https://img.shields.io/badge/Zenodo-024E70?style=for-the-badge&logo=zenodo&logoColor=white)](https://zenodo.org/records/14284483)")
        st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedromaiapapilodata/)")

    # 2. Matriz de Atribuições
    st.subheader(f"1. Matriz de Atribuições ({tipo_matriz})", help="**Como interpretar:** Exibe o valor '1' se o cargo possui a atribuição normativa e '0' caso não possua. \n\n**Cálculo:** Construída lendo os manuais e editais. No modo 'Condensada', a matriz aglutina atribuições que possuem o exato mesmo padrão de repetição (ex: atribuições comuns a um mesmo grupo de cargos viram uma única coluna com peso 1) para evitar que redundâncias documentais criem distorções de peso estatístico.")
    st.info("Passe o mouse nas células para ler a atribuição completa.")
    fig_bin = visualizations.plot_binary_heatmap(df_to_use_siglas, f"Matriz {tipo_matriz} - {cenario_sel}", colorscale="Teal", dic_reverso=dic_reverso)
    st.plotly_chart(fig_bin, use_container_width=True)
    
    st.markdown("---")

    # 3. Adjacência
    st.subheader("2. Matriz de Adjacência (Atribuições Compartilhadas)", help="**Como interpretar:** Exibe a contagem absoluta de quantas atribuições normativas dois cargos distintos compartilham entre si. Valores mais altos (cores fortes) indicam forte justaposição funcional.\n\n**Cálculo:** Feito através do Produto Escalar cruzando a Matriz de Atribuições contra si própria (sua transposta).")
    adj_matrix = data_processing.gerar_matriz_adjacencia(df_to_use)
    fig_adj = visualizations.plot_adjacency_heatmap(adj_matrix, f"Adjacência - {cenario_sel}", text_matrix=text_matrix)
    st.plotly_chart(fig_adj, use_container_width=True)

    st.markdown("---")

    # 4. Grafo de Similaridade
    st.subheader("3. Grafo de Similaridade (Baseado em Adjacência)", help="**Como interpretar:** Representação de rede onde as 'bolas' (nós) representam as carreiras policiais e as 'linhas' (arestas) indicam que há uma intersecção de funções. A espessura da linha simboliza a quantidade de funções compartilhadas.\n\n**Cálculo:** Renderizado pelo motor NetworkX com física Fruchterman-Reingold (Spring Layout), que cria forças de repulsão magnética entre os nós, permitindo que cargos altamente conectados 'puxem' uns aos outros para o centro do agrupamento (cluster).")
    threshold_adj = st.slider("Corte de Adjacência (Threshold de Conexões):", min_value=1, max_value=15, value=2, step=1)
    nodes_data, edges_data, pos = data_processing.gerar_dados_grafo(adj_matrix, threshold=threshold_adj, text_matrix=text_matrix)
    fig_grafo = visualizations.plot_network_graph(nodes_data, edges_data, f"Rede de Carreiras (Adjacência >= {threshold_adj})")
    st.plotly_chart(fig_grafo, use_container_width=True)

    st.markdown("---")

    # 5. Régua Gower
    st.subheader("4. Régua de Similaridade Relativa (Distância de Gower)", help="**Como interpretar:** Fixando um cargo central na marca 'Zero', mapeia o afastamento estatístico de todas as outras carreiras. Valores próximos de Zero demonstram alta comunhão de atribuições, enquanto valores que tangenciam 1.0 (ou mais distantes) revelam carreiras completamente díspares.\n\n**Cálculo:** Emprega o Coeficiente de Distância de Gower para dados mistos, cruzando os arrays de presenças (1) e ausências (0) de cada binômio de cargos na matriz.")
    df_gower = data_processing.calcular_distancias_gower(df_to_use)
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
    st.subheader("5. Árvore Hierárquica (Dendograma)", help="**Como interpretar:** Classifica e agrupa sub-blocos de carreiras que possuem alta afinidade. Se duas carreiras se conectam mais para baixo (mais à esquerda nos eixos X), significa que são funcionalmente muito idênticas e foram agrupadas primeiro na base.\n\n**Cálculo:** Utiliza Algoritmo de Clusterização Hierárquica sobre as métricas da Matriz de Gower. Foi utilizado o método aglomerativo *Single-linkage*, que calcula a distância mínima entre membros de grupos adjacentes.")
    st.markdown("Agrupamento hierárquico das distâncias de Gower usando o método *single*.")
    if len(df_gower.columns) > 1:
        fig_dendro = visualizations.plot_dendrogram(df_gower, f"Dendograma Gower - {cenario_sel}")
        st.plotly_chart(fig_dendro, use_container_width=True)
    else:
        st.warning("Selecione mais de um cargo para gerar a árvore hierárquica.")

    st.markdown("---")
    
    # 7. Explorador Dinâmico
    st.subheader("6. Explorador Dinâmico de Atribuições", help="**Como interpretar:** Permite cruzar dados manualmente simulando as tabelas dinâmicas do estudo original. Você pode descobrir quais cargos dividem funções específicas ou vice-versa.")
    
    df_explorer = df_to_use.set_index('Carreira') if 'Carreira' in df_to_use.columns else df_to_use.copy()
    
    aba1, aba2 = st.tabs(["Filtro por Cargo (O que eles compartilham?)", "Filtro por Atribuição (Quem faz isso?)"])
    
    with aba1:
        st.markdown("Selecione um ou mais cargos para visualizar as atribuições normativas que eles possuem e como elas se alinham.")
        filtro_cargos = st.multiselect("Cargos:", df_explorer.index.tolist(), key="filtro_cargos_aba1")
        if filtro_cargos:
            # Filtra e transpõe (Atribuições nas linhas, cargos nas colunas)
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
                
            # Troca as siglas pelas descrições originais do dicionário
            df_resultado.index = [dic_reverso.get(col, col) for col in df_resultado.index]
            df_resultado.index.name = "Atribuição Normativa"
            
            st.dataframe(df_resultado, use_container_width=True)
            
    with aba2:
        st.markdown("Selecione uma ou mais atribuições para descobrir quais carreiras policiais as possuem formalmente em seus escopos.")
        # As colunas em df_explorer já são os textos descritivos originais
        todas_atrib = df_explorer.columns.tolist()
        filtro_atrib = st.multiselect("Atribuições:", todas_atrib, key="filtro_atrib_aba2")
        if filtro_atrib:
            
            # Filtra as atribuições selecionadas (chaves textuais originais) e apenas os cargos que as possuem
            df_filtro_atrib = df_explorer[filtro_atrib].copy()
            df_filtro_atrib = df_filtro_atrib[(df_filtro_atrib > 0).any(axis=1)]
            
            # Formatação
            df_filtro_atrib.columns = filtro_atrib
            df_filtro_atrib.index.name = "Carreira Policial"
            
            st.dataframe(df_filtro_atrib, use_container_width=True)

else:
    st.error("Cenário indisponível.")
