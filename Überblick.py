### ÜBERBLICK SEITE des Koralmbahn-Dashboards
#import streamlit as st
from misc.gkzList import *
from data import *
from st_bridge import bridge

# PAGE CONSTANTS
START_JAHR: int = 2002
END_JAHR: int = 2023

## PAGE CONFIG
st.set_page_config(page_title="Koralmbahnregion-Index Überblick", layout="wide")

## SESSION STATES
if 'gkz_list' not in st.session_state:
    st.session_state['gkz_list'] = []
if 'index_list' not in st.session_state:
    st.session_state['index_list'] = [0] * 12
if 'selected_years' not in st.session_state:
    st.session_state['selected_years'] = [END_JAHR - 10, END_JAHR]
if 'data' not in st.session_state:
    st.session_state['data'] = gkzList
      

## TITLE
st.title("Koralmbahnregion-Dashboard Überblick")
#st.write("# Koralmbahnregion Dashboard")
## SIDEBAR
with st.sidebar:
    #st.session_state.selected_years = st.slider("Jahre",
    #        min_value=START_JAHR,
    #        max_value=END_JAHR-1,
    #        value=(END_JAHR-10, END_JAHR),
    #        step=1)

    st.image("gfx/stat_ktn_logo.png", use_container_width=True)
    st.text('')
    st.image("gfx/stat_stmk_logo.png", use_container_width=True)
    st.text('')
    with st.expander(f''':orange[**INFO**]''', expanded=False):
        st.write(f'''
                 Dashboard Koralmbahnregionsindex, BETA-Version 0.1.0 vom 06.02.2025, erstellt von Martin Writz, BSc.,
                 Landesstelel für Statistik, Amt der Kärntner Landesregierung in Zusammenarbeit mit der Landesstelle für Statistik, Land Steiermark

                please report bugs to martin.writz@ktn.gv.at or abt1.statistik@ktn.gv.at, feel free to contribute or to commit a pull request directly  
                 ''')

## Data Bridge
bridgeData = bridge("my-bridge", default='')
#st.session_state.data = {key: bridgeData[key] for key in ['gkz', 'flag']}

try:
    st.session_state.data = {key: bridgeData[key] for key in ['gkz', 'flag']}
    #st.session_state.gkz_list = [st.session_state.data['gkz'][index] for index, value in enumerate(st.session_state.data['flag']) if value == 1]
except:
    pass
st.session_state.gkz_list = [st.session_state.data['gkz'][index] for index, value in enumerate(st.session_state.data['flag']) if value == 1]

### GET DATA
## BEV DATA
#bev_df = get_data('Bev_Zeitreihe_Gemeinden.csv')
#bev_df = filter_data(bev_df, st.session_state.selected_years[0], st.session_state.selected_years[1])

## CALCULATE "INDEX"
#try:
#    stk_bev = bev_df[bev_df['GKZ'].astype(str).str.startswith('6')]
#    st.session_state.index_list[0] = round((100/stk_bev[stk_bev['JAHR'] == st.session_state.selected_years[0]]['ANZAHL'].sum()*stk_bev[stk_bev['JAHR'] == st.session_state.selected_years[1]]['ANZAHL'].sum())-100, 2)
#except:
#    st.session_state.index_list[0] = '-'
#try:
#    ktn_bev = bev_df[bev_df['GKZ'].astype(str).str.startswith('2')]
#    st.session_state.index_list[1] = round((100/ktn_bev[ktn_bev['JAHR'] == st.session_state.selected_years[0]]['ANZAHL'].sum()*ktn_bev[ktn_bev['JAHR'] == st.session_state.selected_years[1]]['ANZAHL'].sum())-100, 2)
#except:
#    st.session_state.index_list[1] = '-'
#try:
#    korlm_bev = bev_df[bev_df['GKZ'].astype(str).isin(st.session_state.gkz_list)]
#    st.session_state.index_list[2] = round((100/korlm_bev[korlm_bev['JAHR'] == st.session_state.selected_years[0]]['ANZAHL'].sum()*korlm_bev[korlm_bev['JAHR'] == st.session_state.selected_years[1]]['ANZAHL'].sum())-100, 2)
#except:
#    st.session_state.index_list[2] = '-'

## CONTENT    
col1, col2, col3, col4 = st.columns([3, 0.5, 0.5, 1])

# MAP
with col1:
    with open("map/koralmbahnregion_map.html", "r", encoding="utf-8") as html_file:
                    html_content = html_file.read()
    st.components.v1.html(html_content, width=1572//2, height=966//2, scrolling=False)

# OVERVIEW
#with col2: 
#    st.write(f''':orange[**Bevölkerung**]''')
#    st.write(f''':green[**Stmk**]:&emsp;&emsp;{st.session_state.index_list[0]}  
#            :blue[**Ktn**]:&emsp;&emsp;&ensp;&nbsp;{st.session_state.index_list[1]}  
#            :red[**Koralm**]:&emsp;{st.session_state.index_list[2]}''')
#    st.write(f''':orange[**Arbeitsmarkt**]''')
#    st.write(f''':green[**Stmk**]:&emsp;&emsp;{st.session_state.index_list[3]}  
#            :blue[**Ktn**]:&emsp;&emsp;&ensp;&nbsp;{st.session_state.index_list[4]}  
#            :red[**Koralm**]:&emsp;{st.session_state.index_list[5]}''')
#with col3:
#    st.write(f''':orange[**Vekehr**]''')
#    st.write(f''':green[**Stmk**]:&emsp;&emsp;{st.session_state.index_list[6]}  
#            :blue[**Ktn**]:&emsp;&emsp;&ensp;&nbsp;{st.session_state.index_list[7]}  
#            :red[**Koralm**]:&emsp;{st.session_state.index_list[8]}''')
#    st.write(f''':orange[**Bildung**]''')
#    st.write(f''':green[**Stmk**]:&emsp;&emsp;{st.session_state.index_list[9]}  
#            :blue[**Ktn**]:&emsp;&emsp;&ensp;&nbsp;{st.session_state.index_list[10]}  
#            :red[**Koralm**]:&emsp;{st.session_state.index_list[11]}''')
# ABOUT
with col4:
    with st.expander(f''':orange[**Koralmbahnregion**]''', expanded=True):
        st.write(f'''
                 Die Koralmbahnregion, Definition Joanneum Research.  
                 ''')

#st.session_state