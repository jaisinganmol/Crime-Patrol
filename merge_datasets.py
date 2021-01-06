'''
Author: Shubham Patil (sbp5931@rit.edu)
'''

import math
import pandas as pd
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="BDA")

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)


date_parser_mass = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
def date_parser_mary(x):
    if isinstance(x, str):
        return pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S %p')
    else:
        return pd.NaT


mass_raw = pd.read_csv("Massachusetts.csv", parse_dates = ['OCCURRED_ON_DATE'], date_parser = date_parser_mass)
mary_raw = pd.read_csv("Maryland.csv", parse_dates = ['Start_Date_Time'], date_parser = date_parser_mary) 

# # Random 1000 samples
# mass_raw = mass_raw.sample(n=100)
# mary_raw = mary_raw.sample(n=100)

mass_final = pd.DataFrame()
mary_final = pd.DataFrame()

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
# mary_final['Address'] = mary_raw.apply(lambda x: geocode_reverse(x['Latitude'], x['Longitude']), axis=1)

# def geocode_reverse(lat, lng):
#     if math.isnan(lat) or math.isnan(lng):
#         return None
#     else:
#         return geolocator.reverse(f"{lat}, {lng}").address

# mass_final['Address'] = mass_raw.apply(lambda x: geocode_reverse(x['Lat'], x['Long']), axis=1)
# mary_final['Address'] = mary_raw.apply(lambda x: geocode_reverse(x['Latitude'], x['Longitude']), axis=1)


# def extract_zip(add):
#     if add is not None:
#         x = add.split(",")[-2]
#         if len(x) >= 5:
#             x = x.strip()[:5]
#             if x.isdigit():
#                 return str(x)
#         else:
#             return None
#     else:
#         return add

# mass_final['Zipcode'] = mass_final['Address'].apply(extract_zip)
# mary_final['Zipcode'] = mary_final['Address'].apply(extract_zip)
# mass_final['Zipcode'] = mass_final['Zipcode'].astype(str)
# mary_final['Zipcode'] = mary_final['Zipcode'].astype(str)



# def extract_city(add):
#     if add is not None:
#         x = add.split(",")
#         if len(x) >= 6:
#             x = x[-6:-4]
#             if len(x) >= 2:
#                 return x[0].strip()+", "+x[1].strip()
#         elif len(x) == 5:
#             x = x[-5:-3]
#             if len(x) >= 2:
#                 return x[0].strip()+", "+x[1].strip()            
#     else:
#         return add

# mass_final['City'] = mass_final['Address'].apply(extract_city)
# mary_final['City'] = mary_final['Address'].apply(extract_city)
df = pd.concat([mass_final,mary_final], axis=0)
df.to_csv("Crime.csv", index = False)
