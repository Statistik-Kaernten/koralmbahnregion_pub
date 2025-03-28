import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
#from sklearn.linear_model import LinearRegression
#from bokeh.plotting import figure
#from bokeh.io import show
#from bokeh.models import ColumnDataSource
#from bokeh.layouts import column

def LinearRegression(df: pd.DataFrame) -> pd.DataFrame:

    df['DATUM'] = pd.to_datetime(df['DATUM'])
    df['DAYS_NUMERIC'] = (df['DATUM'] - df['DATUM'].min()).dt.days

    x_mean = np.mean(df['DAYS_NUMERIC'])
    df['ANZAHL'] = df['ANZAHL'].astype(float)
    y_mean = np.mean(df['ANZAHL'])

    numerator = np.sum((df['DAYS_NUMERIC'] - x_mean) * (df['ANZAHL'] - y_mean))
    denominator = np.sum((df['DAYS_NUMERIC'] - x_mean) ** 2)
    m = numerator / denominator
    b = y_mean - m * x_mean

    df['REGRESSION'] = m * df['DAYS_NUMERIC'] + b
    return df

def handle_comma(txt: str) -> str:
    return txt 

def add_thousand_dot(txt: str) -> str:
    if(txt[0] == '-'):
        if(len(txt) > 7):
            txt = txt[::-1]
            txt = txt[:3] + '.' + txt[3:6] + '.' + txt[6:]
            txt = txt[::-1]
        elif(len(txt) > 4):
            txt = txt[::-1]
            txt = txt[:3] + '.' + txt[3:]
            txt = txt[::-1]
    else:
        if(len(txt) > 6):
            txt = txt[::-1]
            txt = txt[:3] + '.' + txt[3:6] + '.' + txt[6:]
            txt = txt[::-1]
        elif(len(txt) > 3):
            txt = txt[::-1]
            txt = txt[:3] + '.' + txt[3:]
            txt = txt[::-1]
    return txt

def custom_css_sytles():
    st.markdown("""
        <style>
            .bokeh-plot-container {
                width: 100% !important;
                height: 100% !important;
            }
        </style>
    """, unsafe_allow_html=True)

def get_palette():
    return ['#ea9010', '#344e41', '#0b1d51', '#ee6c4d', '#bc6c25']
    #return ['#333333', '#777777', '#007722']


def create_linechart(df: pd.DataFrame, reg: int) -> pd.DataFrame:
    y_min = min(df['ANZAHL'].astype(float).min(), df['REGRESSION'].astype(float).min())
    y_max = max(df['ANZAHL'].astype(float).max(), df['REGRESSION'].astype(float).max())

    chart = alt.Chart(df).mark_line(color='#A9B84A').encode(
        x=alt.X('DATUM:T', title='Datum', axis=alt.Axis(format='%Y-%m', labelAngle=-90)),
        y=alt.Y('ANZAHL:Q', title='Anzahl', scale=alt.Scale(domain=(y_min, y_max)))
    )

    if(reg == False):
        return chart
    else:

        regression_line = alt.Chart(df).mark_line(color='#E3000F').encode(
            x=alt.X('DATUM:T'),
            y=alt.Y('REGRESSION:Q', title="Trend")
        )

        combined_chart = alt.layer(chart, regression_line).encode(
            x='DATUM',
            y=alt.Y('ANZAHL:Q', scale=alt.Scale(domain=(y_min, y_max))),
        )
        return combined_chart
    
def verkehr_anpassen(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(['JAHR', 'MONAT'])
    df['DAYS'] = (df['DATUM'] - df['DATUM'].min()).dt.days
    df = LinearRegression(df)
    df.drop(columns=['JAHR', 'MONAT', 'DAYS'], inplace=True, axis=1)
    return df

if __name__ == '__main__':
    pass