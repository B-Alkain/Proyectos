import pandas as pd
import numpy as np
from owlready2 import *

df=pd.read_csv('.\data\mini.csv')

class ConsultaProtege:
    #El init lo definiremos como generar el objeto con la url del archivo del owl
    def __init__(self,ontology_url:str):
        self.ontology_url=ontology_url
    
    @property
    def ontology_url(self):
        return self.__ontology_url 
    
    @ontology_url.setter
    def ontology_url(self,url:str):
        self.__ontology_url=url
        
    def load_onto(self):
        onto=get_ontology(self.__ontology_url).load()
        with onto:
            sync_reasoner_pellet()
        return onto
    
    from owlready2 import default_world

def consultar_peliculas_por_director(director_name:str):
    # Definición de la consulta SPARQL
    query = f"""
    PREFIX : <http://pbl_02.org/movies.owl#>
    SELECT ?title ?year ?imdbid ?tmdbid
    WHERE {{
      ?movie a :Movie .
      ?movie :has_director "{director_name}" .
      ?movie :has_title ?title .
      ?movie :has_year ?year .
      ?movie :imdb_Id ?imdbid .
      ?movie :tmdb_Id ?tmdbid .
    }}
    """
    # Ejecutamos la consulta
    results = default_world.sparql(query)
    
    peliculas = [{"title": str(title), "year": str(year), "imdbid": str(imdbid), "tmdbid":str(tmdbid) } for title, year, imdbid, tmdbid in results]
    return peliculas

    

def obtener_resenias_recientes(nombre_pelicula:str):

    # Definición de la consulta SPARQL
    query = f"""
    PREFIX : <http://pbl_02.org/movies.owl#>
    SELECT ?user ?score ?date
    WHERE {{
      ?movie a :Movie .
      ?movie :has_title "{nombre_pelicula}" .
      ?rating a :Rating .
      ?rating :for_movie ?movie .
      ?rating :given_by ?user .
      ?rating :has_score ?score .
      ?rating :rating_date ?date .
    }}
    ORDER BY DESC(?date)
    LIMIT 10
    """
    # Ejecutar la consulta
    results = default_world.sparql(query)
    
    # Procesar resultados
    reseñas = [{"user": str(user), "rate": float(score), "date": str(date)} for user, score, date in results]
    return reseñas