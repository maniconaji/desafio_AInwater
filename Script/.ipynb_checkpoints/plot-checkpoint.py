import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd
import numpy as np
import math
from matplotlib import cm

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

def k_bins(s):
    """
    Función para determinar número de bins en un histograma
    
    s (series.dataframe): Serie de la que se desea enconrar en número de bins para realizar un histograma.
    """
    if s.count() >= 100:
        return np.round(1+ 3.322*np.log10(s.count())).astype(int)
    else:
        return np.round(np.sqrt(s.count())).astype(int)

########################################## bar_by_cycle_sum ###########################################################

def bar_by_cycle_sum(df, col_name, title, col_color, col_hover_data, **kwargs):
    # Agrupar datos por ciclo y obtener el total por ciclo
    grouped_df   = df.groupby(["cycle_id", "day"])
    grouped_sum  = grouped_df.sum().reset_index().drop(col_hover_data, axis=1)
    grouped_mean = df.groupby(["cycle_id", "day"]).mean().reset_index()[col_hover_data]
    
    grouped_df  = pd.concat([grouped_sum, grouped_mean], axis=1).astype({"day":str, "month":str, "year":str})

    # Figura para gráficar los Hz totales por ciclo
    fig = px.bar(
        data_frame = grouped_df, x = "cycle_id", y = col_name, color=col_color, hover_data = col_hover_data
    )
    fig.update_layout(
        # Axis
        yaxis = dict(
            title = "<b>"+col_name+"</b>", titlefont_size = 14, tickfont_size  = 12, 
            showline = True, linewidth = 1, linecolor = 'black', mirror = True,
            showgrid = True, gridwidth = 0.25, gridcolor = 'rgba(0, 0, 0, 0.5)',
            zeroline = True, zerolinewidth = 0.25, zerolinecolor = 'rgba(0, 0, 0, 0.5)'
        ),
        xaxis = dict(
            title = "<b>cycle_id</b>", titlefont_size = 14, tickfont_size  = 12, 
            tickvals = grouped_df["cycle_id"], ticktext = grouped_df["cycle_id"], 
            showline = True, linewidth = 1, linecolor = 'black', mirror = True,
            showgrid = True, gridwidth = 0.25, gridcolor = 'rgba(0, 0, 0, 0.5)',
            zeroline = True, zerolinewidth = 0.25, zerolinecolor = 'rgba(0, 0, 0, 0.5)'
        ),
        
        yaxis_range = [0, round_up(grouped_df[col_name].max()*1.25,-2)],
        xaxis_range = [grouped_df["cycle_id"].min()-1, grouped_df["cycle_id"].max()+1],
        # Tamaño figura
        height     = kwargs["height"],
        width      = kwargs["width"],
        # Titulo
        title_text = title[col_name].upper(),
        title_x    = 0.5,
        title_y    = 0.95,
        titlefont_size = 20,
        plot_bgcolor = "white"
    )
    
    return fig

#######################################################  gastoenergetico_por_dia  #####################################################

def gastoenergetico_por_dia(df, query, col_labels, col_values, subtitle, col_hover_data, **kwargs):
    
    grouped_df   = df.groupby(["cycle_id", "day"])
    grouped_sum  = grouped_df.sum().reset_index().drop(col_hover_data, axis=1)
    grouped_mean = df.groupby(["cycle_id", "day"]).mean().reset_index()[col_hover_data]

    df_query = pd.concat([grouped_sum, grouped_mean], axis=1).query(query)
    labels   = df_query[col_labels]
    values   = df_query[col_values]

    day, month, year =str(df_query.day.unique()[0]), str(int(df_query.month.unique()[0])), str(int(df_query.year.unique()[0]))
    title = "<b>"+ "Gasto Energético para el día: " +day+"/"+month+"/"+year +"</b>"
    
    specs=[[{'type':'xy'}, {'type':'domain'}]]
    fig = make_subplots(
        rows = 1, cols = 2, 
        specs = specs, subplot_titles=("<b>"+subtitle+"</b>", ""),
    )

    cmap = cm.get_cmap('tab10', 6)
    color_discrete_sequence = cmap(np.linspace(0, 1, 6))
    color_discrete_sequence1 = [ "rgba("+str(r)+","+str(g)+","+str(b)+","+str(a)+")" for r,g,b,a in color_discrete_sequence]
    color_discrete_sequence2 = [ "rgb("+str(r*255)+","+str(g*255)+","+str(b*255)+")" for r,g,b,a in color_discrete_sequence]
    
    # Bar plot con gasto total energético por ciclo para el día seleccionado
    fig.add_trace(
        go.Bar(x = labels, y = values, showlegend=False, marker_color = color_discrete_sequence1, name = col_values), 
        row = 1, col = 1
    )
    
    # Pie chart 
    fig.add_trace(
        go.Pie(
            labels = labels, values = values, sort=False, 
            marker_colors = color_discrete_sequence2, 
            marker_line = dict(color = 'rgba(0, 0, 0, 1)', width=1),
            hole=.3,
            textinfo='label+percent',
            name = col_labels,
            textposition = 'auto'
        ),
        row = 1, col = 2
    )

    fig.update_layout(
        yaxis = dict(
            title = "<b>"+col_values+"</b>", titlefont_size = 14, tickfont_size  = 12, 
            showline = True, linewidth = 1, linecolor = 'black', mirror = True,
            showgrid = True, gridwidth = 0.25, gridcolor = 'rgba(0, 0, 0, 0.5)',
            zeroline = True, zerolinewidth = 0.25, zerolinecolor = 'rgba(0, 0, 0, 0.5)'
        ),
        yaxis_range = [0, round_up(values.max()*1.25, -3)],
        xaxis = dict(
            title = "<b>"+col_labels+"</b>", titlefont_size = 14, tickfont_size  = 12, 
            tickvals = df_query["cycle_id"], ticktext = df_query["cycle_id"], 
            showline = True, linewidth = 1, linecolor = 'black', mirror = True,
            showgrid = True, gridwidth = 0.25, gridcolor = 'rgba(0, 0, 0, 0.5)',
            zeroline = True, zerolinewidth = 0.25, zerolinecolor = 'rgba(0, 0, 0, 0.5)'
        ),
        xaxis_range = [labels.min()-0.5, labels.max()+0.5],

        title_text  = title.upper(),
        title_x     = 0.5,
        title_y     = 0.95,
        titlefont_size = 20,
        height      = kwargs["height"],
        width       = kwargs["width"],
        
        # Margenes y color de fondo
        plot_bgcolor = "white",
        
        legend_title = dict(
            text = col_labels
        )
    )
    return fig

########################################## bar_by_cycle_mean ###########################################################

def bar_by_cycle_mean(df, col_name, title, query_text = None, **kwargs):
    # Agrupar datos por ciclo y obtener el total por ciclo
    if query_text is None:
        title_text = title[col_name].upper()+"<b> por ciclo</b>".upper()
        pass
    else:
        df = df.query(query_text)
        title_text = title[col_name].upper()+"<b> por ciclo para ".upper()+query_text.upper()+"</b>".upper()
        
    grouped_df = df.groupby("cycle_id").mean().reset_index()
    counts, bins = np.histogram(df[col_name], bins=k_bins(df[col_name]), range=(round_down(df[col_name].min()), round_up(df[col_name].max())))
    counts = counts*100/np.sum(counts)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(title[col_name], "<b>Histograma</b>"),
        column_widths=[0.7, 0.3],
#         shared_yaxes= True,
        horizontal_spacing = 0.075
    )
    # Figura para gráficar nivel medio de cada variable
    fig.add_trace(
        go.Scatter(
            x    = grouped_df["cycle_id"], y = grouped_df[col_name],
            name = title[col_name],
            mode='lines+markers',
            marker=dict(
                line=dict(color='rgba(0, 0, 0, 1.0)', width=1)
            )), row=1, col=1
    )
    # Figura para gráficar el histograma de cada variable
    fig.add_trace(
        go.Histogram(
            x        = df[col_name],
            histnorm = 'percent',
            name   = "<b>Histograma</b>",
            xbins  = dict(
                start = bins[0],
                end   = bins[-1],
                size  = bins[1] - bins[0]
            ),
            marker = dict(
                line = dict(color='rgba(0, 0, 0, 1.0)', width=1),
            )
        ), row=1, col=2
    )
    fig.update_layout(
        # Axis gráfico de barras
        yaxis = dict(
            title = "<b>"+col_name+"</b>", titlefont_size = 14, tickfont_size  = 12, 
            showline = True, linewidth = 1, linecolor = 'black', mirror = True,
            showgrid = True, gridwidth = 0.25, gridcolor = 'rgba(0, 0, 0, 0.5)',
            zeroline = True, zerolinewidth = 0.25, zerolinecolor = 'rgba(0, 0, 0, 0.5)'
        ),
        yaxis_range = [round_down(grouped_df[col_name].min()*0.95), round_up(grouped_df[col_name].max()*1.05)],
        xaxis = dict(
            title = "<b>cycle_id</b>", titlefont_size = 14, tickfont_size  = 12, 
            tickvals = grouped_df["cycle_id"], ticktext = grouped_df["cycle_id"], 
            showline = True, linewidth = 1, linecolor = 'black', mirror = True,
            showgrid = True, gridwidth = 0.25, gridcolor = 'rgba(0, 0, 0, 0.5)',
            zeroline = True, zerolinewidth = 0.25, zerolinecolor = 'rgba(0, 0, 0, 0.5)'
        ),
        xaxis_range = [grouped_df["cycle_id"].min()-1, grouped_df["cycle_id"].max()+1],
        
        # Axis Histograma
        yaxis2 = dict(
            title = "<b>Total</b>", titlefont_size = 14, tickfont_size  = 12, 
            showline = True, linewidth = 1, linecolor = 'black', mirror = True,
            showgrid = True, gridwidth = 0.25, gridcolor = 'rgba(0, 0, 0, 0.5)',
            zeroline = True, zerolinewidth = 0.25, zerolinecolor = 'rgba(0, 0, 0, 0.5)'
                     ),
        yaxis2_range = [0, round_up(np.max(counts)*1.05,-2)],
        xaxis2 = dict(
            title = "<b>cycle_id</b>", titlefont_size = 14, tickfont_size  = 12, 
            tickvals = grouped_df["cycle_id"], ticktext = grouped_df["cycle_id"], 
            showline = True, linewidth = 1, linecolor = 'black', mirror = True,
            showgrid = True, gridwidth = 0.25, gridcolor = 'rgba(0, 0, 0, 0.5)',
            zeroline = True, zerolinewidth = 0.25, zerolinecolor = 'rgba(0, 0, 0, 0.5)' 
                     ),
        xaxis2_range = [bins[0], bins[-1]],
        
        # Tamaño figura
        height     = kwargs["height"],
        width      = kwargs["width"],
        
        # Titulo
        title_text = title_text,
        title_x    = 0.5,
        title_y    = 0.95,
        titlefont_size = 20,
        
        # Legend
        showlegend = False,
        
        # Margenes y color de fondo
        plot_bgcolor = "white",
    )
    
    return fig