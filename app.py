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

st.set_page_config(page_title = 'Desafió AInwater', layout = "wide", initial_sidebar_state = "auto")

########################################## sidebar #################################################

sidebar = st.sidebar

sidebar.title('Desafió AInwater')

sidebar.markdown("""
El siguiente desafío tiene por objetivo central caracterizar el funcionamiento de la planta durante una semana dividido en cuatro etapas. Para esto, cuenta con variables que describen n° de registro de la medición, fecha, hora, el consumo energético del motor del soplador, nivel de oxígeno, nivel de agua y una identificación del ciclo a que corresponde. 
""")

variable = sidebar.radio(
    "Variable a analizar:",
    ("Motor soplador", "Oxígeno", "Agua", "Clustering"),
    index = 0
)


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

 # ["do_level", "h2o_level", "blower_hz", "cycle_id"]
if variable == "Motor soplador":
    col_name = 'blower_hz'
    
    # Serie de Tiempo
    container_1 = st.beta_container()
    fig = px.line(df, x="datetime", y=col_name, color="cycle_id", title='Serie de Tiempo de los Hz del soplador')
    fig.update_yaxes(range = [0, 60])
    fig.update_layout(height=500)
    fig.update_xaxes(rangeslider_visible=True)
    container_1.plotly_chart(fig, use_container_width=True)
    
    # Hz totales por ciclo
    title = {"blower_hz"  : "<b>Hz totales por ciclo</b>",}
    container_2 = st.beta_container()
    fig = bar_by_cycle_sum(
    df, "blower_hz", title = title, col_color = "day", col_hover_data = ["do_level", "h2o_level", "month", "year"], height = 450, width=1100
    )
    container_2.plotly_chart(fig, use_container_width=True)
    
    
#     fig1, grouped_df, col_name = bar_by_cycle(df, variable, height = 500, width=1000)

#     if variable in ["Oxígeno", "Agua"]:
#         container_2 = st.beta_container()

#         fig2, grouped_df, col_name = bar_by_cycle_with_query(df, variable, query_text = "blower_hz > 0", height = 500, width=1000)
#         container_2.plotly_chart(fig2, use_container_width=True)
    


