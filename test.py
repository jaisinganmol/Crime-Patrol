def extract_city(add):
    if add is not None:
        x = add.split(",")[-6:-4]
        return x[0].strip()+", "+x[1].strip()
    else:
        return add

def extract_zip(add):
    if add is not None:
        x = add.split(",")[-2]
        if len(x) >= 5:
            x = x.strip()[:5]
            if x.isdigit():
                return str(x)
        else:
            return None
    else:
        return add

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="BDA")

adds = ["20900, Frederick Road, Germantown, Montgomery County, Maryland, 20876, USA", "Tremont Street, Roxbury Crossing, Roxbury, Boston, Suffolk County, Massachusetts, 02120, USA",
        "Saint Gabriels School, Fidelis Way, Aberdeen, Brighton, Boston, Suffolk County, Massachusetts, 02135-3202, USA", "12918, Twinbrook Parkway, Spring Lake Park, North Bethesda, Montgomery County, Maryland, USA"]

import math
def geocode_reverse(lat, lng):
    if math.isnan(lat) or math.isnan(lng):
        return None
    else:
        return geolocator.reverse(f"{lat}, {lng}").address

print(geocode_reverse(39.154082098,-77.273558303))