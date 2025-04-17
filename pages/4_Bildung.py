from data import *
import altair as alt
from customize import *

# PAGE CONSTANTS
START_JAHR: int = 2011
END_JAHR: int = 2023

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
            value=(START_JAHR, END_JAHR),
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
df = filter_start_end_year(df, select_start_jahr, select_end_jahr)
#df = filter_gkz(df, 'GKZ')
#df = df.groupby(['JAHR', 'HOEST_AUSBILDUNG']).agg({'ANZAHL': 'sum'}).reset_index()
#df['JAHR_TOTAL'] = df.groupby('JAHR')['ANZAHL'].transform('sum')
#df['ANTEIL'] = round(df['ANZAHL'] / df['JAHR_TOTAL'] * 100, 2)
df['ANTEIL_FORMATTED'] = df['ANTEIL'].apply(lambda x: handle_comma(x))
order_map = ({'Pflichtschule': 1, 'Lehrabschluss': 2, 'Mittlere und höhere Schule': 3, 'Hochschule und Akademie': 4})
group_order = ['Pflichtschule', 'Lehrabschluss', 'Mittlere und höhere Schule', 'Hochschule und Akademie']
df['ORDER'] = df['HOEST_AUSBILDUNG'].apply(lambda x: order_map.get(x))

stacked_bar_chart = alt.Chart(df).mark_bar().encode(
x=alt.X('JAHR:O', title='Jahr'),  
y=alt.Y('ANTEIL:Q', title='Anteil'),
color=alt.Color('HOEST_AUSBILDUNG:N', 
                title='Höchste abg. Ausbildung', 
                sort=group_order, 
                legend=alt.Legend(orient='bottom',
                                direction='vertical',
                                columns=4), 
                scale=alt.Scale(range=palette)
                ),
order=alt.Order('ORDER:O', 
                sort='ascending'),
tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), 
         alt.Tooltip('HOEST_AUSBILDUNG:N', title='Höchste Ausbildung'),
         alt.Tooltip('ANTEIL_FORMATTED:N', title='Anteil')],
).properties(
width=800,
height=600
).configure_axis(
            titleFontWeight='bold'  
        ).configure_legend(
            titleFontWeight='bold'  
        )
if not df.empty:
    st.altair_chart(stacked_bar_chart, use_container_width=True)
else:
    st.write(NO_DATA)
df = df[['JAHR', 'HOEST_AUSBILDUNG', 'ANTEIL']]
### SCHÜLERPENDLER ###
st.write('#### Schülerpendler')
df = get_data('schueler.csv')

#df['dem_hws_gcd'] = df['dem_hws_gcd'].astype(str)
#df['ast_gcd'] = df['ast_gcd'].astype(str)
#df = df[~(df['dem_hws_gcd'].isin(gkzList['gkz']) & df['ast_gcd'].isin(gkzList['gkz']))] # Binnenpendler innerhalb Koralmregion
    
#df['TYPE'] = df.apply(lambda row:   'Auspendler KTN/STK' if row['dem_hws_gcd'] in gkzList['gkz'] and row['ast_gcd'] not in gkzList['gkz'] and len(row['ast_gcd']) == 5 and (row['ast_gcd'].startswith('2') or row['ast_gcd'].startswith('6')) else
#                                        'Einpendler KTN/STK' if row['dem_hws_gcd'] not in gkzList['gkz'] and row['ast_gcd'] in gkzList['gkz'] and len(row['dem_hws_gcd']) == 5 and (row['dem_hws_gcd'].startswith('2') or row['dem_hws_gcd'].startswith('6'))  else
#                                        'Auspendler Ö' if row['dem_hws_gcd'] in gkzList['gkz'] and row['ast_gcd'] not in gkzList['gkz'] and len(row['ast_gcd']) == 5 and (not row['ast_gcd'].startswith('2') or not row['ast_gcd'].startswith('6')) else
#                                        'Einpendler Ö' if row['dem_hws_gcd'] not in gkzList['gkz'] and row['ast_gcd'] in gkzList['gkz'] and len(row['dem_hws_gcd']) == 5 and (not row['dem_hws_gcd'].startswith('2') or not row['dem_hws_gcd'].startswith('6')) else
#                                        0, axis=1)
#df = df[df['TYPE'] != 0]

##df = df.groupby(['JAHR', 'SEKTOR', 'TYPE']).agg({'ANZAHL': 'sum'}).reset_index()
#df = df.groupby(['JAHR', 'TYPE']).agg({'ANZAHL': 'sum'}).reset_index()

#auspendList = ['Auspendler KTN/STK', 'Auspendler Ö']
#df.loc[df['TYPE'].isin(auspendList), 'ANZAHL'] = -df['ANZAHL']

df = filter_start_end_year(df, select_start_jahr, select_end_jahr)

df_saldo = df.groupby('JAHR', as_index=False)['ANZAHL'].sum()

df['ANZAHL_FORMATTED'] = df['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))
df_saldo['ANZAHL_FORMATTED'] = df_saldo['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))

line_chart = alt.Chart(df_saldo).mark_line(size=4).encode(
    x='JAHR:O',
    y='ANZAHL:Q',
    color=alt.value(palette[6]),  # Set color for the line
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
                    columns=3), 
                    scale=alt.Scale(domain=['Einpendler KTN/STK', 'Auspendler KTN/STK', 'Einpendler Ö', 'Auspendler Ö', 'Saldo'], 
                                    range=[palette[0], palette[0], palette[1], palette[1], palette[6]])),
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

hover_points = alt.Chart(df_saldo).mark_circle(size=HOVER_SIZE, opacity=HOVER_OPACITY).encode(
    x='JAHR:O',
    y='ANZAHL:Q',
    tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), alt.Tooltip('ANZAHL_FORMATTED:N', title='Saldo')]  # Still works with tooltip
)


combined_chart = alt.layer(stacked_bar_chart, line_chart, white_line, hover_points).configure_axis(
            titleFontWeight='bold'  
        ).configure_legend(
            titleFontWeight='bold'  
        )

if not df.empty:
    st.altair_chart(combined_chart, use_container_width=True)
else:
    st.write(NO_DATA)
