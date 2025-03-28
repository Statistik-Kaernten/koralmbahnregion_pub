### ÜBERBLICK SEITE des Koralmbahn-Dashboards
from misc.gkzList import *
from data import *

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

## SIDEBAR
with st.sidebar:

    st.image("gfx/stat_ktn_logo.png", use_container_width=False, width=180)
    st.text('')
    st.image("gfx/stat_stmk_logo.png", use_container_width=False, width=180)
    st.text('')
    with st.expander(f''':orange[**INFO**]''', expanded=False):
        st.write(f'''
                 Dashboard Koralmbahnregionsindex, BETA-Version 1.0 vom 28.03.2025, erstellt von Martin Writz, BSc.,
                 Landesstelel für Statistik, Amt der Kärntner Landesregierung in Zusammenarbeit mit der Landesstelle für Statistik, Land Steiermark

                please report bugs to martin.writz@ktn.gv.at or abt1.statistik@ktn.gv.at, feel free to contribute or to commit a pull request directly  
                 ''')

## CONTENT    
col1, col2, col3, col4 = st.columns([3, 0.5, 0.5, 1])

# MAP
with col1:
    with open("map/koralmbahnregion_map.html", "r", encoding="utf-8") as html_file:
                    html_content = html_file.read()
    st.components.v1.html(html_content, width=1572//2, height=966//2, scrolling=False)
 
# ABOUT
with col4:
    with st.expander(f''':orange[**Koralmbahnregion**]''', expanded=True):
        st.write(f'''
                 Die Koralmbahnregion, Definition Joanneum Research.  
                 ''')
