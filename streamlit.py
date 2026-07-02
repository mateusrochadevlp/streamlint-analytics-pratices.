import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração inicial da página
st.set_page_config(page_title="Spotify Analytics", page_icon="🎵", layout="wide")

st.title("🎵 Dashboard de Análise: Spotify")
st.markdown("Uma visão interativa sobre gêneros, popularidade e características das faixas.")

# 2. Carregamento e Limpeza de Dados (Usando cache para não travar o app)
@st.cache_data
def load_data():
    df = pd.read_csv("spotify-tracks.csv")
    
    # Limpeza (baseada no seu script original)
    df.drop(columns=["Unnamed: 0"], inplace=True, errors="ignore")
    df.dropna(subset=["artists", "album_name", "track_name"], inplace=True)
    return df

df = load_data()

# 3. Criando as Abas para organizar a apresentação
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral", 
    "📈 Popularidade", 
    "🎧 Características de Áudio", 
    "🔞 Conteúdo Explícito"
])

# ==========================================
# ABA 1: VISÃO GERAL
# ==========================================
with tab1:
    st.header("Visão Geral do Dataset")
    
    # Exibindo métricas rápidas (KPIs)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Faixas", f"{len(df):,}")
    col2.metric("Total de Artistas", df["artists"].nunique())
    col3.metric("Total de Gêneros", df["track_genre"].nunique())
    
    st.divider()
    
    colA, colB, colC = st.columns(2)
    with colA:
        st.subheader("Top 10 Faixas Mais Populares")
        top_faixas = df[["track_name", "artists", "popularity"]].sort_values("popularity", ascending=False).head(10)
        st.dataframe(top_faixas, use_container_width=True, hide_index=True)
        
    with colB:
        st.subheader("Artistas com Mais Faixas")
        top_artistas = df["artists"].value_counts().head(10).reset_index()
        top_artistas.columns = ["Artista", "Qtd de Faixas"]
        st.dataframe(top_artistas, use_container_width=True, hide_index=True)



# ==========================================
# ABA 2: POPULARIDADE
# ==========================================
with tab2:
    st.header("Análise de Popularidade")
    
    # Gráfico 3 (Planejado): Histograma - Distribuição de popularidade
    st.subheader("Distribuição da Popularidade das Músicas")
    fig_hist = px.histogram(df, x="popularity", nbins=50, 
                            title="Concentração de Músicas por Nota de Popularidade",
                            color_discrete_sequence=["#1DB954"]) # Cor do Spotify
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Gráfico 1 (Planejado): Barras - Popularidade média por gênero
    # Dica: Como há muitos gêneros, vamos pegar apenas os 20 mais populares para o gráfico não ficar poluído
    st.subheader("Top 20 Gêneros Mais Populares (Média)")
    pop_genero = df.groupby("track_genre")["popularity"].mean().sort_values(ascending=False).head(20).reset_index()
    fig_bar = px.bar(pop_genero, x="track_genre", y="popularity", 
                     title="Média de Popularidade por Gênero",
                     color="popularity", color_continuous_scale="Viridis")
    st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# ABA 3: CARACTERÍSTICAS DE ÁUDIO
# ==========================================
with tab3:
    st.header("Entendendo a Vibe das Músicas")
    
    # Filtro para não travar o Scatter Plot 
    st.write("Selecione alguns gêneros para comparar:")
    generos_selecionados = st.multiselect(
        "Gêneros:", 
        options=df["track_genre"].unique(),
        default=["pop", "classical", "hip-hop", "rock", "jazz"]
    )
    
    df_filtrado = df[df["track_genre"].isin(generos_selecionados)]
    
    # Gráfico 2 (Planejado): Scatter - Danceability vs Energy
    st.subheader("Dançabilidade vs Energia")
    fig_scatter = px.scatter(df_filtrado, x="danceability", y="energy", color="track_genre",
                             hover_data=["track_name", "artists"], opacity=0.6,
                             title="Clusters de Gêneros Musicais")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Gráfico 4 (Planejado): Box Plot - Valence por gênero
    st.subheader("Valence (Positividade Emocional) por Gênero")
    fig_box = px.box(df_filtrado, x="track_genre", y="valence", color="track_genre",
                     title="Distribuição da Positividade das Músicas")
    st.plotly_chart(fig_box, use_container_width=True)

# ==========================================
# ABA 4: CONTEÚDO EXPLÍCITO
# ==========================================
with tab4:
    st.header("Músicas Explícitas")
    
    # Gráfico 5 (Planejado): Donut - Proporção de músicas explícitas
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Proporção Geral")
        explicito_counts = df["explicit"].value_counts().reset_index()
        explicito_counts.columns = ["Explícito", "Quantidade"]
        # Convertendo boolean para texto para ficar bonito no gráfico
        explicito_counts["Explícito"] = explicito_counts["Explícito"].map({True: "Sim", False: "Não"})
        
        fig_donut = px.pie(explicito_counts, names="Explícito", values="Quantidade", hole=0.5,
                           title="Dataset: Explícito vs Não Explícito",
                           color="Explícito", color_discrete_map={"Sim": "red", "Não": "#1DB954"})
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col2:
        st.subheader("Gêneros com mais músicas explícitas")
        # Porcentagem de músicas explícitas por gênero
        exp_gen = df.groupby("track_genre")["explicit"].mean().sort_values(ascending=False).head(10).reset_index()
        exp_gen["explicit"] = exp_gen["explicit"] * 100 # Transforma em porcentagem
        
        fig_bar_exp = px.bar(exp_gen, x="track_genre", y="explicit",
                             title="Top 10 Gêneros (% Explícito)",
                             labels={"explicit": "% Explícito", "track_genre": "Gênero"})
        st.plotly_chart(fig_bar_exp, use_container_width=True)