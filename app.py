from typing import Container
import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

import sys
sys.path.insert(0, 'Script')
from read_data import read_csvdata

st.set_page_config(page_title = 'Desafió AInwater', layout = "wide", initial_sidebar_state = "auto")

########################################## sidebar #################################################

sidebar = st.sidebar

sidebar.title('Desafió AInwater')

variable = sidebar.radio(
    "Variable a analizar:",
    ("Motor", "Oxígeno", "Agua", "Clustering"),
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

# # ["do_level", "h2o_level", "blower_hz", "cycle_id"]
# if variable in ["Motor", "Oxígeno", "Agua"]:
#     container_1 = st.beta_container()
    
#     fig1, grouped_df, col_name = bar_by_cycle(df, variable, height = 500, width=1000)
#     container_1.plotly_chart(fig1, use_container_width=True)

#     if variable in ["Oxígeno", "Agua"]:
#         container_2 = st.beta_container()

#         fig2, grouped_df, col_name = bar_by_cycle_with_query(df, variable, query_text = "blower_hz > 0", height = 500, width=1000)
#         container_2.plotly_chart(fig2, use_container_width=True)
    


