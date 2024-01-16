import dash_bootstrap_components as dbc
from dash import dcc, html
from dashboard_utils import H2_style, H3_style, H5_style
class CardCreator:
    def __init__(self, tab_style=None, tab_selected_style=None):
        self.tab_style = tab_style
        self.tab_selected_style = tab_selected_style

    @staticmethod
    def create_tabbed_card(title, tabs, content_id, card_description=None, additional_content=None):
        card_content = [
            html.H3([title], style=H3_style, className="mb-3"),
            dcc.Tabs(
                id=f"tabs_{content_id}",
                value=tabs[0]['value'],
                children=[dcc.Tab(**tab) for tab in tabs]
            ),
            dcc.Loading(type='dot', children=[html.Div(id=f"tabs_{content_id}_content")])
        ]

        if additional_content:
            card_content.extend(additional_content)

        card = dbc.Card([dbc.CardBody(card_content), dbc.CardFooter(card_description)])
        return card
   
    @staticmethod
    def create_person_card(name, description):
        card_person = dbc.Card(
            dbc.CardBody([
                html.H5(name, style=H5_style, className="card-title"),
                html.P(description, style={"color": "white", "font-size": "15px", "white-space": "pre-line"})
            ])
        )
        return card_person

    def create_ryan_card(self):
        card_ryan = self.create_person_card(
            "Ryan Cassisi",
            "Hello, I'm Ryan! A tech enthusiast with a deep passion for artificial intelligence.\nOutside the world of code, I'm a sports fan, particularly devoted to soccer. Huge fan of PSG !"
        )
        return card_ryan

    def create_hafsa_card(self):
        card_hafsa = self.create_person_card(
            "Hafsa Boughemza",
            "Hello, it's Hafsa! I am passionate about computer science and artificial intelligence.\nBeside coding, I'm all about fitness !"
        )
        return card_hafsa

    def create_histogram_card(self):
        histogram_tabs = [
            {'label': 'Grouped', 'value': 'tab_grouped', 'style': self.tab_style, 'selected_style': self.tab_selected_style},
            {'label': 'Separated', 'value': 'tab_separated', 'style': self.tab_style, 'selected_style': self.tab_selected_style}
        ]
        histogram_description = html.P([
            "Select a time above to see its distribution.",
            html.Br(),
            html.Br(),
            "This visualization offers a comprehensive view of the distribution of the different time-related variables, allowing the identification of patterns and outliers.",
            html.Br(),
            html.Br(),
            "-Grouped : Displays the selected categories together.",
            html.Br(),
            "-Separated : Displays each category individually. Double-click on a category on the right to isolate it."
        ])
        radioItems_time = [
            dbc.Row([
                dbc.Col([html.H5("Time : ", style=H5_style)], width=2),
                dbc.Col([dcc.RadioItems(
                        id='radioItems_time', 
                        options=[
                            {'label': 'Intake', 'value': 'intaketime'},
                            {'label': 'Dispatch', 'value': 'dispatchtime'},
                            {'label': 'Travel', 'value': 'traveltime'},
                            {'label': 'On scene', 'value': 'timeonscene'},
                            {'label': 'Total', 'value': 'totaltime'},
                        ],
                        value='traveltime',
                        inline=True,
                        inputStyle={"margin-left": "15px", "margin-right": "4px"}
                )], width=10)
            ])
        ]
        card_histogram = self.create_tabbed_card('Histogram of times', histogram_tabs, 'histogram', histogram_description, radioItems_time)
        return card_histogram

    def create_linechartcount_card(self):
        linechart_tabs = [
            {'label': 'Grouped', 'value': 'tab_grouped', 'style': self.tab_style, 'selected_style': self.tab_selected_style},
            {'label': 'Separated', 'value': 'tab_separated', 'style': self.tab_style, 'selected_style': self.tab_selected_style}
        ]
        linechartcount_description = html.P([
            "Select the scale for a daily or monthly view.",
            html.Br(),
            html.Br(),
            "This graph illustrates the temporal trends in 911 emergency calls, providing a dynamic overview of call volume over time. This visualization allows for the identification of patterns, peaks, or dips in call activity, aiding in the analysis of temporal variations in emergency response demands.",
            html.Br(),
            html.Br(),
            "-Grouped : Displays the selected categories together.",
            html.Br(),
            "-Separated : Displays each category individually. Double-click on a category on the right to isolate it."
        ])

        radioItems_scale = [
            dbc.Row([
                dbc.Col([html.H5("Scale : ", style=H5_style)], width=2),
                dbc.Col([dcc.RadioItems(
                        id='radioItems_scale', 
                        options=[
                            {'label': 'Daily', 'value': 'Daily'},
                            {'label': 'Monthly', 'value': 'Monthly'}
                        ],
                        value='Monthly',
                        inline=True,
                        inputStyle={"margin-left": "18px", "margin-right": "5px"}
                )], width=10)
            ])
        ]
        card_linechartcount = self.create_tabbed_card('Line chart of the number of calls', linechart_tabs, 'linechartCount', linechartcount_description, radioItems_scale)
        return card_linechartcount

    def create_map_card(self):
        map_tabs = [
            {'label': 'Choropleth', 'value': 'tab_choropleth', 'style': self.tab_style, 'selected_style': self.tab_selected_style},
            {'label': 'Markers', 'value': 'tab_markers', 'style': self.tab_style, 'selected_style': self.tab_selected_style}
        ]
        map_description = html.P([
            "Choropleth Map: Illustrates the distribution of the emergencies in Detroit across different zip codes, giving a quick overview of incident concentrations in various city areas.",
            html.Br(),
            "Markers Map: Pinpoints the exact locations of 911 police responses in Detroit, offering a detailed, point-by-point view for a closer examination of specific neighborhoods or regions within the city.",
            html.Br(),
            "The loading of the Markers Map may take time, especially when the number of calls is substantial."
        ])

        card_map = self.create_tabbed_card('Detroit Map', map_tabs, 'map', map_description)
        return card_map
    
    def create_dispositions_card(self):
        disposition_tabs = [
            {'label': 'Bar chart', 'value': 'tab_barchart', 'style': self.tab_style, 'selected_style': self.tab_selected_style},
            {'label': 'Line chart', 'value': 'tab_linechart', 'style': self.tab_style, 'selected_style': self.tab_selected_style}
        ]
        disposition_description = html.P([
            "This card shows the outcomes of the selected emergencies offering insights into how different incidents are resolved by authorities.",
            html.Br(),
            html.Br(),
            "-Bar Chart : Counts the different dispositions taken.",
            html.Br(),
            "-Line Chart : Displays the evolution for each disposition over time. Double-click on a disposition on the right to isolate it.",
            html.Br(),
            "Select the scale for a daily or monthly view"
        ])
        radioItems_scale_disposition = [
            dbc.Row([
                    dbc.Col([html.H5("Scale : ", style=H5_style)], width=2),
                    dbc.Col([dcc.RadioItems(
                            id='radioItems_scale_disposition', 
                            options=[
                                {'label': 'Daily', 'value': 'Daily'},
                                {'label': 'Monthly', 'value': 'Monthly'}
                            ],
                            value='Monthly',
                            inline=True,
                            inputStyle={"margin-left": "18px", "margin-right": "5px"}
                    )], width=10)
                ])
        ]
        card_disposition = self.create_tabbed_card('Dispositions', disposition_tabs, 'disposition', disposition_description, radioItems_scale_disposition)
        return card_disposition

    def create_averagetimes_card(self):
        average_times_tabs = [
            {'label': 'Text', 'value': 'tab_text', 'style': self.tab_style, 'selected_style': self.tab_selected_style},
            {'label': 'Pie chart', 'value': 'tab_piechart', 'style': self.tab_style, 'selected_style': self.tab_selected_style}
        ]
        averagetimes_description = html.P([
            "Provides a comprehensive view of average response times for 911 police emergency incidents in Detroit",
            html.Br(),
            "-Text : Displays the average times of all the times variables. ",
            html.Br(),
            "-Pie Chart : Visually summarizes the combined response times, offering insights into the overall efficiency of emergency services."
        ])
        card_averageTimes = self.create_tabbed_card('Average times', average_times_tabs, 'time', averagetimes_description)
        return card_averageTimes
    
    def create_bestunits_card(self):
        bestunits_description = html.P("This card showcases the most efficient units, offering valuable insights into the agencies contributing to swift emergency responses in the city.")

        card_bestunits = dbc.Card([
            dbc.CardBody([
                html.H3('Best units : Top 3', style=H3_style, className='mb-3'),
                html.Br(),
                html.Div(id='bestunits')
            ]),
            dbc.CardFooter(bestunits_description)
        ])
        return card_bestunits
    
    def create_callscount_card(self):
        callscount_description = html.P("Tallies the total number of 911 emergency calls within the user-selected categories and time period, providing an essential overview of call frequency. This card enables users to track and analyze the volume of incidents in specific categories, aiding in the identification of patterns or trends in emergency service demand.")

        card_calls_number = dbc.Card([
            dbc.CardBody([
                html.H3('Number of calls', style=H3_style, className='mb-3'),
                html.H2(id='calls_number', style=H2_style, className='text-center mt-3')
            ]),
            dbc.CardFooter(callscount_description)
        ])
        return card_calls_number