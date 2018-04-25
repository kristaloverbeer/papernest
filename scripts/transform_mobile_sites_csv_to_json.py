import csv
import json
import os


def transform(csv_input):
    result = {}
    with open(csv_input, 'r') as csv_file_stream:
        reader = csv.DictReader(csv_file_stream, delimiter=';')

        for row in reader:
            postcode, provider = row['postcode'], row['provider']
            result_to_store = {
                    '2G': bool(int(row['2G'])),
                    '3G': bool(int(row['3G'])),
                    '4G': bool(int(row['4G'])),
            }
            if postcode not in result:
                result[postcode] = {provider: result_to_store}
            else:
                if provider not in result[postcode]:
                    result[postcode][provider] = result_to_store
                else:
                    result_to_update = result[postcode][provider]
                    result_to_update['2G'] = result_to_update['2G'] or result_to_store['2G']
                    result_to_update['3G'] = result_to_update['3G'] or result_to_store['3G']
                    result_to_update['4G'] = result_to_update['4G'] or result_to_store['4G']
    return result


def write_json(json_data, output_filepath):
    with open(output_filepath, 'w') as json_file_stream:
        json.dump(json_data, json_file_stream)


if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.realpath(__file__))
    csv_file_input = os.path.join(current_directory, '..', 'src', 'database', 'assets', 'mobile_sites.csv')
    json_file_output = os.path.join(current_directory, '..', 'src', 'database', 'assets', 'mobile_sites.json')

    transformed_data = transform(csv_file_input)

    write_json(transformed_data, json_file_output)
