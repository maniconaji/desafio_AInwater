import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

import sys
sys.path.insert(0, 'Script')
from read_data import read_csvdata
from plot import bar_by_cycle

st.set_page_config(page_title = 'Desafió AInwater', layout = "wide", initial_sidebar_state = "auto")

########################################## sidebar #################################################

sidebar = st.sidebar

sidebar.title('Desafió AInwater')

variable = sidebar.radio(
    "Variable",
    ("Visión General","Motor", "Oxígeno", "Agua", "Cluster"),
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

# muestra en el panel

# ["do_level", "h2o_level", "blower_hz", "cycle_id"]
if variable in ["Motor", "Oxígeno", "Agua"]:
    fig, grouped_df, col_name = bar_by_cycle(df, variable)
    
    container1 = st.beta_container()
    
    container1.plotly_chart(fig, use_container_width=True)
    container1.write(grouped_df[["cycle_id", col_name]].set_index("cycle_id").T)
    
    #st.plotly_chart(fig, use_container_width=True)
    #st.write(grouped_df[["cycle_id", col_name]].set_index("cycle_id"))


