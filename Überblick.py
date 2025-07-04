### ÜBERBLICK SEITE des Koralmbahn-Dashboards
from misc.gkzList import *
from data import *
from map import createMap
from streamlit_bokeh import streamlit_bokeh

# PAGE CONSTANTS
START_JAHR: int = 2002
END_JAHR: int = 2023

## PAGE CONFIG
st.set_page_config(page_title="Koralmbahnregion-Index Überblick", layout="wide", initial_sidebar_state='expanded')

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

## SIDEBAR
with st.sidebar:

    st.image("gfx/stat_ktn_logo.png", width=190)
    st.text('')
    st.image("gfx/stat_stmk_logo.png", width=150)
    st.text('')

    with st.expander(f''':orange[**Info**]''', expanded=False):
        st.write(f'''
                 Koralmbahnregion-Dashboard  
                 BETA-Version vom 29.04.2025,  
                 erstellt von Martin Writz, BSc.,  
                 Landesstelle für Statistik,   
                 Amt der Kärntner Landesregierung  
                   
                 in Zusammenarbeit mit der   
                 Landesstelle für Statistik,  
                 Land Steiermark 
                  
                Farbschema im Color Universal Design  
                  
                please report bugs to  
                martin.writz@ktn.gv.at  
                or  
                abt1.statistik@ktn.gv.at,  
                 feel free to contribute  
                 or  
                 commit a pull request directly  
                 ''')

## CONTENT    
col1, col2= st.columns([0.8, 0.2])

# MAP
with col1:
    streamlit_bokeh(createMap(), use_container_width=True)#, key="plot1"
    #with open("map.html", "r", encoding="utf-8") as html_file:
    #                html_content = html_file.read()
    #st.components.v1.html(html_content, width=1572//2, height=966//2, scrolling=True)
# OG: st.components.v1.html(html_content, width=1572//2, height=966//2, scrolling=False)
 
# ABOUT
with col2:
    with st.expander(f''':orange[**Koralmbahnregion**]''', expanded=True):
        st.write(f'''
                 Die Koralmbahnregion,  
                 Definition nach Joanneum Research.  
                 [Website](https://www.joanneum.at/policies/die-koralmbahn-und-ihre-regionaloekonomische-wirkung-ein-neuer-international-sichtbarer-ballungsraum-entsteht/)  
                   
                 Das Koralmbahnprojekt verfolgt das Ziel,  
                 dass Kärnten und die Steiermark zusammenwachsen.  
                 Dieses Dashboard bietet eine Datensammlung gegliedert  
                 in den vier Bereichen Bevölkerung, Wirtschaft, Verkehr  
                 und Bildung für die definierte Koralmbahnregion um die  
                 Entwicklungen darstellen zu können.
                 ''')

# pre-load data
data_lst = ['bevoelkerung', 'wanderungen', "wohnungen", "erwerbstaetige", "arbeitsstaetten", "tourismus", "schueler", "hoest_ausbildung", "verkehrszaehlung"]
for elem in data_lst:
    df = get_data(f'{elem}.csv')