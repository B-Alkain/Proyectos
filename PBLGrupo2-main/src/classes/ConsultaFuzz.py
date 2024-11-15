import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from io import BytesIO

list_genres=['(no genres listed)', 'Action','Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary','Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery',
       'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

class ConsultaFuzz:
    def __init__(self):
        # Init lo uso como contructor y para generar el sistema de reglas y control
        self.genres = list_genres
        
        # Crear variables de entrada (una por cada género)
        self.inputs = {}
        for genre in self.genres:
            self.inputs[genre] = ctrl.Antecedent(np.arange(0, 11, 1), genre)
            
        # Crear variable de salida
        self.output = ctrl.Consequent(np.arange(0, len(self.genres), 1), 'recommended_genre')
        
        # Definir funciones de membresía para entradas
        for genre in self.genres:
            self.inputs[genre]['bajo'] = fuzz.gaussmf(self.inputs[genre].universe, 0, 2)
            self.inputs[genre]['medio'] = fuzz.gaussmf(self.inputs[genre].universe, 5, 2)
            self.inputs[genre]['alto'] = fuzz.gaussmf(self.inputs[genre].universe, 10, 2)
        
        # Crear reglas
        self.rules = []
        for i, genre in enumerate(self.genres):
            self.output[genre] = fuzz.gaussmf(self.output.universe, i, 1)
        
        # Crear reglas
        self.rules = []
        for i, genre in enumerate(self.genres):
            rule = ctrl.Rule(
                self.inputs[genre]['alto'] &
                self.get_other_genres_rules(genre),
                self.output[genre]
            )
            self.rules.append(rule)
        
        # Crear sistema de control
        self.system = ctrl.ControlSystem(self.rules)
        self.sim = ctrl.ControlSystemSimulation(self.system)
    
    def get_other_genres_rules(self, main_genre):
        """Función auxiliar: Genera reglas para los otros géneros"""
        others_rule = None
        for genre in self.genres:
            if genre != main_genre:
                if others_rule is None:
                    others_rule = self.inputs[genre]['bajo']
                else:
                    others_rule = others_rule & self.inputs[genre]['bajo']
        return others_rule
    
    def recommend(self, ratings):
        
        # Establecer entradas
        for genre, rating in ratings.items():
            self.sim.input[genre] = rating
        
        try:
            # Computar resultado
            self.sim.compute()
            
            # Obtener el género con el valor más alto en la salida
            max_value = -1
            recommended_genre = None
            
            for genre in self.genres:
                value = self.sim.output['recommended_genre']
                genre_index = self.genres.index(genre)
                membership = fuzz.gaussmf(np.array([value]), genre_index, 1)[0]
                
                if membership > max_value:
                    max_value = membership
                    recommended_genre = genre
             #Crear la gráfica en memoria
            fig, ax = plt.subplots(figsize=(25,15))
            self.output.view(sim=self.sim, ax=ax)
            ax.set_title("Simulación de Recomendación de Género")
            ax.set_xlabel("Nivel de Pertinencia")
            ax.set_ylabel("Géneros")
            plt.tight_layout()
            plt.savefig('./img/temp.png')

            # Guardar la gráfica en un objeto BytesIO
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)  # Regresar el puntero al inicio del objeto BytesIO
            plt.close(fig)  # Cerrar la figura para liberar memoria
            
            return recommended_genre,fig
            
        except Exception:
            return "No se pudo generar una recomendación"
