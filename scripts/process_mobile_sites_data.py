import os

import pandas as pd
import pyproj
import requests


def read_file(filepath):
    data = pd.read_csv(filepath, sep=";")
    return data


def write_file(filepath, dataframe):
    dataframe.to_csv(filepath, sep=';', index=False)


def transform_coordinates(x_plus_y):
    lambert = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 '
                          '+towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
    wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    x, y = x_plus_y.split(',')
    longitude, latitude = pyproj.transform(lambert, wgs84, x, y)
    return longitude, latitude


def get_provider_name(provider):
    correspondance_table = {
        '20801': 'orange',
        '20810': 'SFR',
        '20815': 'free',
        '20820': 'bouygues',
    }
    provider_name = correspondance_table[provider]
    return provider_name


def get_postcode_for_provider_antenna(row):
    url = 'https://api-adresse.data.gouv.fr/reverse/?lon={}&lat={}'.format(row['longitude'], row['latitude'])
    request = requests.get(url, verify=False)
    print(row.name, request.status_code)
    if 200 <= request.status_code < 300:
        response = request.json()
        try:
            postcode = response['features'][0]['properties']['postcode']
        except (IndexError, Exception):
            postcode = None
        return postcode
    else:
        raise Exception('Query did not execute correctly.')


if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_to_transform = os.path.join(current_directory, '..', 'src', 'database', 'assets', 'mobile_sites.csv')

    mobile_sites_data = read_file(file_to_transform)

    mobile_sites_data['x_plus_y'] = mobile_sites_data['X'].map(str) + ',' + mobile_sites_data['Y'].map(str)

    mobile_sites_data['longitude'], mobile_sites_data['latitude'] = zip(*
        mobile_sites_data['x_plus_y'].map(transform_coordinates)
    )

    mobile_sites_data['provider'] = mobile_sites_data['Operateur'].apply(lambda x: get_provider_name(str(x)))

    mobile_sites_data['postcode'] = mobile_sites_data.apply(get_postcode_for_provider_antenna, axis=1)

    mobile_sites_data = mobile_sites_data[['Operateur', 'provider', 'postcode', 'X', 'Y', 'longitude', 'latitude', '2G', '3G', '4G']]

    write_file(file_to_transform, mobile_sites_data)
