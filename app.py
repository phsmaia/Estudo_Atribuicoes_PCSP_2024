import streamlit as st
import data_loader
import data_processing
import visualizations

# Configuração Básica da Página
st.set_page_config(page_title="Estudo de Atribuições PCSP", layout="wide", initial_sidebar_state="expanded")

st.title("Painel Interativo: Estudo de Atribuições da PCSP (2024)")
st.markdown("Este painel apresenta de forma transparente as semelhanças e distinções entre os cargos da Polícia Civil do Estado de São Paulo, baseando-se em editais, legislação e propostas de reestruturação.")

# --- BARRA LATERAL (GLOSSÁRIO E OPÇÕES) ---
with st.sidebar:
    st.header("⚙️ Opções de Visualização")
    
    # Seletor de Cenário
    cenario_selecionado = st.selectbox(
        "Selecione o Cenário Analítico:",
        [
            "Atual Sem Correção",
            "Atual Com Correção",
            "LONPC Sem Correção",
            "LONPC Com Correção",
            "Reestruturação 2024"
        ]
    )
    
    st.markdown("---")
    st.header("📖 Glossário Público")
    with st.expander("O que são os Cenários?"):
        st.markdown("""
        - **Atual Sem Correção**: Lê os editais originais de concursos de forma literal, mesmo havendo omissões históricas.
        - **Atual Com Correção**: Ajusta as omissões óbvias dos editais baseando-se na realidade prática atual (ex: atribuições inerentes a cargos policiais).
        - **LONPC**: Lei Orgânica Nacional das Polícias Civis, que propõe agrupamentos e novas diretrizes para as corporações do Brasil.
        - **Reestruturação 2024**: Proposta específica do estado de SP para aglutinar e reformular carreiras em 2024.
        """)
        
    with st.expander("O que é a Tabela Condensada?"):
        st.markdown("""
        Atribuições que aparecem exatamente da mesma forma para exatamente os mesmos cargos são aglutinadas (condensadas) matematicamente em uma única "Macro Atribuição". 
        Isso evita que uma repetição de textos nos editais crie um falso peso ("viés") nas nossas análises de similaridade.
        """)

# --- CARREGAMENTO DE DADOS ---
# Utilizando as funções em cache para alta performance.
datasets = data_loader.get_all_datasets()

mapa_cenarios = {
    "Atual Sem Correção": datasets["atual_sem_correcao"],
    "Atual Com Correção": datasets["atual_com_correcao"],
    "LONPC Sem Correção": datasets["lonpc_sem_correcao"],
    "LONPC Com Correção": datasets["lonpc_com_correcao"],
    "Reestruturação 2024": datasets["reestruturacao"]
}

df_cenario = mapa_cenarios.get(cenario_selecionado)

if df_cenario is None or df_cenario.empty:
    st.error("Erro ao carregar o cenário selecionado. Verifique os arquivos na pasta.")
    st.stop()

# --- PROCESSAMENTO MATEMÁTICO DINÂMICO ---
st.header(f"Visualizando: {cenario_selecionado}")

# Abas para separar a visualização Original da Condensada
tab1, tab2, tab3 = st.tabs(["📊 Matriz de Atribuições (Original)", "🔬 Matriz Condensada (Sem Viés)", "🔗 Correlação entre Carreiras"])

with tab1:
    st.subheader("Matriz Binária Original")
    st.info("Esta tabela mostra 1 (verde) se a carreira possui a atribuição, e 0 (azul escuro/branco dependendo do tema) se não possui. As atribuições comuns a absolutamente todos os cargos foram matematicamente removidas para não distorcer a análise de diferenciação.")
    
    # Processamento e Plotagem
    df_original_limpo = data_processing.remover_atribuicoes_comuns(df_cenario)
    fig_original = visualizations.plot_binary_heatmap(df_original_limpo, "Matriz de Atribuições (Excluindo Comuns)")
    st.plotly_chart(fig_original, use_container_width=True)

with tab2:
    st.subheader("Matriz Binária Condensada")
    st.info("Neste cenário, as atribuições foram compactadas para evitar peso excessivo em repetições. Por exemplo, se duas tarefas são realizadas somente por Peritos e Médicos Legistas conjuntamente, elas viram uma única coluna indicadora.")
    
    # Processamento (Cacheado dinamicamente caso mude o dataframe)
    df_condensado, historico = data_processing.condensar_dataframe(df_cenario)
    
    # Exibir a plotagem interativa
    fig_condensada = visualizations.plot_binary_heatmap(df_condensado, "Matriz Condensada de Atribuições", colorscale="PRGn")
    st.plotly_chart(fig_condensada, use_container_width=True)
    
    # Exibir matemática explicita
    st.markdown("### Matemática por trás da Condensação")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total de Atribuições Originais", value=len(df_original_limpo.columns))
    with col2:
        st.metric(label="Total de Atribuições após Condensar", value=len(df_condensado.columns))
        
    with st.expander("Ver o Log Matemático de Condensações (Apenas para Curiosos)"):
        for item in historico:
            st.text(item)

with tab3:
    st.subheader("Distância e Similaridade (Correlação de Pearson)")
    st.info("A matriz abaixo não usa distâncias complexas como Gower neste momento, mas uma correlação simples e robusta (Pearson) baseada nas marcações de presença/ausência (0 e 1). Quanto mais próximo de 1.0 (vermelho), mais similares são as carreiras na teoria dos editais.")
    
    # Matriz de Correlação baseada no condensado
    matriz_corr = data_processing.gerar_matriz_correlacao(df_condensado)
    fig_corr = visualizations.plot_correlation_heatmap(matriz_corr, "Correlação entre Carreiras")
    st.plotly_chart(fig_corr, use_container_width=True)
