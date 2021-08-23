from typing import Container
import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import plotly.express as px

import sys
sys.path.insert(0, 'Script')
from read_data import read_csvdata

st.set_page_config(page_title = 'Desafío AInwater', layout = "wide", initial_sidebar_state = "auto")

########################################## sidebar #################################################

sidebar = st.sidebar

sidebar.title('Desafío AInwater')

sidebar.markdown("""
El siguiente desafío tiene por objetivo central caracterizar el funcionamiento de la planta durante una semana dividido en cuatro etapas ("Motor soplador", "Oxígeno", "Agua", "Clustering"). 

Para esto, se cuenta con variables que describen n° de registro de la medición, fecha, hora, el consumo energético del motor del soplador, nivel de oxígeno, nivel de agua y una identificación del ciclo a que corresponde. 
""")

variable = sidebar.radio(
    "Variable a analizar:",
    ("Motor soplador", "Oxígeno", "Agua", "Clustering"),
    index = 0
)

sidebar.markdown("""
Autor: Manuel Huerta
""")

########################################## panel #################################################
# previo
path_src = "Data/base_test_planta_tupiniquim.csv"
type_columns = {
    "date"      : str,
    "time"      : str,
    "do_level"  : float,
    "h2o_level" : float,
    "blower_hz" : float,
    "cycle_id"  : int
}
df = read_csvdata(path_src, type_columns)

from plot import bar_by_cycle_sum, gastoenergetico_por_dia, bar_by_cycle_mean

if variable == "Motor soplador":
    col_name = 'blower_hz'
    
    container_0 = st.beta_container()
    container_0.header(variable)
    container_0.markdown("""
    La variable "blower_hz" contiene hz de giro del motor a lo largo de esta semana, caracterizándose por presentar una mayor variabilidad con relación a la media a la hora de comparar el promedio y la desviación estándar de esta variable. Esto se debe principalmente a que el accionamiento del motor no es continuo (observable al manejar la barra de abajo de la serie de tiempo).
    """)
    container_0.subheader("Resumen estadistico")
    container_0.write(df.filter([col_name]).describe().T)
    
    # Serie de Tiempo
    container_1 = st.beta_container()
    fig = px.line(df, x="datetime", y=col_name, color="cycle_id", title='<b>Serie de Tiempo de los Hz del soplador</b>')
    fig.update_yaxes(range = [0, 60])
    fig.update_layout(height=500)
    fig.update_xaxes(rangeslider_visible=True)
    container_1.plotly_chart(fig, use_container_width=True)
    
    # Hz totales por ciclo
    title = {"blower_hz"  : "<b>Hz totales por ciclo</b>",}
    container_2 = st.beta_container()
    container_2.markdown("""
    Por otro lado, cuando se estudia los Hz totales por cada ciclo, se deduce:
    * Hay un mayor consumo energético en los ciclos correspondientes a las tardes-noches (últimos tres ciclos de cada día).
    * Este fenómeno es producto del aumento en el flujo de RIL a tratar en la planta de tratamiento.
    
    Estas aseveraciones son comprobables en el siguiente gráfico de barras, que corresponde a los Hz totales por cada ciclo, considerando distintos colores para cada día.
    """)
    fig = bar_by_cycle_sum(
    df, col_name, title = title, col_color = "day", col_hover_data = ["do_level", "h2o_level", "month", "year"], height = 400, width=1100
    )
    container_2.plotly_chart(fig, use_container_width=True)
    
elif variable == "Oxígeno":
    col_name = 'do_level'
    
    container_0 = st.beta_container()
    container_0.header(variable)
    container_0.markdown("""
    La variable "do_level" contiene el nivel de oxígeno a lo largo de esta semana, caracterizándose por presentar una mayor variabilidad con relación a la media a la hora de comparar el promedio y la desviación estándar de esta variable. Esto se debe principalmente a que la inyección de oxígeno en la etapa aerobia de la planta de tratamiento no es continuo, sino bajo un sistema batch (observable al manejar la barra de abajo de la serie de tiempo).
    """)
    container_0.subheader("Resumen estadistico")
    container_0.write(df.filter([col_name]).describe().T)
    
    # Serie de Tiempo   
    container_1 = st.beta_container()
    fig = px.line(df, x="datetime", y=col_name, color="cycle_id", title='<b>Serie de Tiempo del nivel de oxígeno</b>')
    fig.update_layout(height=500)
    fig.update_xaxes(rangeslider_visible=True)
    container_1.plotly_chart(fig, use_container_width=True)
    
    #
    container_2 = st.beta_container()
    title = {
    "blower_hz"  : "<b>Nivel medio de Hz</b>",
    "do_level"   : "<b>Nivel medio de O<sub>2</sub></b>",
    "h2o_level"  : "<b>Nivel medio de H<sub>2</sub>O</b>"
    }
    container_2.markdown("""
    Ahora, en relación a la comparación del nivel medio de oxígeno considerando todos los datos y aquellos en que solo estaba en funcionamiento el motor del soplador ("blower_hz > 0"), se deduce:
    
    * Antes de que se produzca un mayor consumo energético en cada uno de los ciclos, es decir, los ciclos 3, 8, 13, 18, 23, 28 y 33, los niveles medios de oxígeno se encuentran por sobre los otros ciclos de funcionamiento de cada día. 
    * El efecto anterior ocurre debido al aumento en el flujo a tratar, y por ende, los niveles de oxígeno en el proceso aerobio disminuyen por una crecida en el volumen a tratar.
    * Referente a los histogramas, ambos presentan una distribución exponencial. En el primer histograma (el que considera todos los valores de la variable "blower_hz") la clase "0 - 0.462" es presenta por sobre 40% de los datos. Por otro lado, cuando se filtran los resultados de la variable "blower_hz", la clase "0 - 0.544" presenta cerca de un 30% de los datos.
    
    Estas aseveraciones son comprobables en los siguientes gráficos, que corresponde al nivel medio de oxígeno y la distribución del oxígeno para todos los datos y para el caso "blower_hz > 0".
    """)
    
    fig1 = bar_by_cycle_mean(df, col_name, title = title, height = 400, width=1200)
    container_2.plotly_chart(fig1, use_container_width=True)
    fig2 = bar_by_cycle_mean(df, col_name, title = title, query_text = "blower_hz > 0", height = 400, width=1200)
    container_2.plotly_chart(fig2, use_container_width=True)
    
elif variable == "Agua":
    col_name = 'h2o_level'
    
    container_0 = st.beta_container()
    container_0.header(variable)
    container_0.markdown("""
    La variable "h2o_level" contiene el nivel de agua a lo largo de esta semana, caracterizándose por presentar una menor variabilidad con relación a la media a la hora de comparar el promedio y la desviación estándar de esta variable. Esto se debe principalmente a que en la etapa aerobia de la planta de tratamiento se mantiene un nivel mínimo de agua (observable en la serie de tiempo).
    """)
    container_0.subheader("Resumen estadistico")
    container_0.write(df.filter([col_name]).describe().T)
    
    # Serie de Tiempo   
    container_1 = st.beta_container()
    fig = px.line(df, x="datetime", y=col_name, color="cycle_id", title='<b>Serie de Tiempo del nivel de oxígeno</b>')
    fig.update_layout(height=500)
    fig.update_xaxes(rangeslider_visible=True)
    container_1.plotly_chart(fig, use_container_width=True)
    
    #
    container_2 = st.beta_container()
    title = {
    "blower_hz"  : "<b>Nivel medio de Hz</b>",
    "do_level"   : "<b>Nivel medio de O<sub>2</sub></b>",
    "h2o_level"  : "<b>Nivel medio de H<sub>2</sub>O</b>"
    }
    container_2.markdown("""
    Ahora, en relación a la comparación del nivel medio de agua considerando todos los datos y aquellos en que solo estaba en funcionamiento el motor del soplador ("blower_hz > 0"), se deduce:
    
    * Cuando se produce un mayor consumo energético en cada uno de los ciclos, es decir, los ciclos 3, 8, 13, 18, 23, 28 y 33, los niveles medios de agua se encuentran por sobre los otros ciclos de funcionamiento de ese día.
    * Respecto a los histogramas, considerando todos los valores de la variable "blower_hz" se presenta una distribución bimodal. No obstante, cuando se filtran los valores de la variable "blower_hz" esta distribución pasa a ser una distribución normal con un sesgo hacia la derecha. 
    
    Estas aseveraciones son comprobables en los siguientes gráficos, que corresponde al nivel medio de agua y la distribución del nivel de agua para todos los datos y para el caso "blower_hz > 0".
    """)
    
    fig1 = bar_by_cycle_mean(df, col_name, title = title, height = 400, width=1200)
    container_2.plotly_chart(fig1, use_container_width=True)
    fig2 = bar_by_cycle_mean(df, col_name, title = title, query_text = "blower_hz > 0", height = 400, width=1200)
    container_2.plotly_chart(fig2, use_container_width=True)


elif variable == "Clustering":
    # Todos los datos
    container_0 = st.beta_container()
    container_0.header("Clustering para todos los datos.")
    container_0.markdown("""
    1. Se probaron 3 modelos: K-means, DBSCAN y Hierarchical clustering. 
    2. Para el algoritmo de K-means se encontraron dos números de clúster, 8 a través del método de elbow y 2 a través del coeficiente de silueta.
    3. Para el modelo AgglomerativeClustering (Hierarchical clustering) se encontraron 2 clúster.
    4. Para el modelo DBSCAN no se encontraron parámetros óptimos.
    5. Comparando los tres modeles en base al coeficiente de silueta, escala de Calinski y Harabasz y la escala de Davies-Bouldin, el mejor modelo es del tipo "AgglomerativeClustering" con n_cluster = 2, con:
        * silhouette_score: 0.39484
        * calinski_harabasz_score: 1594.52080
        * davies_bouldin_score: 1.00619
    """)
    
    df_sin_query = pd.read_csv("Output/csv/datos_sin_query.csv").astype({"kmeans_label1": object, "kmeans_label2": object, "sch_label": object,})
    
    fig = px.scatter(df_sin_query.sort_values("sch_label", axis=0), x="pca 1", y="pca 2", color="sch_label", hover_data=["do_level", "h2o_level", "blower_hz", "cycle_id"],
                    title = "<b>Clusters para modelo AgglomerativeClustering con n_cluster = 2 </b>")
    container_0.plotly_chart(fig, use_container_width=True)
    
    # blower > 0
    container_1 = st.beta_container()
    container_1.header("Clustering para blower_hz > 0.")
    container_1.markdown("""
    1. Al igual que el análisis anterior, se probaron 3 modelos: K-means, DBSCAN y Hierarchical clustering. 
    2. Para el algoritmo de K-means se encontraron dos números de clúster, 7 a través del método de elbow y 8 a través del coeficiente de silueta.
    3. Para el modelo AgglomerativeClustering (Hierarchical clustering) se encontraron 2 clúster.
    4. Para el modelo DBSCAN no se encontraron parámetros óptimos.
    5. Comparando los tres modeles en base al coeficiente de silueta, escala de Calinski y Harabasz y la escala de Davies-Bouldin, el mejor modelo es del tipo k-means con n_cluster = 8, con:
        * silhouette_score: 0.37165
        * calinski_harabasz_score: 590.21804
        * davies_bouldin_score: 0.89632
    """)
    df_con_query = pd.read_csv("Output/csv/datos_con_query.csv").astype({"kmeans_label3": object, "kmeans_label4": object, "sch_label": object,})
    
    fig = px.scatter(df_con_query.sort_values("kmeans_label4", axis=0), x="pca 1", y="pca 2", color="kmeans_label4", hover_data=["do_level", "h2o_level", "blower_hz", "cycle_id"],
                    title = "<b>Clusters para un modelo k-means con n_cluster = 8 </b>")
    container_1.plotly_chart(fig, use_container_width=True)

    # blower > 0
    container_2 = st.beta_container()
    container_2.header("Conclusiones")
    container_2.markdown("""
    Comparando ambos resultados se deduce:
    
    1. Cuando se consideran todos los datos, los momentos en que el motor no se encuentra funcionando actúan como sesgo en el modelo, obteniendo tan solo 2 clúster.
    2. Si bien, el coeficiente de silueta es menor cuando se filtran los datos, la variabilidad observada en el coeficiente de calinski-harabasz y el agrupamiento en los clústeres a través del coeficiente de davies-bouldin muestran que el modelo k-means con 8 clústeres representa mejor el funcionamiento de la planta durante la semana que un modelo "AgglomerativeClustering" con n_cluster = 2.
    """)