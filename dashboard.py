import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações da pagina.
st.set_page_config(page_title="Spotify Analytics", page_icon="🎵", layout="wide")
@st.cache_data
def load_data():
    df = pd.read_csv("spotify-tracks.csv")
    
    df.drop(columns=["Unnamed: 0"], inplace=True, errors="ignore")
    df.dropna(subset=["artists", "album_name", "track_name"], inplace=True)
    return df

df = load_data()


st.title("🎵 Dashboard de Análise: Spotify")
st.markdown("Uma visão interativa sobre gêneros, popularidade e características das faixas.")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral", 
    "📈 Popularidade", 
    "🎧 Características de Áudio", 
    "🔞 Musicas mais inapropriadas"
])

with tab1:
    st.header("Visão Geral do Dataset")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Faixas", f"{len(df):,}") #numero de linhas
    col2.metric("Total de Artistas", df["artists"].nunique()) # artistas unicos
    col3.metric("Total de Gêneros", df["track_genre"].nunique()) # generos unicos

    st.divider()

    colA, colB = st.columns(2)
    with colA:
        st.subheader("Top 10 Faixas Mais Populares")
        top_faixas = df[["track_name", "artists", "popularity"]].sort_values("popularity", ascending=False).head(10)
        st.dataframe(top_faixas, hide_index=True)
    with colB:
        st.subheader("Artistas com Mais Faixas")
        top_artistas = df["artists"].value_counts().head(10).reset_index()
        top_artistas.columns = ["Artista", "Qtd de Faixas"]
        st.dataframe(top_artistas, hide_index=True)

with tab2:
    
    # Gráfico 1 (Planejado): Barras - Popularidade média por gênero
    st.subheader("Top 20 Gêneros Mais Populares (Média)")
    top_generos = df.groupby("track_genre")["popularity"].mean().sort_values(ascending=False).head(20).reset_index()
    barras = px.bar(top_generos, x="track_genre", y="popularity", 
                     title="Média de Popularidade por Gênero",
                     color="popularity", color_continuous_scale="Viridis")
    st.plotly_chart(barras)

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
    
    # Danceability vs Energy
    st.subheader("Dançabilidade vs Energia")
    fig_scatter = px.scatter(df_filtrado, x="danceability", y="energy", color="track_genre",
                             hover_data=["track_name", "artists"], opacity=0.6,
                             title="Clusters de Gêneros Musicais")
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab4:
    st.header("Músicas Explícitas")
    
    # Donut
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Proporção Geral")
        explicito_counts = df["explicit"].value_counts().reset_index()
        explicito_counts.columns = ["Explícito", "Quantidade"]
        # Convertendo boolean para texto para ficar bonito no gráfico
        explicito_counts["Explícito"] = explicito_counts["Explícito"].map({True: "Sim", False: "Não"})
        
        fig_pizza = px.pie(explicito_counts, names="Explícito", values="Quantidade",
                           title="Dataset: Explícito vs Não Explícito",
                           color="Explícito", color_discrete_map={"Sim": "red", "Não": "#1DB954"})
        st.plotly_chart(fig_pizza)
        
    with col2:
        st.subheader("Gêneros com mais músicas explícitas")
        # Porcentagem de músicas explícitas por gênero
        exp_gen = df.groupby("track_genre")["explicit"].mean().sort_values(ascending=False).head(10).reset_index()
        exp_gen["explicit"] = exp_gen["explicit"] * 100 # Transforma em porcentagem
        
        fig_bar_exp = px.bar(exp_gen, x="track_genre", y="explicit",
                             title="Top 10 Gêneros (% Explícito)",
                             labels={"explicit": "% Explícito", "track_genre": "Gênero"})
        st.plotly_chart(fig_bar_exp)