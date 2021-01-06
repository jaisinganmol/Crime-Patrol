import pandas as pd

"""Preprocess.py: This file is used to do preprocessing of the data."""

__author__      = "Shubham Patil, Priyanka Dwivedi, Anmol Jaising"


class PreProcess:

    def __init__(self):
        pass
    def preprocess(self):
        """
         This function preprocess the data by merging two dataset
         Joins the zipcode and city based on lat, long
        :return:
        """

        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('max_colwidth', -1)

        date_parser_mass = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

        def date_parser_mary(x):
            if isinstance(x, str):
                return pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S %p')
            else:
                return pd.NaT

        # Read CSV files for both states
        mass_raw = pd.read_csv("Massachusetts.csv", parse_dates=['OCCURRED_ON_DATE'], date_parser=date_parser_mass,
                               low_memory=False, float_precision='round_trip')
        mary_raw = pd.read_csv("Maryland.csv", parse_dates=['Start_Date_Time'], date_parser=date_parser_mary,
                               low_memory=False, float_precision='round_trip')

        # Initialize data frame for new updated csv file
        mass_final = pd.DataFrame()
        mary_final = pd.DataFrame()

        # get the values from raw dataset and process necessary to make sure final dataset is consistent
        mass_final['IncidentNumber'] = mass_raw['INCIDENT_NUMBER'].apply(lambda x: x[1:10])
        mary_final['IncidentNumber'] = mary_raw['Incident ID']

        mass_final['OffenseCode'] = mass_raw['OFFENSE_CODE']
        mary_final['OffenseCode'] = mary_raw['Offence Code']

        mass_final['OffenseDescription'] = mass_raw['OFFENSE_DESCRIPTION']
        mary_final['OffenseDescription'] = mary_raw['Crime Name3']

        mass_final['OffenseCodeGroup'] = mass_raw['OFFENSE_CODE_GROUP']
        mary_final['OffenseCodeGroup'] = mary_raw['Crime Name2']

        mass_final['StreetName'] = mass_raw['STREET']
        mary_final['StreetName'] = mary_raw['Street Name']

        mass_datetime = mass_raw['OCCURRED_ON_DATE']
        mary_datetime = mary_raw['Start_Date_Time']
        mass_final['OccurredOnDate'] = mass_datetime.dt.date
        mary_final['OccurredOnDate'] = mary_datetime.dt.date
        mass_final['OccurredOnTime'] = mass_datetime.dt.time
        mary_final['OccurredOnTime'] = mary_datetime.dt.time

        mass_final['PoliceDistrictName'] = mass_raw['DISTRICT']
        mary_final['PoliceDistrictName'] = mary_raw['Police District Number']

        mass_final[['Lat', 'Long']] = mass_raw[['Lat', 'Long']]
        mary_final[['Lat', 'Long']] = mary_raw[['Latitude', 'Longitude']]

        # since we have two datset, we merge them into one
        df = pd.concat([mass_final, mary_final], axis=0)
        df.to_csv("final_dataset.csv", index=False, float_format="%.2f")

        # read the zipcode and city mapping dataset to convert decimal places of dataset by 2 places
        zip_city_data = pd.read_csv("zip_data.csv", low_memory=False, float_precision='round_trip')
        zip_city_data_final = pd.DataFrame()

        zip_city_data_final['ZipCode'] = zip_city_data['ZipCode']

        zip_city_data_final['City'] = zip_city_data['City']

        zip_city_data_final['Latitude'] = zip_city_data['Latitude']

        zip_city_data_final['Longitude'] = zip_city_data['Longitude']
        # convert it to csv
        zip_city_data_final.to_csv("uszip_updated.csv", index=False, float_format="%.2f")

        # join zipcode and city mapping with latitude and longtitude using crime dataset generated and zipcode dataset
        zip_city_data = pd.read_csv("uszip_updated.csv", low_memory=False, float_precision='round_trip')
        final_raw = pd.read_csv("Crime.csv", low_memory=False, float_precision='round_trip')
        common = pd.merge(final_raw, zip_city_data, how='left', left_on=['Lat', 'Long'],
                          right_on=['Latitude', 'Longitude']).dropna()
        common.to_csv("final_dataset1.csv", index=False, float_format="%.2f")

        # Remove latitude and longtiude to get the finished final dataset
        final_dataset_raw = pd.read_csv("final_dataset1.csv", low_memory=False, float_precision='round_trip')
        final_dataset = pd.DataFrame()

        final_dataset['IncidentNumber'] = final_dataset_raw['IncidentNumber']
        final_dataset['OffenseCode'] = final_dataset_raw['OffenseCode']
        final_dataset['OffenseDescription'] = final_dataset_raw['OffenseDescription']
        final_dataset['OffenseCodeGroup'] = final_dataset_raw['OffenseCodeGroup']
        final_dataset['StreetName'] = final_dataset_raw['StreetName']
        final_dataset['OccurredOnDate'] = final_dataset_raw['OccurredOnDate']
        final_dataset['OccurredOnTime'] = final_dataset_raw['OccurredOnTime']
        final_dataset['PoliceDistrictName'] = final_dataset_raw['PoliceDistrictName']
        final_dataset['ZipCode'] = (final_dataset_raw['ZipCode']) // 1
        final_dataset['City'] = final_dataset_raw['City']

        #convert the final dataset into csv
        final_dataset.to_csv("Crime.csv", index=False, float_format="%.2f")

if __name__ == '__main__':
    p = PreProcess()
    p.preprocess()





