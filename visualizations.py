import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_binary_heatmap(df: pd.DataFrame, title: str, colorscale: str = "Teal") -> go.Figure:
    """
    Renderiza um mapa de calor interativo (Plotly) para as matrizes binárias de atribuições.
    A interatividade garante clareza (tooltips nas células).
    """
    df_temp = df.copy()
    if 'Carreira' in df_temp.columns:
        df_temp = df_temp.set_index('Carreira')
    
    # Garantir formato numérico
    df_temp = df_temp.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    fig = px.imshow(
        df_temp,
        labels=dict(x="Atribuição", y="Carreira", color="Possui Atribuição?"),
        x=df_temp.columns,
        y=df_temp.index,
        color_continuous_scale=colorscale,
        aspect="auto",
        title=title
    )
    
    # Ajuste de layout para legibilidade
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        title_font_size=20,
        margin=dict(l=150, r=20, t=50, b=150),
        coloraxis_showscale=False # Binário, a escala não é tão útil visualmente
    )
    
    # Ajuste dos ticks no eixo X para ficar vertical caso os textos sejam grandes
    fig.update_xaxes(tickangle=45)
    
    # Melhora do hover
    fig.update_traces(
        hovertemplate="<b>Carreira:</b> %{y}<br><b>Atribuição:</b> %{x}<br><b>Valor:</b> %{z}<extra></extra>"
    )
    
    return fig

def plot_correlation_heatmap(matriz_corr: pd.DataFrame, title: str) -> go.Figure:
    """
    Gera um mapa de calor de correlação estatística entre carreiras.
    """
    fig = px.imshow(
        matriz_corr,
        labels=dict(x="Carreira", y="Carreira", color="Correlação"),
        x=matriz_corr.columns,
        y=matriz_corr.index,
        color_continuous_scale="RdBu_r",
        aspect="auto",
        zmin=-1, zmax=1,
        title=title
    )
    fig.update_layout(
        title_font_size=20,
        margin=dict(l=100, r=20, t=50, b=100)
    )
    fig.update_traces(
        hovertemplate="<b>Carreira A:</b> %{y}<br><b>Carreira B:</b> %{x}<br><b>Correlação:</b> %{z:.2f}<extra></extra>"
    )
    return fig
