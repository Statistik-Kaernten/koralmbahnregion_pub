from data import *
import altair as alt
from misc.customize import *

# PAGE CONSTANTS
START_JAHR: int = 2004
END_JAHR: int = 2025

## PAGE CONFIG
st.set_page_config(page_title="Arbeitsmarkt in der Koralmbahnregion", layout="wide")

## TITLE
st.title("Arbeitsmarkt in der Koralmbahnregion")

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

### ERWERBSPENDLER ###
st.write('#### Ein- und  Auspendler')
df = get_data('erwerbstaetige.csv')

df['dem_hws_gcd'] = df['dem_hws_gcd'].astype(str)
df['ast_gcd'] = df['ast_gcd'].astype(str)
df = df[~((df['dem_hws_gcd'].isin(gkzList['gkz'])) & (df['ast_gcd'].isin(gkzList['gkz'])))] # Binnenpendler innerhalb Koralmregion
    
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

group_order = ['Einpendler KTN/STK', 'Auspendler KTN/STK', 'Einpendler Ö', 'Auspendler Ö']
df['ANZAHL_FORMATTED'] = df['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))
df_saldo['ANZAHL_FORMATTED'] = df_saldo['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))

line_chart = alt.Chart(df_saldo).mark_line().encode(
    x='JAHR:O',
    y='ANZAHL:Q',
    color=alt.value('red'),  # Set color for the line
    tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), alt.Tooltip('ANZAHL_FORMATTED:N', title='Saldo')]
)

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


### ARBEITSSTAETTEN ###
st.write('#### Arbeitsstätten nach Größengruppen')

df = get_data('arbeitsstaetten.csv')
df = filter_gkz(df, 'GKZ')
df = df.groupby(['JAHR', 'GRUPPE']).agg({'ANZAHL': 'sum'}).reset_index()

#line_chart = alt.Chart(df).mark_line().encode(
#    x='JAHR:O',  # Ordinal scale for year
#    y='ANZAHL:Q',  # Quantitative scale for the value
#    color='GRUPPE:N',  # Categorical scale for GRUPPE (this will assign different colors)
#    tooltip=['JAHR', 'GRUPPE', 'ANZAHL']  # Optional: add tooltip for interactivity
#)
group_order = ['1 Beschäftigter', '2-4 Beschäftigte', '5-9 Beschäftigte', '10-19 Beschäftigte', '20-49 Beschäftigte', '50-99 Beschäftigte', '100-249 Beschäftigte', '250-499 Beschäftigte', '500-999 Beschäftigte', '1.000 und mehr Beschäftigte']
df['ANZAHL_FORMATTED'] = df['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))

line_chart = alt.Chart(df).mark_line().encode(
    x=alt.X('JAHR:O', title='Jahr'),
    y=alt.Y('sum(ANZAHL)', title='Anzahl').scale(type="log"),
    color=alt.Color('GRUPPE:N', sort=group_order),
    tooltip=[alt.Tooltip('JAHR:O', title='Jahr'), 
             alt.Tooltip('GRUPPE:N', title='Arbeitsstätte'),
             alt.Tooltip('ANZAHL_FORMATTED:N', title='Anzahl')]
).properties(
    width=800,
    height=600
)

st.altair_chart(line_chart, use_container_width=True)

### ARBEITSLOSE ###
st.write('#### Arbeitslose nach Geschlecht')

df = get_data('arbeitslose.csv')
df = filter_gkz(df, 'GKZ')
df = df.groupby(['DATUM', 'GESCHLECHT']).agg({'ANZAHL': 'sum'}).reset_index()
df['ANZAHL_FORMATTED'] = df['ANZAHL'].apply(lambda x: add_thousand_dot(str(x)))
stacked_bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('DATUM:O', title='Jahr'),  
    y=alt.Y('ANZAHL:Q', title='Anzahl'), 
    color=alt.Color('GESCHLECHT:N', 
                    title='Pendlertyp', 
                    #sort=group_order, 
                    legend=alt.Legend(orient='bottom',
                    direction='vertical',
                    columns=1 ), 
                    scale=alt.Scale(range=palette)),
    tooltip=[alt.Tooltip('DATUM:O', title='Monat'), 
             alt.Tooltip('GESCHLECHT:N', title='Geschlecht'),
             alt.Tooltip('ANZAHL_FORMATTED:N', title='Anzahl')],
    ).properties(
    width=800,
    height=600
)

st.altair_chart(stacked_bar_chart, use_container_width=True)


### TOURISMUS
st.write('#### Nächtigungen nach Monaten')

monats_name_mapping = {'1': 'Jänner', '2': 'Feber', '3': 'März', '4':' April', '5': 'Mai', '6': 'Juni', '7': 'Juli', '8': 'August', '9': 'September', '10': 'Oktober', '11': 'November', '12': 'Dezember'}

df = get_data('tourismus.csv')
df = filter_gkz(df, 'GKZ')
df = df.groupby(['JAHR', 'MONAT']).agg({'UEBERNACHTUNGEN': 'sum'}).reset_index()

#df = calcDifference(df, distance_for_calc_diff)
df = df[df['JAHR'] >= select_start_jahr]
df = df[df['JAHR'] <= select_end_jahr]
#df = df[~((df['JAHR'] < select_start_jahr))]

df['ANZAHL_FORMATTED'] = df['UEBERNACHTUNGEN'].apply(lambda x: add_thousand_dot(str(x)))
df['MONAT_NAME'] = df['MONAT'].apply(lambda x: monats_name_mapping.get(str(x)))
stacked_bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('JAHR:O', 
                title='Jahr'),
        y=alt.Y('UEBERNACHTUNGEN:Q', 
                title='Anzahl'
                ),
        color=alt.Color(
            'MONAT:N', 
            title='Monat', 
            scale=alt.Scale(range=palette),
            legend=None
        ),
        order=alt.Order('JAHR:N', sort='ascending'),
        tooltip=[
            alt.Tooltip('JAHR:O', 
                        title='Jahr'), 
            alt.Tooltip('MONAT_NAME:N', 
                        title='Monat'), 
            alt.Tooltip('ANZAHL_FORMATTED:N', 
                        title='Anzahl'),
            #alt.Tooltip(f'{diff}:O', 
            #            title='Veränderung zum Vorjahr'),
            #alt.Tooltip(f'Durchschnittliche Verweildauer:O', 
            #            title='Durchschnittliche Verweildauer')
        ],
    ).properties(
        width=800,
        height=600
    )

st.altair_chart(stacked_bar_chart, use_container_width=True)