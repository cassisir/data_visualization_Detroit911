import sys
import os
current_script_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_script_directory)
sys.path.append(parent_directory)
from data_processing import data_processor
from card_creator import CardCreator
from dash import Dash, html, Output, Input, State, dash_table, callback
import dash
import dash_bootstrap_components as dbc
from dashboard_utils import create_button, create_collapse, H2_style, H3_style, H5_style


dash.register_page(__name__, path='/', name='Presentation')

data = data_processor.data

card_creator = CardCreator()
card_hafsa = card_creator.create_hafsa_card()
card_ryan = card_creator.create_ryan_card()

style_list={"color": "white", "font-size": "15px"}
variable_descriptions = html.Ul([
            html.Li("callno: Call number in the records management system.", style=style_list, className='mb-2'),
            html.Li("agency: The responding agency, which could be DPD (Detroit Police Department), WSUPD (Wayne State University Police Department), HIGHLAND PARK, DET PUB SCHOOLS, etc.", style=style_list, className='mb-2'),
            html.Li("incident_address: The location of the incident.", style=style_list, className='mb-2'),
            html.Li("callcode: Numeric code or type of the call.", style=style_list, className='mb-2'),
            html.Li("calldescription: Description of the emergency or call type.", style=style_list, className='mb-2'),
            html.Li("category: The category of the call, such as Family Trouble, Assault, Robbery, and more.", style=style_list, className='mb-2'),
            html.Li("calldate: The date of the incident.", style=style_list, className='mb-2'),
            html.Li("calltime: The time of the incident.", style=style_list, className='mb-2'),
            html.Li("disposition: The disposition of the call, indicating outcomes like arrest, report taken, etc.", style=style_list, className='mb-2'),
            html.Li("precinctSCA: DPD Precinct and Scout Car Area, providing geographic information.", style=style_list, className='mb-2'),
            html.Li("respondingunit: Car code of the responding unit.", style=style_list, className='mb-2'),
            html.Li("officerinitiated: A binary field (yes/no) indicating whether the call was officer-initiated or on-view.", style=style_list, className='mb-2'),
            html.Li("intaketime: The time in minutes for call intake, from handoff to dispatcher.", style=style_list, className='mb-2'),
            html.Li("dispatchtime: The time in minutes elapsed until the first unit is dispatched.", style=style_list, className='mb-2'),
            html.Li("traveltime: The time in minutes elapsed from dispatch to the unit arriving on the scene.", style=style_list, className='mb-2'),
            html.Li("totresponsetime: The total time elapsed from the call's dispatch time to its closure time.", style=style_list, className='mb-2'),
            html.Li("timeonscene: The time in minutes elapsed from the unit arriving on the scene to the call's closure time.", style=style_list, className='mb-2'),
            html.Li("totaltime: The total time elapsed from the call's creation time to its closure time.", style=style_list, className='mb-2'),
            html.Li("latitude: The geographical coordinate representing the north-south position of the incident location.", style=style_list, className='mb-2'),
            html.Li("longitude: The geographical coordinate representing the east-west position of the incident location.", style=style_list, className='mb-2'),
            html.Li("day_of_week: The day of the week on which the incident occurred (e.g., Monday, Tuesday, etc.).", style=style_list, className='mb-2'),
            html.Li("time_of_day: The general time of day when the incident occurred, categorized as morning, afternoon, evening, or night.", style=style_list, className='mb-2'),
            html.Li("zipcode: The postal code associated with the incident location.", style=style_list, className='mb-2'),
])


layout = dbc.Container([
    
    # Presentation of the Dataset
    dbc.Row([
        dbc.Col([
            html.H2("Presentation of the Dataset", style=H2_style, className='text-center'),
            html.Br(),
            html.Div([
                html.H3("Dataset Description :", style=H3_style),
                html.H5("This dataset contains comprehensive information on 911 police emergency responses and officer-initiated calls for service in the City of Detroit, starting from January 1, 2016. Emergency response calls are generated when individuals dial 911 to request police assistance, while officer-initiated calls encompass various police activities such as traffic stops, on-site investigations, and responding to ongoing criminal incidents, all initiated by police officers. The dataset encompasses details about call intake, dispatch, travel, as well as the total response and call times for incidents handled by police agencies. It also includes information about the responding agency, unit, call type, call category, and the disposition of each call.",
                        style=H5_style, className='text-justify'),
                html.H5("To ensure privacy, location data is anonymized at the block level, with the last two digits of the incident address and the longitude/latitude coordinates being offset. Time information is presented in fractional minutes (e.g., 1.5 minutes represents 1 minute and 30 seconds). The dataset is updated at 20-minute intervals.", style=H5_style),
            ]),
        ])
    ]),

    # Variables descriptions
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Div([
                html.H3("Variable Descriptions :", style=H3_style),
                create_button("Open Descriptions", "variable_description_button"),
                create_collapse(variable_descriptions, "variable_description_collapse", False)
            ])
        ])
    ]),

    # View Dataset
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H3("View Dataset :", style=H3_style),
            create_button("Open Dataset", "dataset_button"),
            create_collapse([
                html.Div([
                    html.H5(f"The dimensions are : {data.shape}", style=H5_style),
                    html.H5("Only the first 100 rows are displayed below.", style=H5_style),
                    dash_table.DataTable(
                        data=data[:100:].to_dict('records'),
                        page_size=20,
                        style_header={"background-color": "darkgrey", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"},
                        style_cell={"background-color": "lightgrey", "color": "black", "font-size": "16px", "text-align": "center"}
                    )
                ]),
            ], "dataset_collapse", False)
        ])
    ]),

    # About us
    # Group
    dbc.Row([
        dbc.Col([
            html.H3("About us", className='mt-8 mb-2 text-center', style=H3_style),
            html.H5(["We are a team of two students from the engineering school ",
                html.A("ESIEE Paris", href="https://www.esiee.fr/en", target="_blank"),
                ", specializing in \"Data Science and Artificial Intelligence.\" This project is a collaborative effort as part of our coursework on \"Data Visualization with Python,\" under the guidance of our teacher, Daniel Courivaud."],
            style=H5_style, className='text-center text-justify'),
        ], width=6, className='mx-auto mb-2')
    ]),
    # Individual
    dbc.Row([
        dbc.Col([
            create_button("Hafsa Boughemza", "left"),
            create_collapse(card_hafsa, "left-collapse", 0),
        ],width=6, className="d-flex flex-column align-items-end"),
        dbc.Col([
            create_button("Ryan Cassisi", "right"),
            create_collapse(card_ryan, "right-collapse", 0),
        ],width={'size':'auto'}, className="align-items-left"),
    ], className='mb-5'),

], fluid=True)

@callback(
    Output(component_id='dataset_collapse',component_property='is_open'),
    Input(component_id='dataset_button', component_property='n_clicks'),
    State(component_id='dataset_collapse', component_property='is_open')
)
def toggle_collapse_dataset(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output(component_id="variable_description_collapse", component_property="is_open"),
    Input(component_id="variable_description_button", component_property="n_clicks"),
    State(component_id='variable_description_collapse', component_property='is_open')
)
def toggle_collapse_variables(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("left-collapse", "is_open"),
    [Input("left", "n_clicks")],
    [State("left-collapse", "is_open")],
)
def toggle_left(n_left, is_open):
    return not is_open if n_left else is_open

@callback(
    Output("right-collapse", "is_open"),
    [Input("right", "n_clicks")],
    [State("right-collapse", "is_open")],
)
def toggle_right(n_right, is_open):
    return not is_open if n_right else is_open
