from data import *
import altair as alt
from misc.customize import *

# PAGE CONSTANTS
START_JAHR: int = 2011
END_JAHR: int = 2022

## PAGE CONFIG
st.set_page_config(page_title="Bildung in der Koralmbahnregion", layout="wide")

## TITLE
st.title("Bildung in der Koralmbahnregion")

## PALETTE
palette = get_palette()

## SIDEBAR
with st.sidebar:
    selected_jahre: int = st.slider("Startjahr",
            min_value=START_JAHR,
            max_value=END_JAHR-1,
            value=(2011, END_JAHR),
            step=1)
    
    select_start_jahr: int = selected_jahre[0]
    select_end_jahr: int = selected_jahre[1]

    st.image("gfx/stat_ktn_logo.png", use_container_width=True)
    st.text('')
    st.image("gfx/stat_stmk_logo.png", use_container_width=True)
    st.text('')

# HÖCHSTE ABGESCHLOSSENE AUSBILDUNG
st.write('#### Höchste abgeschlossene Ausbildung der 20 bis 64-jährigen')

df = get_data('hoest_ausbildung.csv')
df = filter_gkz(df, 'GKZ')
df = df.groupby(['JAHR', 'HOEST_AUSBILDUNG']).agg({'ANZAHL': 'sum'}).reset_index()
df['JAHR_TOTAL'] = df.groupby('JAHR')['ANZAHL'].transform('sum')
df['ANTEIL'] = round(df['ANZAHL'] / df['JAHR_TOTAL'] * 100, 2)



stacked_bar_chart = alt.Chart(df).mark_bar().encode(
x=alt.X('JAHR:O', title='Jahr'),  
y=alt.Y('ANTEIL:Q', title='Anteil'),
color=alt.Color('HOEST_AUSBILDUNG:N', 
                title='Höchste Ausbildung', 
                #sort=group_order, 
                legend=alt.Legend(orient='bottom',
                                direction='vertical',
                                columns=2), 
                scale=alt.Scale(range=palette)),
order=alt.Order('ANTEIL:Q', 
                sort='descending'),
tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), 
         alt.Tooltip('HOEST_AUSBILDUNG:N', title='Höchste Ausbildung'),
         alt.Tooltip('ANTEIL:Q', title='Anteil')],
).properties(
width=800,
height=600
)

st.altair_chart(stacked_bar_chart, use_container_width=True)

### SCHÜLERPENDLER ###
st.write('#### Schülerpendler')
df = get_data('schueler.csv')

df['dem_hws_gcd'] = df['dem_hws_gcd'].astype(str)
df['ast_gcd'] = df['ast_gcd'].astype(str)
df = df[~(df['dem_hws_gcd'].isin(gkzList['gkz']) & df['ast_gcd'].isin(gkzList['gkz']))] # Binnenpendler innerhalb Koralmregion
    
df['TYPE'] = df.apply(lambda row:   'Auspendler KTN/STK' if row['dem_hws_gcd'] in gkzList['gkz'] and row['ast_gcd'] not in gkzList['gkz'] and len(row['ast_gcd']) == 5 and (row['ast_gcd'].startswith('2') or row['ast_gcd'].startswith('6')) else
                                        'Einpendler KTN/STK' if row['dem_hws_gcd'] not in gkzList['gkz'] and row['ast_gcd'] in gkzList['gkz'] and len(row['dem_hws_gcd']) == 5 and (row['dem_hws_gcd'].startswith('2') or row['dem_hws_gcd'].startswith('6'))  else
                                        'Auspendler Ö' if row['dem_hws_gcd'] in gkzList['gkz'] and row['ast_gcd'] not in gkzList['gkz'] and len(row['ast_gcd']) == 5 and (not row['ast_gcd'].startswith('2') or not row['ast_gcd'].startswith('6')) else
                                        'Einpendler Ö' if row['dem_hws_gcd'] not in gkzList['gkz'] and row['ast_gcd'] in gkzList['gkz'] and len(row['dem_hws_gcd']) == 5 and (not row['dem_hws_gcd'].startswith('2') or not row['dem_hws_gcd'].startswith('6')) else
                                        0, axis=1)
df = df[df['TYPE'] != 0]

#df = df.groupby(['JAHR', 'SEKTOR', 'TYPE']).agg({'ANZAHL': 'sum'}).reset_index()
df = df.groupby(['JAHR', 'TYPE']).agg({'ANZAHL': 'sum'}).reset_index()

auspendList = ['Auspendler KTN/STK', 'Auspendler Ö']
df.loc[df['TYPE'].isin(auspendList), 'ANZAHL'] = -df['ANZAHL']

df = filter_start_end_year(df, select_start_jahr, select_end_jahr)

df_saldo = df.groupby('JAHR', as_index=False)['ANZAHL'].sum()

df['ANZAHL_FORMATTED'] = df['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))
df_saldo['ANZAHL_FORMATTED'] = df_saldo['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))

line_chart = alt.Chart(df_saldo).mark_line().encode(
    x='JAHR:O',
    y='ANZAHL:Q',
    color=alt.value('red'),  # Set color for the line
    tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), 
             alt.Tooltip('ANZAHL_FORMATTED:N', title='Saldo')]
)
group_order = ['Einpendler KTN/STK', 'Auspendler KTN/STK', 'Einpendler Ö', 'Auspendler Ö']
stacked_bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('JAHR:O', title='Jahr'),  
    y=alt.Y('ANZAHL:Q', title='Anzahl'), 
    color=alt.Color('TYPE:N', 
                    title='Pendlertyp', 
                    sort=group_order, 
                    legend=alt.Legend(orient='bottom',
                    direction='vertical',
                    columns=2), 
                    scale=alt.Scale(range=[palette[0], palette[0], palette[1], palette[1]])),
    tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), 
             alt.Tooltip('TYPE:N', title='Pendlertyp'),
             alt.Tooltip('ANZAHL_FORMATTED:N', title='Anzahl')],
    ).properties(
    width=800,
    height=600
)

white_line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='white').encode(
    y='y'
)

combined_chart = alt.layer(stacked_bar_chart, line_chart, white_line).resolve_scale(
    #y='independent'  # Use independent y-axes for the two layers
)
st.altair_chart(combined_chart, use_container_width=True)

