# PBLGrupo2

## Sistema de Recomendación de Películas con Procesamiento de Datos e Integración de Ontologías

Este proyecto es un sistema de recomendación de películas integral que aprovecha el análisis de datos, el razonamiento ontológico y la lógica difusa. La aplicación consta de varios scripts de Python y notebooks de Jupyter que trabajan juntos para proporcionar a los usuarios recomendaciones de películas.

## Tabla de Contenidos


- [Módulos](#módulos)
  - [Análisis_Exploratorio_Datos.ipynb](#análisis_exploratorio_datosipynb)
  - [data_eng.ipynb](#data_engipynb)
  - [Poblar_ow.ipynb](#poblar_owipynb)
  - [Scripts Principales](#scripts-principales)
    - [main.py](#mainpy)
    - [stream.py](#streampy)
    - [ConsultaFuzz.py](#consultafuzzpy)
    - [ConsultaProtege.py](#consultaprotegepy)
    - [cosineSimilarity.py](#cosinesimilaritypy)
    - [Top10Movies.py](#top10moviespy)
  - [Archivo de Ontología](#archivo-de-ontología)
    - [movies.owl](#moviesowl)


## Módulos

### Análisis_Exploratorio_Datos.ipynb

Este notebook proporciona un análisis exploratorio de datos (EDA) sobre el conjunto de datos de películas, utilizando visualizaciones para descubrir tendencias e insights.

### data_eng.ipynb

Se centra en tareas de ingeniería de datos, como la limpieza y preparación del conjunto de datos para análisis y modelado.

### Poblar_ow.ipynb

Se utiliza para poblar una ontología OWL con datos de películas, integrando información estructurada para consultas.

## Scripts Principales

### main.py
 Script principal de la aplicación que sirve como punto de entrada para el sistema de recomendación de películas.

### stream.py 

Archivo base para poder usar la interfaz de Streamlit

### ConsultaFuzz.py

Implementa un sistema de recomendación basado en lógica difusa para sugerir géneros de películas según las valoraciones de los usuarios.

### ConsultaProtege.py
Interactúa con una ontología OWL para consultar datos de películas y recuperar información relevante sobre películas y valoraciones.

### cosineSimilarity.py

Calcula la similitud coseno para recomendar películas que son similares a una película dada según las valoraciones de los usuarios

### Top10Movies.py

 Identifica y recomienda las películas más populares según las valoraciones promedio y la cantidad de valoraciones.

## Archivo de Ontología

### movies.owl

Contiene la definición de la ontología para películas, proporcionando una representación estructurada de los datos relacionados con las películas.

