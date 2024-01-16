import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

class DataCleaningProcessing:
    def __init__(self, data_file_path, geojson_file_path):
        self.data = pd.read_csv(data_file_path)
        self.zipcode_gdf = gpd.read_file(geojson_file_path)

    def clean_data(self):
        # Supression des doublons
        self.data = self.data.drop_duplicates(subset='callno')
        
        # Valeurs absolues des variables de temps
        time_columns = ['intaketime', 'dispatchtime', 'traveltime', 'totresponsetime', 'timeonscene', 'totaltime']
        self.data[time_columns] = self.data[time_columns].abs()

        # Conversion calldate et calltime en datetime
        self.data['calldate'] = pd.to_datetime(self.data['calldate'], format='%Y-%m-%d')
        self.data['calltime'] = pd.to_datetime(self.data['calltime'], format='%H:%M:%S').dt.time

        # Trie des données par la date et l'heure (ordre chronologique)
        self.data = self.data.sort_values(by=['calldate', 'calltime']).reset_index(drop=True)

        # Extraction latitude et longitude de la variable location
        self.data['latitude'] = self.data['location'].apply(self.extract_latitude)
        self.data['longitude'] = self.data['location'].apply(self.extract_longitude)
        self.data = self.data.drop(columns='location')

        # Mapping des categories en catégories plus large
        category_mapping = {
            'DISORDERLY PERSON': 'Disturbance',
            'INVESTIGATE PERSON': 'Investigation',
            'ACCIDENT': 'Accident',
            'PRANK/OTHER': 'Prank',
            'ASSAULT': 'Assault',
            'FAMILY TROUBLE': 'Domestic',
            'TRAFFIC': 'Traffic',
            'AUTO THEFT': 'Theft',
            'MEDICAL': 'Medical',
            'ALARM': 'Alarm',
            'BURGLARY': 'Burglary',
            'ROBBERY': 'Robbery',
            'SA': 'Sexual Assault',
            'RAPE': 'Sexual Assault',
            'FIRE': 'Fire',
            'DRUGS': 'Drug Related',
            'AR': 'Arson',
            'LARCENY': 'Theft',
            'OTHER': 'Other',
            'TS': 'Traffic',
            'TI': 'Traffic',
            'SI': 'Investigation',
            'T': 'Traffic',
            '93': 'Other',
            'W8': 'Other',
            '31': 'Other',
            'ANIMAL': 'Animal',
            'W3': 'Other',
            'SPECIAL DETAIL': 'Special Detail',
            '90': 'Other',
            'TO': 'Traffic',
            'SS': 'Special Service',
            'RA': 'Restricted Area',
            'W5': 'Other',
            '99': 'Other'
        }       

        self.data['category'] = self.data['category'].map(category_mapping)

        # Mapping des dispositions en dispositions plus large
        disposition_mapping = {
            # No Action Required
            'NO PROBLEM FOUND': 'No problem found',
            'HANDLED BY OTHER': 'Handled by Other Agency',
            'FALSE ALARM - BUSINESS': 'False Alarm',
            'FALSE ALARM - RESIDENCE': 'False Alarm',
            'FALSE ALARM - OTHER': 'False Alarm',
            'NCF': 'No Charges Filed',
            'NSA': 'No Such Address',
            'ADV': 'Advised',
            'CAN': 'Call Cancelled',
            'CANCELLED BY CALLER': 'Call Cancelled',
            'CANCELLED BY DISPATCH': 'Call Cancelled',
            'DUP': 'Duplicate Call',
            'UNF': 'Unfounded',

            # Investigation and Enforcement
            'INV - FURTHER ACTION TAKEN': 'Investigation - Further Action taken',
            'INV - NO FURTHER ACTION': 'Investigation - No Further Action',
            'REPORT': 'Report Taken',
            'ARREST': 'Arrest Made',
            'INV SUSP AND RELEASED': 'Investigation - Suspect Released',
            'RECOV STOLEN AUTO': 'Stolen Auto Recovered',
            'DETAIL COMPLETED': 'Detail Completed',
            'WARNING GIVEN': 'Warning Issued',
            'TICKET ISSUED': 'Ticket Issued',
            'NAR': 'Narcotics Arrest',
            'RCR': 'Property Recovered',
            'PCP': 'Peace Officer Complaint',

            # Assistance and services
            'ASSIST': 'Assistance and Services',
            'TRANSPORT': 'Assistance and Services',
            'AC1': 'Assistance and Services',
            'AC2': 'Assistance and Services',
            'DPS': 'Assistance and Services',
            'RPP': 'Assistance and Services',

            # Unknown
            'MSG': 'Unknown or Miscellaneous',
            'UNK': 'Unknown or Miscellaneous',
            'IMP': 'Unknown or Miscellaneous',
            'HTX': 'Unknown or Miscellaneous',
            'AGO': 'Unknown or Miscellaneous',
            'VRM': 'Unknown or Miscellaneous',
            'UTC': 'Unknown or Miscellaneous',
            'AGB': 'Unknown or Miscellaneous',
            'RAC': 'Unknown or Miscellaneous',
            'AGR': 'Unknown or Miscellaneous',
            'PK13': 'Unknown or Miscellaneous',
            'PKR1': 'Unknown or Miscellaneous',
            'PKR3': 'Unknown or Miscellaneous',
            'PKR4': 'Unknown or Miscellaneous',
            'PKNC': 'Unknown or Miscellaneous',
            'AFI': 'Unknown or Miscellaneous'
        }

        self.data['disposition'] = self.data['disposition'].map(disposition_mapping)

        # Extraction du jour de la semaine
        self.data['day_of_week'] = self.data['calldate'].dt.day_name()
        self.data['calldate'] = self.data['calldate'].dt.date

        # Ajout d'une variable time_of_day
        self.data['time_of_day'] = self.data['calltime'].apply(self.time_into_category)

    def add_zipcode_column(self):
        geometry = [Point(xy) for xy in zip(self.data.longitude, self.data.latitude)]
        calls_gdf = gpd.GeoDataFrame(self.data, geometry=geometry)
        calls_gdf.crs = 'EPSG:4326'
        result = gpd.sjoin(calls_gdf, self.zipcode_gdf, how="inner", predicate="within")
        zip_codes = result['zipcode']
        self.data['zipcode'] = zip_codes

    @staticmethod
    def extract_latitude(location):
        index = location.find('(')
        coords = location[index+1:-1]
        latitude = float(coords.split(',')[0])
        return latitude

    @staticmethod
    def extract_longitude(location):
        index = location.find('(')
        coords = location[index+1:-1]
        longitude = float(coords.split(',')[1])
        return longitude

    @staticmethod
    def time_into_category(timestamp):
        if 5 <= timestamp.hour < 12:
            return 'Morning'
        elif 12 <= timestamp.hour < 18:
            return 'Afternoon'
        elif 18 <= timestamp.hour < 22:
            return 'Evening'
        else:
            return 'Night'


data_processor = DataCleaningProcessing("datasets/dpd_911_calls_for_service.csv", "datasets/City_of_Detroit_Zip_Codes.geojson")
data_processor.clean_data()
data_processor.add_zipcode_column()