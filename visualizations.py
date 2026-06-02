import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_binary_heatmap(df: pd.DataFrame, title: str, colorscale: str = "Teal", dic_reverso: dict = None) -> go.Figure:
    """
    Renderiza um mapa de calor interativo (Plotly) para as matrizes binárias de atribuições.
    A interatividade garante clareza (tooltips nas células).
    """
    df_temp = df.copy()
    if 'Carreira' in df_temp.columns:
        df_temp = df_temp.set_index('Carreira')
    
    # Garantir formato numérico
    df_temp = df_temp.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # Criação de um hover text customizado
    hover_text = []
    for index, row in df_temp.iterrows():
        hover_row = []
        for col in df_temp.columns:
            # Pega o texto completo se o dic_reverso existir, senão usa a própria coluna
            nome_real = dic_reverso.get(col, col) if dic_reverso else col
            hover_row.append(f"<b>Carreira:</b> {index}<br><b>Atribuição:</b> {nome_real}<br><b>Valor:</b> {row[col]}")
        hover_text.append(hover_row)
        
    fig = go.Figure(data=go.Heatmap(
        z=df_temp.values,
        x=df_temp.columns,
        y=df_temp.index,
        colorscale=colorscale,
        xgap=1, ygap=1,
        text=hover_text,
        hoverinfo="text",
        showscale=False
    ))
    
    # Ajuste de layout para legibilidade
    fig.update_layout(
        title=title,
        title_font_size=20,
        margin=dict(l=150, r=20, t=50, b=150),
    )
    fig.update_yaxes(autorange="reversed")
    
    # Ajuste dos ticks no eixo X para ficar vertical caso os textos sejam grandes
    fig.update_xaxes(tickangle=45)
    
    return fig

def plot_correlation_heatmap(matriz_corr: pd.DataFrame, title: str) -> go.Figure:
    """
    Gera um mapa de calor de correlação estatística entre carreiras.
    """
    fig = go.Figure(data=go.Heatmap(
        z=matriz_corr.values,
        x=matriz_corr.columns,
        y=matriz_corr.index,
        colorscale="RdBu_r",
        zmin=-1, zmax=1,
        xgap=1, ygap=1,
        hovertemplate="<b>Carreira A:</b> %{y}<br><b>Carreira B:</b> %{x}<br><b>Correlação:</b> %{z:.2f}<extra></extra>"
    ))
    fig.update_layout(
        title=title,
        title_font_size=20,
        margin=dict(l=100, r=20, t=50, b=100)
    )
    return fig

def plot_network_graph(nodes_data: list, edges_data: list, title: str) -> go.Figure:
    """
    Renderiza um grafo interativo usando as coordenadas previamente calculadas pelo NetworkX.
    """
    # Arestas
    edge_traces = []
    for edge in edges_data:
        x0, y0 = next((n["x"], n["y"]) for n in nodes_data if n["id"] == edge["source"])
        x1, y1 = next((n["x"], n["y"]) for n in nodes_data if n["id"] == edge["target"])
        
        peso = edge["weight"]
        # Espessura escalonada via raiz quadrada para evitar linhas de 30px
        import math
        largura = max(0.5, 0.5 + math.sqrt(peso)) if peso > 0 else 0.5
        
        # O hovertext será mostrado no centro da aresta
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        
        edge_traces.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=largura, color='#888'),
            hoverinfo='none',
            mode='lines'
        ))
        
        # Ponto invisível no meio da linha para ativar o Hovertext
        texto_hover = f"<b>{edge['source']} ↔ {edge['target']}</b><br>Força: {peso:.2f}<br>Comum: {edge['hovertext']}"
        edge_traces.append(go.Scatter(
            x=[mid_x],
            y=[mid_y],
            mode='markers',
            marker=dict(size=0.1, color='rgba(0,0,0,0)'),
            text=[texto_hover],
            hoverinfo='text',
            showlegend=False
        ))

    node_x = [n["x"] for n in nodes_data]
    node_y = [n["y"] for n in nodes_data]
    node_text = [n["id"] for n in nodes_data]
    
    # Cores qualitativas para os nós
    node_colors = px.colors.qualitative.Plotly
    cores_nos = [node_colors[i % len(node_colors)] for i in range(len(nodes_data))]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        textposition="top center",
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=False,
            color=cores_nos,
            size=20,
            line_width=2))


    fig = go.Figure(data=edge_traces + [node_trace],
             layout=go.Layout(
                title=title,
                title_font_size=20,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    return fig

def plot_adjacency_heatmap(adj_matrix: pd.DataFrame, title: str, text_matrix: pd.DataFrame = None) -> go.Figure:
    """
    Gera um mapa de calor para a matriz de adjacência (número de atribuições em comum).
    """
    import numpy as np
    adj_array = adj_matrix.to_numpy(dtype=float, copy=True)
    np.fill_diagonal(adj_array, np.nan)
    adj_vis = pd.DataFrame(adj_array, index=adj_matrix.index, columns=adj_matrix.columns)
    
    # Se uma matriz de textos (atributos compartilhados) foi enviada, injetamos como customdata
    custom_data = text_matrix.values if text_matrix is not None else None
    
    hovertemplate = "<b>Carreira A:</b> %{y}<br><b>Carreira B:</b> %{x}<br><b>Atribuições em Comum:</b> %{z}<extra></extra>"
    if custom_data is not None:
        hovertemplate = "<b>Carreira A:</b> %{y}<br><b>Carreira B:</b> %{x}<br><b>Qtd. Atribuições:</b> %{z}<br><b>Comum:</b><br>%{customdata}<extra></extra>"
    
    fig = go.Figure(data=go.Heatmap(
        z=adj_vis.values,
        x=adj_vis.columns,
        y=adj_vis.index,
        customdata=custom_data,
        colorscale="YlGnBu",
        xgap=1, ygap=1,
        hovertemplate=hovertemplate
    ))
    fig.update_layout(
        title=title,
        title_font_size=20,
        margin=dict(l=100, r=20, t=50, b=100)
    )
    fig.update_yaxes(autorange="reversed")
    return fig

def plot_gower_ruler(df_gower: pd.DataFrame, reference_career: str = "Delegado de Polícia") -> go.Figure:
    """
    Cria uma régua 1D (Scatter plot) baseada na distância de Gower de todos os cargos
    em relação a um cargo de referência (Delegado de Polícia, assumindo x=0).
    """
    if reference_career not in df_gower.columns:
        return go.Figure()
    
    # Extrair as distâncias em relação ao cargo de referência
    dist_serie = df_gower[reference_career].sort_values()
    
    fig = go.Figure()
    
    # Adicionamos os pontos ao scatter. O eixo X é a distância, o eixo Y pode ser 0.
    # Mas para não encavalar, vamos escalonar o eixo Y por índice.
    fig.add_trace(go.Scatter(
        x=dist_serie.values,
        y=dist_serie.index,
        mode='markers',
        marker=dict(size=12, color=dist_serie.values, colorscale='Viridis', showscale=True),
        text=dist_serie.index,
        hovertemplate="<b>Carreira:</b> %{text}<br><b>Distância Gower (ref: " + reference_career + "):</b> %{x:.3f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=f"Régua de Distanciamento Relativo (Referência: {reference_career})",
        title_font_size=18,
        xaxis_title="Distância de Gower",
        yaxis_title=None,
        margin=dict(l=150, r=50, t=50, b=50),
        height=500,
        autosize=True
    )
    
    # Adicionando a linha da Média e Mediana para possibilitar um panorama geral
    media = dist_serie.mean()
    mediana = dist_serie.median()
    
    fig.add_vline(x=media, line_width=2, line_dash="dash", line_color="red", 
                  annotation_text=f"Média: {media:.3f}", annotation_position="top right")
    fig.add_vline(x=mediana, line_width=2, line_dash="dot", line_color="blue", 
                  annotation_text=f"Mediana: {mediana:.3f}", annotation_position="bottom right")
                  
    return fig

import plotly.figure_factory as ff
from scipy.spatial.distance import squareform

def plot_dendrogram(df_gower: pd.DataFrame, title: str) -> go.Figure:
    """
    Gera um dendograma a partir da matriz de distâncias de Gower.
    """
    # Certificar-se que a matriz é simétrica (a gower as vezes tem floats com infimas diferenças)
    dist_array = (df_gower.values + df_gower.values.T) / 2
    # Preencher a diagonal com exatos 0s
    import numpy as np
    np.fill_diagonal(dist_array, 0)
    
    labels = df_gower.index.tolist()
    
    # Squareform requer distância sem a diagonal
    condensed_dist = squareform(dist_array)
    
    # Para usar o Plotly, precisamos criar um linkage
    from scipy.cluster.hierarchy import linkage
    Z = linkage(condensed_dist, method='single')
    
    # Plotly figure factory aceita a matriz condensada ou dados crus.
    # Como já temos distâncias, a forma mais segura no Plotly é via scipy -> plotly dendrogram manual,
    # ou deixar o plotly calcular a hierarquia mas enviando a matriz squareform e uma função linkage custom.
    # Em implementações diretas:
    fig = ff.create_dendrogram(
        dist_array,
        labels=labels,
        orientation='left',
        linkagefun=lambda x: linkage(squareform(x) if x.ndim == 2 else x, method='single')
    )
    
    fig.update_layout(
        title=title,
        title_font_size=18,
        height=600,
        margin=dict(l=250, r=50, t=50, b=50),
        autosize=True
    )
    
    # Injetando as alturas nos ramos (Dendograma Plotly gera Scatters em formato de U)
    annotations = []
    for trace in fig.data:
        x = trace.x
        y = trace.y
        # No formato 'left', a linha vertical une os dois sub-ramos e seus X são idênticos
        if len(x) == 4 and len(y) == 4:
            if x[1] == x[2] and x[1] > 0:
                dist = x[1]
                mid_y = (y[1] + y[2]) / 2
                annotations.append(dict(
                    x=dist,
                    y=mid_y,
                    xref='x',
                    yref='y',
                    text=f"{dist:.2f}",
                    showarrow=False,
                    xanchor='left',
                    yanchor='middle',
                    font=dict(size=10, color="red"),
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor="rgba(0, 0, 0, 0)",
                    borderpad=2,
                    xshift=5
                ))
                
    fig.update_layout(annotations=annotations)
    
    return fig
