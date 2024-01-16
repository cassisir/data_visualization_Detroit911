import sys
import os
current_script_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_script_directory)
sys.path.append(parent_directory)
from data_processing import data_processor
from card_creator import CardCreator
from dashboard_utils import convert_minutes_to_minutes_seconds, filter_data, H4_style
from dash import Dash, html, dcc, Output, Input, State, dash_table, callback
import dash
import dash_bootstrap_components as dbc
import datetime
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster

dash.register_page(__name__, path='/dashboard', name='Dashboard')

# Dataset imported from presentation.py
data = data_processor.data

### Creation of the cards ###
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#393F85',
    'color': 'white',
    'padding': '6px'
}

card_creator = CardCreator(tab_style, tab_selected_style)

card_callscount = card_creator.create_callscount_card()
card_averagetimes = card_creator.create_averagetimes_card()
card_bestunits = card_creator.create_bestunits_card()
card_histogram = card_creator.create_histogram_card()
card_linechartcount = card_creator.create_linechartcount_card()
card_disposition = card_creator.create_dispositions_card()
card_map = card_creator.create_map_card()

### End Creation of the cards ###

layout = dbc.Container([

    #Gestion des paramètres
    dbc.Row([
        # Date picker range
        dbc.Col([
            dcc.DatePickerRange(
                min_date_allowed=datetime.date(2016, 1, 1),
                max_date_allowed=datetime.date(2016, 6, 28),              
                start_date=datetime.date(2016, 1, 1),
                end_date=datetime.date(2016, 6, 28),
                number_of_months_shown=3,
                display_format='DD MMM, YY',
                id='date_picker_range',
            )   
                
        ], width=2, className='mb-4'),
        # Dropdown category
        dbc.Col([
            dcc.Dropdown(
                id='dropdown_category', 
                options=sorted(data.category.unique()),
                placeholder='All categories',
                multi=True,
                style=({'backgroundColor': '#121212'})
            )   
        ],width=3, className='mb-4'),
        # Dropdown period
        dbc.Col([
            dcc.Dropdown(
                id='dropdown_period', 
                options=['Morning', 'Afternoon', 'Evening', 'Night'],
                placeholder='Full day',
                multi=True,
                style=({'backgroundColor': '#121212'})
            )                         
        ], width=3, className='mb-4'),
        dbc.Col([
            # Dropdown day
            dcc.Dropdown(
                id='dropdown_day', 
                options=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                placeholder='Entire week',
                multi=True,
                style=({'backgroundColor': '#121212'})
            )
        ],width=3, className='mb-4'),
    ]),
    #Calls count + Average time + Best units
    dbc.Row([
        dbc.Col([
            card_callscount
        ],width=4),
        dbc.Col([
            card_averagetimes
        ],width=4),
        dbc.Col([
            card_bestunits
        ],width=4)
    ], className='mb-3'),
    #histogram + Count linechart + Dispositions
    dbc.Row([
        dbc.Col([
            card_histogram
        ],width=4),
        dbc.Col([
            card_linechartcount
        ],width=4),
        dbc.Col([
            card_disposition
        ],width=4)
    ], className='mb-3'),
    #Carte
    dbc.Row([
        dbc.Col([
            card_map
        ])
    ], className='mt-1 mb-3')
    
], fluid=True)

### Callbacks interactivity ###
@callback(
    Output(component_id='bestunits', component_property='children'),
    Input(component_id='dropdown_category', component_property='value'),
    Input(component_id='date_picker_range', component_property='start_date'),
    Input(component_id='date_picker_range', component_property='end_date'),
    Input(component_id='dropdown_period', component_property='value'),
    Input(component_id='dropdown_day', component_property='value')
)
def update_bestunits(selected_categories, start_date, end_date, selected_periods, selected_days):
    df = filter_data(selected_categories, start_date, end_date, selected_periods, selected_days, data)
    bestunits = df.groupby(df.respondingunit).size().reset_index(name='count').sort_values(by='count', ascending=False)
    bestunits = bestunits.iloc[:3]

    best_text = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H4('Rank', style=H4_style),
                    html.Br()
                ]),
                dbc.Col([
                    html.H4('Unit', style=H4_style, className='text-center'),
                    html.Br()
                ]),
                dbc.Col([
                    html.H4('Total calls', style=H4_style),
                    html.Br()
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4('1st.', style=H4_style)
                ]),
                dbc.Col([
                    html.H4(bestunits.iloc[0]['respondingunit'], style=H4_style, className='text-center')
                ]),
                dbc.Col([
                    html.H4(str(bestunits.iloc[1]['count']), style=H4_style, className='text-center')
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4('2nd.', style=H4_style)
                ]),
                dbc.Col([
                    html.H4(bestunits.iloc[1]['respondingunit'], style=H4_style, className='text-center')
                ]),
                dbc.Col([
                    html.H4(str(bestunits.iloc[1]['count']), style=H4_style, className='text-center')
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4('3rd.', style=H4_style)
                ]),
                dbc.Col([
                    html.H4(bestunits.iloc[2]['respondingunit'], style=H4_style, className='text-center')
                ]),
                dbc.Col([
                    html.H4(str(bestunits.iloc[2]['count']), style=H4_style, className='text-center')
                ])
            ])
        ])
    return best_text


@callback(
    Output(component_id='calls_number', component_property='children'),
    Input(component_id='dropdown_category', component_property='value'),
    Input(component_id='date_picker_range', component_property='start_date'),
    Input(component_id='date_picker_range', component_property='end_date'),
    Input(component_id='dropdown_period', component_property='value'),
    Input(component_id='dropdown_day', component_property='value')
)
def update_calls_number(selected_categories, start_date, end_date, selected_periods, selected_days):
    df = filter_data(selected_categories, start_date, end_date, selected_periods, selected_days, data)
    number_of_calls = df.shape[0]
    return(f'{number_of_calls:,}'.replace(',', ' '))


@callback(
        Output(component_id='tabs_histogram_content', component_property='children'),
        Input(component_id='tabs_histogram', component_property='value'),
        Input(component_id='dropdown_category', component_property='value'),
        Input(component_id='radioItems_time', component_property='value'),
        Input(component_id='date_picker_range', component_property='start_date'),
        Input(component_id='date_picker_range', component_property='end_date'),
        Input(component_id='dropdown_period', component_property='value'),
        Input(component_id='dropdown_day', component_property='value')
)
def update_histogram(tab, selected_categories, selected_time, start_date, end_date, selected_periods, selected_days):
    df = filter_data(selected_categories, start_date, end_date, selected_periods, selected_days, data)
    # Filtrage de tous les appels ayant mené à l'intervention d'une unité (donc ayant un traveltime)
    if(selected_time=='traveltime'):
        df = df.query('not (respondingunit.isna() and traveltime==0) and officerinitiated==False')

    ## histogram
    if tab=='tab_grouped' :
        histogram = px.histogram(df, x=selected_time, range_x=[0,30], barmode='overlay', template="plotly_dark")
        
    elif tab=='tab_separated' :
        histogram = px.histogram(df, x=selected_time, color="category", range_x=[0,30], barmode='overlay', template="plotly_dark")
    # Titre
    histogram.update_layout(title_text=f"Histogram of the {selected_time} for the selected categories on the selected period.")

    return dcc.Graph(id='histogram', figure=histogram)


@callback(
        Output(component_id='tabs_linechartCount_content', component_property='children'),
        Input(component_id='tabs_linechartCount', component_property='value'),
        Input(component_id='dropdown_category', component_property='value'),
        Input(component_id='date_picker_range', component_property='start_date'),
        Input(component_id='date_picker_range', component_property='end_date'),
        Input(component_id='dropdown_period', component_property='value'),
        Input(component_id='dropdown_day', component_property='value'),
        Input(component_id='radioItems_scale', component_property='value')
)
def update_linechart(tab,selected_categories, start_date, end_date, selected_periods, selected_days, selected_scale):
    df = filter_data(selected_categories, start_date, end_date, selected_periods, selected_days, data)
    if selected_scale=='Monthly' :
        df['calldate'] = pd.to_datetime(df['calldate']).dt.month
    if tab=='tab_grouped' :
        calls_by__month = df.groupby(['calldate']).size().reset_index(name='call_count')
        linechart = px.line(calls_by__month, x='calldate', y='call_count', markers=True, height=450, template="plotly_dark")
    if tab=='tab_separated' :
        calls_by_category_and_month = df.groupby(['category', 'calldate']).size().reset_index(name='call_count')
        linechart = px.line(calls_by_category_and_month, x='calldate', y='call_count', color='category', markers=True, height=450, template="plotly_dark")
    
    if selected_scale == 'Monthly':
        linechart.update_layout(xaxis_title='Months', yaxis_title='Number of calls')
    
    # Reduce the legend's size
    linechart.update_layout(
        legend=dict(
            traceorder='normal',
            font=dict(size=5),  # Adjust the font size here
            itemsizing='constant'  # Adjust the item sizing
        )
    )

    # Titre
    linechart.update_layout(title_text=f"Number of calls over time for the selected categories on the selected period.")
    return dcc.Graph(id='linechart_count', figure=linechart)


@callback(
    Output(component_id='tabs_time_content', component_property='children'),
    Input(component_id='tabs_time', component_property='value'),
    Input(component_id='dropdown_category', component_property='value'),
    Input(component_id='date_picker_range', component_property='start_date'),
    Input(component_id='date_picker_range', component_property='end_date'),
    Input(component_id='dropdown_period', component_property='value'),
    Input(component_id='dropdown_day', component_property='value')
)
def update_averagetimes(tab, selected_categories, start_date, end_date, selected_periods, selected_days):
    df = filter_data(selected_categories, start_date, end_date, selected_periods, selected_days, data)

    # Calcul des temps moyens :
    intakeMean = df.intaketime.mean()
    dispatchMean = df.dispatchtime.mean()
    travelMean = df.traveltime.mean()
    onsceneMean = df.timeonscene.mean()
    totalMean = df.totaltime.mean()

    if tab=='tab_text' :
        # Affichage sous forme de texte :
        intakeMean = convert_minutes_to_minutes_seconds(intakeMean)
        dispatchMean = convert_minutes_to_minutes_seconds(dispatchMean)
        travelMean = convert_minutes_to_minutes_seconds(travelMean)
        onsceneMean = convert_minutes_to_minutes_seconds(onsceneMean)
        totalMean = convert_minutes_to_minutes_seconds(totalMean)
        return html.Div([
            html.H4("Intake time : "+ intakeMean, style=H4_style, className='mt-2 mb-3'),
            html.H4("Dispatch time : "+ dispatchMean, style=H4_style, className='mb-3'),
            html.H4("Travel time : "+ travelMean, style=H4_style, className='mb-3'),
            html.H4("Time on scene : "+ onsceneMean, style=H4_style, className='mb-3'),
            html.H4("Total time : "+ totalMean, style=H4_style, className='mb-3')
        ])
    
    elif tab=='tab_piechart' :
        times = ['Intake', 'Dispatch', 'Travel', 'On Scene']
        values = [intakeMean,dispatchMean,travelMean,onsceneMean]
        df_time = pd.DataFrame({'Times': times, 'Values': values})
        piechart = px.pie(df_time, names='Times', values='Values', title='Average Times Distribution', hole=0.6, height=320, template="plotly_dark")
        
        return dcc.Graph(id='piechart', figure=piechart)


@callback(
    Output(component_id='tabs_map_content', component_property='children'),
    Input(component_id='tabs_map', component_property='value'),
    Input(component_id='dropdown_category', component_property='value'),
    Input(component_id='date_picker_range', component_property='start_date'),
    Input(component_id='date_picker_range', component_property='end_date'),
    Input(component_id='dropdown_period', component_property='value'),
    Input(component_id='dropdown_day', component_property='value')
)
def update_map(tab, selected_categories, start_date, end_date, selected_periods, selected_days):
    # Filtrage
    df = filter_data(selected_categories, start_date, end_date, selected_periods, selected_days, data)
    
    if tab=='tab_choropleth':
        calls_by_zipcode = df.groupby(['zipcode']).count().reset_index()
        occurences = calls_by_zipcode[['zipcode', 'callno']]

        # Création de la carte
        center = (42.36873, -83.07779)
        map = folium.Map(location=center, tiles='OpenStreetMap', zoom_start=12)

        folium.Choropleth(
            geo_data=data_processor.zipcode_gdf,
            name='choropleth',
            data=occurences,
            columns=['zipcode', 'callno'],
            key_on='feature.properties.zipcode',
            fil_color='Reds',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Number of calls',
            zoom=5
        ).add_to(map)
        # Conversion de la carte en string HTML
        map_html = map.get_root().render()
    
    elif tab=='tab_markers':
        merged_df_cat = df.dropna(subset=['zipcode'])
        merged_df_cat = merged_df_cat.groupby(['incident_address','category', 'latitude', 'longitude']).size().reset_index(name='Count')
        merged_df_cat = merged_df_cat.drop_duplicates(subset=['incident_address','category'], keep='first')
        # Création de la carte
        center = (42.36873, -83.07779)
        map = folium.Map(location=center, zoom_start=12)
        marker_cluster = MarkerCluster().add_to(map)
        for _, row in merged_df_cat.iterrows():
            folium.Marker(
                location=(row['latitude'], row['longitude']),
                popup=f"{row['incident_address']}\n({row['Count']} incidents) (Category : {row['category']})",
            ).add_to(marker_cluster)
        # Conversion de la carte en string HTML
        map_html = marker_cluster.get_root().render()
    
    return html.Iframe(id='map', srcDoc=map_html, width="100%", height="600", className='mt-4')


@callback(
        Output(component_id='tabs_disposition_content', component_property='children'),
        Input(component_id='tabs_disposition', component_property='value'),
        Input(component_id='dropdown_category', component_property='value'),
        Input(component_id='date_picker_range', component_property='start_date'),
        Input(component_id='date_picker_range', component_property='end_date'),
        Input(component_id='dropdown_period', component_property='value'),
        Input(component_id='dropdown_day', component_property='value'),
        Input(component_id='radioItems_scale_disposition', component_property='value')
)
def update_disposition(tab, selected_categories, start_date, end_date, selected_periods, selected_days, selected_scale):
    df = filter_data(selected_categories, start_date, end_date, selected_periods, selected_days, data)
    
    if selected_scale=='Monthly' :
        df['calldate'] = pd.to_datetime(df['calldate']).dt.month

    if tab=='tab_linechart' :
        calls_by_disposition_and_date = df.groupby(['disposition', 'calldate']).size().reset_index(name='call_count')
        disposition_graph = px.line(calls_by_disposition_and_date, x='calldate', y='call_count', color='disposition', markers=True, height=450, template="plotly_dark")
    elif tab=='tab_barchart' :
        calls_by_disposition = df.groupby(['disposition']).size().reset_index(name='count').sort_values(by='count')
        disposition_graph = px.bar(calls_by_disposition, x='count', y='disposition', text='count', template='plotly_dark')
        disposition_graph.update_traces(textfont_size=14)
        disposition_graph.update_traces(textposition='outside', textfont_size=14, textfont_color='white', insidetextanchor='start')

    disposition_graph.update_layout(title_text=f"Dispositions over time for the selected categories on the selected period.")
    return dcc.Graph(id='disposition_graph', figure=disposition_graph)

### End of interactivity ###
