import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el archivo CSV que contiene los datos
df = pd.read_csv('.\data\mini.csv')

no_of_users_threshold = 4

def recommend_similar_movies(
        df: pd.DataFrame,
        movie_id: int,
        movies_amount: int,
        n_users_rating: int):
    # Asegurarse de que el umbral mínimo de usuarios sea 4
    # if n_users_rating < 4:
    #     print("El valor de no_of_users_threshold debe ser al menos 4. Ajustando a 4.")
    #     no_of_users_threshold = 4

    # Título de la película seleccionada
    selected_movie_title = df.loc[df["movieId"] == movie_id, "title"].values[0]
    print("Selected movie: ", selected_movie_title)
    print("\nSimilar movies:\n")

    # Crear un DataFrame de valoraciones
    ratings_df = df[['userId', 'movieId', 'rating']].drop_duplicates()

    # Matriz usuario-película
    user_movie_matrix = pd.pivot_table(
        data=ratings_df,
        values='rating',
        index='userId',
        columns='movieId',
        fill_value=0
    )

    # Matriz de similitud (coseno)
    movie_similarity_matrix = pd.DataFrame(
        cosine_similarity(user_movie_matrix.T),
        columns=user_movie_matrix.columns,
        index=user_movie_matrix.columns
    )

    # Similitudes para la película seleccionada
    movie_similarities = pd.DataFrame(movie_similarity_matrix[movie_id])
    movie_similarities = (
        movie_similarities.loc[movie_similarities.index != movie_id, :]
        .rename(columns={movie_id: "movie_similarities"})
        .sort_values("movie_similarities", ascending=False)
    )

    # Filtrar por número de usuarios que calificaron ambas películas
    no_of_users_rated_both_movies = [
        sum((user_movie_matrix[movie_id] > 0) &
            (user_movie_matrix[isbn] > 0)) for isbn in movie_similarities.index
    ]
    movie_similarities["users_who_rated_both_movies"] = no_of_users_rated_both_movies
    movie_similarities = movie_similarities[
        movie_similarities["users_who_rated_both_movies"] >= no_of_users_threshold
        ]

    # Verifica si 'movieId' está en df
    if 'movieId' not in df.columns:
        raise KeyError("La columna 'movieId' no se encuentra en el DataFrame.")

    # Seleccionar las columnas correctas para la fusión
    movie_cols = ["movieId", "title", "genres"]
    similar_movies = (
        movie_similarities
        .head(movies_amount)
        .reset_index()
        .merge(df[movie_cols].drop_duplicates(subset='movieId'),
               on='movieId',
               how='left')
        [movie_cols + ["movie_similarities", "users_who_rated_both_movies"]]
    )

    return similar_movies

def obtener_id_pelicula(df, titulo):
    """
    Dada una película en formato string, devuelve el id_pelicula correspondiente.

    Parámetros:
    - df (pd.DataFrame): DataFrame con columnas 'pelicula' e 'id_pelicula'.
    - titulo_pelicula (str): Título de la película a buscar.

    Retorna:
    - int o None: El id de la película si se encuentra; de lo contrario, None.
    """
    resultado = df.loc[df['title'] == titulo, 'movieId']
    if not resultado.empty:
        return resultado.iloc[0]
    else:
        return -1
