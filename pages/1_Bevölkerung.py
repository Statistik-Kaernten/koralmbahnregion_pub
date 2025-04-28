from data import *
import altair as alt
from customize import *

# PAGE CONSTANTS
START_JAHR: int = 2002
END_JAHR: int = 2024

## PAGE CONFIG
st.set_page_config(page_title="Bevölkerung in der Koralmbahnregion", layout="wide")

## TITLE
st.title("Bevölkerung in der Koralmbahnregion")

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

    st.image("gfx/stat_ktn_logo.png", width=190)
    st.text('')
    st.image("gfx/stat_stmk_logo.png", width=150)
    st.text('')
    with st.expander(f''':orange[**INFO**]''', expanded=False):
        st.write(f'''
                 Quellen:  
                 Landesstelle für Statistik,  
                 Grundstückspreise: QUELLE HIER EINFÜGEN!!!
                 ''')

## BEVÖLKERUNG NACH ALTER
st.write("#### Bevölkerung nach Altersgruppen")

df = get_data('bevoelkerung.csv')
#df = filter_gkz(df, 'GKZ')
df = filter_start_end_year(df, select_start_jahr, select_end_jahr)
anteil_anzahl = st.toggle('Anteil/Anzahl', value=True)
#df['GKZ'] = df['GKZ'].astype(str)
#df['JAHR'] = df['JAHR'].astype(str)
#df = df.groupby(['JAHR', 'GRUPPE']).agg({'ANZAHL': 'sum'}).reset_index()
#df = df[['JAHR', 'GRUPPE', 'ANZAHL']]
#df.replace({'0-19': 'bis 20 Jahre', '20-64': 'zw. 20 und 64 Jahren', '65+': 'über 65 Jahre'}, inplace=True)

group_order = ['bis 20 Jahre', 'zw. 20 und 64 Jahren', 'über 65 Jahre']

if (anteil_anzahl == False):
    df['ANTEIL'] = df['ANZAHL'] / df.groupby('JAHR')['ANZAHL'].transform('sum') * 100
    df['ANTEIL_FORMATTED'] = df['ANTEIL'].apply(lambda x: handle_comma(str(round(x,1))))
    stacked_bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('JAHR:O', title='Jahr', axis=alt.Axis(labelAngle=45)),  
        y=alt.Y('ANTEIL:Q', title='Anteil'),
        color=alt.Color('GRUPPE:N', 
                        title='Altersgruppe', 
                        sort=group_order, 
                        scale=alt.Scale(domain=group_order, range=palette),
                        legend=alt.Legend(orient='bottom',
                                        direction='vertical',
                                        columns=3)),
        order=alt.Order('GRUPPE:N', 
                        sort='ascending'),
        tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), 
                alt.Tooltip('GRUPPE:N', title='Altersgruppe'),
                alt.Tooltip('ANTEIL_FORMATTED:N', title='Anteil')],
        ).properties(
                width=800,
                height=600
                ).configure_axis(
                    titleFontWeight='bold'
                ).configure_legend(
                    titleFontWeight='bold'  
                ).properties(
                usermeta={
                    "embedOptions": custom_locale
                }
            )
else:
    df['ANZAHL_FORMATTED'] = df['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))


    stacked_bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('JAHR:O', title='Jahr', axis=alt.Axis(labelAngle=45)),  
        y=alt.Y('ANZAHL:Q', title='Anzahl'),
        color=alt.Color('GRUPPE:N', 
                        title='Altersgruppe', 
                        sort=group_order, 
                        scale=alt.Scale(domain=group_order, range=palette),
                        legend=alt.Legend(orient='bottom',
                                        direction='vertical',
                                        columns=3)),
        order=alt.Order('GRUPPE:N', 
                        sort='ascending'),
        tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), 
                alt.Tooltip('GRUPPE:N', title='Altersgruppe'),
                alt.Tooltip('ANZAHL_FORMATTED:N', title='Anzahl')],
        ).properties(
                width=800,
                height=600
                ).configure_axis(
                    titleFontWeight='bold'
                ).configure_legend(
                    titleFontWeight='bold'  
                ).properties(
                usermeta={
                    "embedOptions": custom_locale
                }
            )

if not df.empty:
    st.altair_chart(stacked_bar_chart, use_container_width=True)
else:
    st.write(NO_DATA)


### WANDERUNGEN ###
st.write("#### Wanderungen nach Wanderungstyp")

df = get_data('wanderungen.csv')
df = filter_start_end_year(df, select_start_jahr, select_end_jahr)
#df['ort_je_h'] = df['ort_je_h'].astype(str)
#df['ort_je_z'] = df['ort_je_z'].astype(str)

#df = df[~((df['ort_je_h'].isin(gkzList['gkz'])) & (df['ort_je_z'].isin(gkzList['gkz'])))]
 # Umzüge innerhalb Koralmregion

#df['ZUAB'] = df.apply(lambda row: 1 if row['ort_je_h'] in gkzList['gkz'] else 2 if row['ort_je_z'] in gkzList['gkz'] else 0, axis=1)
#df = df[df['ZUAB'] != 0]
#df['TYPE'] = df.apply(lambda row:   'Abwanderung KTN/STK' if row['ZUAB'] == 1 and len(row['ort_je_z']) == 5 and (row['ort_je_z'].startswith('2') or row['ort_je_z'].startswith('6')) else
#                                        'Zuwanderung KTN/STK' if row['ZUAB'] == 2 and len(row['ort_je_h']) == 5 and (row['ort_je_h'].startswith('2') or row['ort_je_h'].startswith('6')) else
#                                        'Abwanderung Ö' if row['ZUAB'] == 1 and len(row['ort_je_z']) == 5 and (not row['ort_je_z'].startswith('2') or not row['ort_je_z'].startswith('6')) else
#                                        'Zuwanderung Ö' if row['ZUAB'] == 2 and len(row['ort_je_h']) == 5 and (not row['ort_je_h'].startswith('2') or not row['ort_je_h'].startswith('6')) else
#                                        'Abwanderung Ausland' if row['ZUAB'] == 1 and len(row['ort_je_z']) != 5 else
#                                        'Zuwanderung Ausland' if row['ZUAB'] == 2 and len(row['ort_je_h']) != 5 else
#                                        0, axis=1 )
findmax = df.groupby('JAHR').agg({'ANZAHL': 'sum'}).reset_index()
max_value = max(abs(findmax['ANZAHL'].min()), abs(findmax['ANZAHL'].max()))

#df = df.groupby(['JAHR', 'TYPE']).agg({'ANZAHL': 'sum'}).reset_index()
#abwList = ['Abwanderung KTN/STK', 'Abwanderung Ö', 'Abwanderung Ausland']
#df.loc[df['TYPE'].isin(abwList), 'ANZAHL'] = -df['ANZAHL']

df_saldo = df.groupby('JAHR', as_index=False)['ANZAHL'].sum()


df['ANZAHL_FORMATTED'] = df['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))
df_saldo['ANZAHL_FORMATTED'] = df_saldo['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))

only_line_chart = alt.Chart(df_saldo).mark_line(size=5).encode(
    x='JAHR:O',
    y='ANZAHL:Q',
    color=alt.value(palette[6]),  # Set color for the line
    tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), 
             alt.Tooltip('ANZAHL_FORMATTED:N', title='Saldo')]
)

#text_labels = alt.Chart(df_saldo).mark_text(
#    align='center',
#    baseline='middle',
#    dy=-10 # Adjust the vertical position of the text (up or down from the points)
#).encode(
#    x='JAHR:O',
#    y='ANZAHL_FORMATTED:Q',
#    text='ANZAHL_FORMATTED'
#)

#line_chart = only_line_chart + text_labels
group_order = ['Zuwanderung KTN/STK', 'Abwanderung KTN/STK', 'Zuwanderung Ö', 'Abwanderung Ö', 'Zuwanderung Ausland', 'Abwanderung Ausland']

stacked_bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('JAHR:O', title='Jahr', axis=alt.Axis(labelAngle=45)),  
    y=alt.Y('ANZAHL:Q', title='Anzahl', #scale=alt.Scale(domain=[-max_value/2, max_value/2])
            ), 
    color=alt.Color('TYPE:N', 
                     title='Wanderungstyp', 
                    sort=group_order, 
                    legend=alt.Legend(orient='bottom',
                    direction='vertical',
                    columns=4), 
                    scale=alt.Scale(domain=['Zuwanderung KTN/STK', 'Abwanderung KTN/STK', 'Zuwanderung Ö', 'Abwanderung Ö', 'Zuwanderung Ausland', 'Abwanderung Ausland', 'Saldo'], 
                                    range=[palette[0], palette[0], palette[1], palette[1], palette[2], palette[2], palette[6]])
                   ),
    tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), 
             alt.Tooltip('TYPE:N', title='Wanderungstyp'),
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

#selected_saldo = st.checkbox('Wanderungssaldo', True, disabled=True)

combined_chart = alt.layer(stacked_bar_chart, only_line_chart, white_line, hover_points).configure_axis(
            titleFontWeight='bold'  
        ).configure_legend(
            titleFontWeight='bold'  
        )


if not df.empty:
    st.altair_chart(combined_chart, use_container_width=True)
else:
    st.write(NO_DATA)


### GRUNDSTÜCKSPREISE ###
st.write("#### Durchschnittliche Grundstückspreise")
df = get_data('grundstueckspreise.csv')
#df = filter_gkz(df, 'GKZ')
df = filter_start_end_year(df, select_start_jahr, select_end_jahr)
#df = df.groupby(['JAHR', 'GEMTYPE']).agg({'Preis': 'mean'}).reset_index()
df['Preis_FORMATTED'] = df['Preis'].apply(lambda x: handle_comma(x))
group_order=['< 5.000 EW', '5.000 - 10.000 EW', '10.000 - 50.000 EW', '> 50.000 EW']

line_chart = alt.Chart(df).mark_line(size=5).encode(
    x=alt.X('JAHR:O', title='Jahr', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Preis:Q', title='Preis pro m²'),
    color=alt.Color('GEMTYPE:N', 
                    title='Gemeinden mit ...',
                    sort=group_order,
                    legend=alt.Legend(orient='bottom',
                    direction='vertical',
                    columns=4),
                    scale=alt.Scale(range=[palette[0], palette[1], palette[2], palette[3]])),  
    tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), alt.Tooltip('Preis_FORMATTED:N', title='Preis pro m²')]
).properties(
    width=800,
    height=600
).configure_axis(
    titleFontWeight='bold'  
).configure_legend(
    titleFontWeight='bold'  
)
if not df.empty:
    st.altair_chart(line_chart, use_container_width=True)
else:
    st.write(NO_DATA)

### WOHNUNGEN ###
st.write("#### Wohnungen nach Bauperiode")

#bauperiode_mapping = {'Vor 1919': 'bis 1960',
#                      '1919 bis 1944': 'bis 1960',
#                       '1945 bis 1960':  'bis 1960',
#                       '1961 bis 1970': '1961 bis 1970',
#                       '1971 bis 1980': '1971 bis 1980',
#                       '1981 bis 1990': '1981 bis 1990',
#                       '1991 bis 2000': '1991 bis 2000',
#                       '2001': '2001 bis 2010',
#                       '2002': '2001 bis 2010',
#                       '2003': '2001 bis 2010',
#                       '2004': '2001 bis 2010',
#                       '2005': '2001 bis 2010',
#                       '2006': '2001 bis 2010',
#                       '2007': '2001 bis 2010',
#                       '2008': '2001 bis 2010',
#                       '2009': '2001 bis 2010',
#                       '2010': '2001 bis 2010',
#                       '2011': '2011 bis 2020',
#                        '2012': '2011 bis 2020',
#                        '2013': '2011 bis 2020',
#                        '2014': '2011 bis 2020',
#                        '2015': '2011 bis 2020',
#                        '2016': '2011 bis 2020',
#                        '2017': '2011 bis 2020',
#                        '2018': '2011 bis 2020',
#                        '2019': '2011 bis 2020',
#                        '2020': '2011 bis 2020',
#                        '2021': '2021 bis 2022',
#                        '2022': '2021 bis 2022'}


df = get_data('wohnungen.csv')
#df = filter_gkz(df, 'GKZ')
df = filter_start_end_year(df, select_start_jahr, select_end_jahr)
#df['BAUPERIODE_A'] = df['BAUPERIODE'].apply(lambda x: bauperiode_mapping.get(x))
#df = df.groupby(['JAHR', 'BAUPERIODE_A']).agg({'ANZAHL': 'sum'}).reset_index()
df['ANZAHL_FORMATTED'] = df['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))

group_order = ['bis 1960']
stacked_bar_chart = alt.Chart(df).mark_bar().encode(
x=alt.X('JAHR:O', title='Jahr', axis=alt.Axis(labelAngle=0)),  
y=alt.Y('ANZAHL:Q', title='Anzahl'),
color=alt.Color('BAUPERIODE_A:N', 
                title='Bauperiode', 
                sort=group_order, 
                legend=alt.Legend(orient='bottom',
                                direction='vertical',
                                columns=8), 
                scale=alt.Scale(range=palette)),
order=alt.Order('ANZAHL:Q', 
                sort='descending'),
tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), 
         alt.Tooltip('BAUPERIODE_A:N', title='Bauperiode'),
         alt.Tooltip('ANZAHL_FORMATTED:N', title='Anzahl')],
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
#df = df.groupby('JAHR').agg({'Preis': 'mean'}).reset_index()