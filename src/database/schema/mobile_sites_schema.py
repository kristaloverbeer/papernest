import json
import os
from functools import lru_cache


class MobileSitesSchema:
    def __init__(self):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(current_directory, '..', 'assets', 'mobile_sites.json')

    # This function is a mimic of a serialization function from a query build by an ORM for instance, which could
    # allows us to apply different filters before actually loading the results.
    # Here I decided to simply cache the results so that we don't load the file into memory every time
    # we call this function.
    @lru_cache(maxsize=None)
    def serialize(self, postcode_filter):
        with open(self.path, 'r') as file_stream:
            json_data = json.load(file_stream)

        providers_data_per_post_code = {
            postcode: providers_coverage_information
            for postcode, providers_coverage_information in json_data.items()
            if postcode == str(postcode_filter)
        }
        return providers_data_per_post_code
