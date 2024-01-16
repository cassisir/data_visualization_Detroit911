import dash_bootstrap_components as dbc
import datetime

def create_button(text, id):
    return dbc.Button(
        text,
        id=id,
        className="mb-3",
        color="primary",
        n_clicks=0,
        style={"background-color": "white", "color": "black", "font-size": "18px", "fontWeight": "bold"}
)

def create_collapse(content, id, is_open):
    return dbc.Collapse(
        content,
        id=id,
        is_open=is_open
)

def convert_minutes_to_minutes_seconds(minutes):
    total_seconds = int(minutes*60)
    minutes_part = total_seconds//60
    seconds_part = total_seconds%60
    return f"{minutes_part}min {seconds_part}sec"

def filter_data(selected_categories, start_date, end_date, selected_periods, selected_days, data):
    # Conversion des dates (str) en datetime.datetime
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    # Sélectionne toutes les catégories si aucune n'est sélectionnée
    if selected_categories==None or not selected_categories:
        selected_categories = sorted(data.category.unique())

    # Sélectionne toutes les périodes si aucune n'est sélectionnée
    if selected_periods==None or not selected_periods:
        selected_periods = ['Morning', 'Afternoon', 'Evening', 'Night']

    # Sélectionne tous les jours si aucun n'est sélectionné
    if selected_days==None or not selected_days:
        selected_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Vérifie que selected_categories soit une list
    if not isinstance(selected_categories, list):
        selected_categories = [selected_categories]
    # Vérifie que selected_periods soit une list
    if not isinstance(selected_periods, list):
        selected_periods = [selected_periods]
    # Vérifie que selected_days soit une list
    if not isinstance(selected_periods, list):
        selected_periods = [selected_periods]

    ## FILTRAGE ##
    df = data[(data['calldate'] >= start_date) & (data['calldate'] <= end_date)]
    df = df[df.category.isin(selected_categories)]
    df = df[df.time_of_day.isin(selected_periods)]
    df = df[df.day_of_week.isin(selected_days)]
    return df

H1_style = {"font-size": "35px"}
H2_style = {"font-size": "30px"}
H3_style = {"font-size": "25px"}
H4_style = {"font-size": "20px"}
H5_style = {"font-size": "15px"}
H6_style = {"font-size": "12px"}