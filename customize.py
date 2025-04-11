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

def handle_comma(input: float) -> str:
    input = str(input).replace('.', ',')
    return input


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
    cud_colors = ['#003B5C', '#FFB81C', '#55B0B9', '#F56D8D', '#9E2A2F', '#5B8C5A', '#CC79A7']
    return cud_colors


def create_linechart(df: pd.DataFrame, reg: int) -> pd.DataFrame:
    palette = get_palette()
    y_min = min(df['ANZAHL'].astype(float).min(), df['REGRESSION'].astype(float).min())
    y_max = max(df['ANZAHL'].astype(float).max(), df['REGRESSION'].astype(float).max())
    df['ANZAHL_FORMATTED'] = df['ANZAHL'].apply(lambda x: add_thousand_dot(str(int(round(x, 0)))))

    chart = alt.Chart(df).mark_line(color=palette[1], size=4).encode(
        x=alt.X('DATUM:T', title='Datum', axis=alt.Axis(format='%Y-%m', labelAngle=-90)),
        y=alt.Y('ANZAHL:Q', title='Anzahl', scale=alt.Scale(domain=(y_min, y_max))),
        tooltip=[alt.Tooltip('DATUM:T', title='Datum'), 
             #alt.Tooltip('TYPE:N', title='Arbeitsstätte'),
             alt.Tooltip('ANZAHL_FORMATTED:N', title='Anzahl')]

    )
    df['REG_FORMATTED'] = df['REGRESSION'].apply(lambda x: add_thousand_dot(str(int(round(x, 0)))))
    regression_line = alt.Chart(df).mark_line(color=palette[6], size=2).encode(
            x=alt.X('DATUM:T'),
            y=alt.Y('REGRESSION:Q', title="Trend"),
            tooltip=[alt.Tooltip('DATUM:T', title='Datum'),
                     alt.Tooltip('REG_FORMATTED:O', title='Trend')]
        )

    if(reg == False):
        combined_chart = (chart).configure_axis(
            titleFontWeight='bold'  
        ).configure_legend(
            titleFontWeight='bold'  
        )
    else:
        combined_chart = (chart + regression_line).configure_axis(
            titleFontWeight='bold'  
        ).configure_legend(
            titleFontWeight='bold'  
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