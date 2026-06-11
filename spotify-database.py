import pandas as pd

df = pd.read_csv("spotify-tracks.csv")
print(f"Linhas: {df.shape[0]} | Colunas: {df.shape[1]}\n")

print(f"=======Informações importantes=========")
df.info()
df.describe()

print("\nValores ausentes:")
print(df.isna().sum())
print(f"\nDuplicatas: {df.duplicated().sum()}")
print(f'=============Limpando...===================')
#joga fora colunas inuteis
df.drop(columns=["Unnamed: 0"], inplace=True, errors="ignore")

#joga fora linhas inuteis nas colunas que foram identificadas 
df.dropna(subset=["artists", "album_name", "track_name"], inplace=True)
print(df.isna().sum())

print(f"Dataset limpo! Linhas restantes: {len(df)}")

print(f"\n ======================================")

# Pergunta 1: Quais gêneros são mais populares?
print("\n1. Popularidade média por gênero:")
print(df.groupby("track_genre")["popularity"].mean().sort_values(ascending=False).round(2))
 
# Pergunta 2: Quais artistas têm mais faixas?
print("\n2. Artistas com mais faixas:")
print(df["artists"].value_counts().head(10))
 
 
# Pergunta 3: Danceability e energy por gênero
print("\n4. Danceability e energy por gênero:")
print(df.groupby("track_genre")[["danceability", "energy"]].mean().sort_values("danceability", ascending=False).round(3))
 
# Pergunta 4: Top 10 faixas mais populares
print("\n5. Top 10 faixas mais populares:")
print(df[["track_name", "artists", "popularity"]].sort_values("popularity", ascending=False).head(10).to_string(index=False))


# Gráficos planejados:
#   1. Barras — Popularidade média por gênero
#      Por quê: mostra de forma direta qual gênero domina o Spotify.
#
#   2. Scatter — Danceability vs Energy (colorido por gênero)
#      Por quê: revela clusters entre gêneros (ex: hip-hop vs classical).
#
#   3. Histograma — Distribuição de popularidade
#      Por quê: mostra se as músicas se concentram em alta ou baixa popularidade.
#
#   4. Box Plot — Valence por gênero
#      Por quê: compara a "positividade emocional" entre os gêneros.
#
#   5. Donut — Proporção de músicas explícitas
#      Por quê: visual e rápido para comparar gêneros mais/menos explícitos.
