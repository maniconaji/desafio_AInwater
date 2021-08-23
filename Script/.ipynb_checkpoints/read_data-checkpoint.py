import pandas as pd
import numpy as np

def To_datetime(df, col_date, col_time):
    df["datetime"]     = pd.to_datetime(df[col_date]+' '+df[col_time], format="%Y-%m-%d %H:%M:%S")
    df["year"]       = df["datetime"].dt.year
    df["month"]      = df["datetime"].dt.month
    df["day"]        = df["datetime"].dt.day
    return df

def rename_columns(df, col_initial, col_finish):
    return df.rename({col_initial: col_finish}, axis=1)

def read_csvdata(path_src, type_columns):
    df = pd.read_csv(path_src, dtype=type_columns, index_col=False)
    df = (df.
          pipe(To_datetime, "date", "time").
          pipe(rename_columns, "Unnamed: 0", "registro_id")
         )
    return df.set_index("registro_id")