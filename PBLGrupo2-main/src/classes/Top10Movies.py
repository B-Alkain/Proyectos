import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('.\data\mini.csv')


def recommend_most_popular_movies(df: pd.DataFrame, n_movies: int):
    print("Most popular movies:\n")

    # Calcular métricas de popularidad
    popularity_metrics = df.groupby("movieId").agg({
        "rating": "mean",
        "movieId": "count"
    })
    popularity_metrics.columns = ['avg_rating', 'number_of_ratings']

    # Métrica combinada
    popularity_metrics["combined_metric"] = (
            (3 * popularity_metrics["avg_rating"]) * (1 * popularity_metrics["number_of_ratings"])
    )
    popularity_metrics=popularity_metrics.sort_values(by=['combined_metric']).tail(n_movies)
    list_id=popularity_metrics.index.to_list()
    top_n_movies = df[df['movieId'].isin(list_id)].drop_duplicates(subset='movieId')
    top_n_movies.insert(0, column="ranking", value=range(1, n_movies + 1, 1))
    return top_n_movies

