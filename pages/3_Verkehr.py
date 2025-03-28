import streamlit as st
from data import *
import altair as alt
from customize import *
from misc.gkzList import *


#from server import *
#from create_charts import create_linechart
#from custom import *

## PALETTE
palette = get_palette()

st.set_page_config(page_title="Verkehr", layout="wide")

st.write('# Verkehr')
st.sidebar.title("Einstellungen")


def select_messstelle(values: str) -> str:
    key = [key for key, value in zaehlstellen.items() if value == values]
    if key:
        return key[0]
    else:
        return None
    
selected_value = st.sidebar.selectbox('Zählstelle:', zaehlstellen.values())

#def min_startjahr() -> int:
#    df: pd.DataFrame = get_data(100, 1900, 2100, st.session_state.first_choice, st.session_state.second_choice, select_messstelle(selected_value))
#    return int(df['DATUM'].min().year)


# CONSTANTS
START_JAHR: int = 2012# min_startjahr()
END_JAHR: int = 2024

with st.sidebar:
    selected_jahre: int = st.slider("Startjahr",
            min_value=START_JAHR,
            max_value=END_JAHR-1,
            value=(START_JAHR, END_JAHR),
            step=1)
    
    select_start_jahr: int = selected_jahre[0]
    select_end_jahr: int = selected_jahre[1]

    select_trend_line = st.checkbox('Trendlinie', True)

    st.sidebar.write("<p style='text-align: center;'><em>Quelle: ASFINAG - Verkehrszählung.</em></p>", unsafe_allow_html=True)

    st.image("gfx/stat_ktn_logo.png", use_container_width=True)
    st.text('')
    st.image("gfx/stat_stmk_logo.png", use_container_width=True)
    st.text('')

#st.write(f"### Anzahl der gesamten Kfz im Bereich {selected_value} für beide Fahrtrichtungen")
#df_3 = get_messstelle_data(102, select_start_jahr, select_end_jahr, st.session_state.first_choice, st.session_state.second_choice, select_messstelle(selected_value))

#st.altair_chart(create_linechart(df_3, select_trend_line), use_container_width=True)


st.write(f"### Anzahl der Kfz kleiner 3,5t im Bereich {selected_value} beide Fahrtrichtungen")
df = get_data('verkehrszaehlung.csv')
df = filter_start_end_year(df, select_start_jahr, select_end_jahr)
df = df[df['ZAEHLSTELLE'] == (int)(select_messstelle(selected_value))]
df = df[df['FAHRZEUGKLASSE'] == 'Kfz <= 3,5t hzG']
df['DATUM'] = pd.to_datetime(df['JAHR'].astype(str) + '-' + df['MONAT'].astype(str) + '-01')

chart = create_linechart(verkehr_anpassen(df), select_trend_line)

st.altair_chart(chart, use_container_width=True)


st.write(f"### Anzahl der Kfz größer 3,5t im Bereich {selected_value} beide Fahrtrichtungen")
df = get_data('verkehrszaehlung.csv')
df = filter_start_end_year(df, select_start_jahr, select_end_jahr)
df = df[df['ZAEHLSTELLE'] == (int)(select_messstelle(selected_value))]
df = df[df['FAHRZEUGKLASSE'] == 'Kfz > 3,5t hzG']
df['DATUM'] = pd.to_datetime(df['JAHR'].astype(str) + '-' + df['MONAT'].astype(str) + '-01')

chart = create_linechart(verkehr_anpassen(df), select_trend_line)

st.altair_chart(chart, use_container_width=True)


st.write(f"### Anzahl aller Kfz im Bereich {selected_value} beide Fahrtrichtungen")
df = get_data('verkehrszaehlung.csv')
df = filter_start_end_year(df, select_start_jahr, select_end_jahr)
df = df[df['ZAEHLSTELLE'] == (int)(select_messstelle(selected_value))]
df = df[df['FAHRZEUGKLASSE'] == 'Kfz']
df['DATUM'] = pd.to_datetime(df['JAHR'].astype(str) + '-' + df['MONAT'].astype(str) + '-01')

chart = create_linechart(verkehr_anpassen(df), select_trend_line)

st.altair_chart(chart, use_container_width=True)

#st.write(f"### Anzahl der Kfz größer 3,5t im Bereich {selected_value} beide Fahrtrichtungen")
#df_2 = get_messstelle_data(101, select_start_jahr, select_end_jahr,  st.session_state.first_choice, st.session_state.second_choice, select_messstelle(selected_value))

#st.altair_chart(create_linechart(df_2, select_trend_line), use_container_width=True)

if __name__ == '__main__':
    select_messstelle('530')