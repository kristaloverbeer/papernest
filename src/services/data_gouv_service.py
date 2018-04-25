import json

import requests
from requests.exceptions import HTTPError, ConnectTimeout, ReadTimeout

from src.logging.mixin import LoggingMixin


class DataGouvService(LoggingMixin):
    def __init__(self, base_url='https://api-adresse.data.gouv.fr', limit=1):
        self.base_url = base_url
        self.limit = limit

    def get_address_information(self, queried_address):
        url_to_query = '{}/search/?q={}&limit={}'.format(self.base_url, queried_address, self.limit)
        result = {}
        try:
            request = requests.get(url_to_query)
            request.raise_for_status()
            result = request.json()
        except json.decoder.JSONDecodeError as error:
            self.logger.exception(error.msg)
        except (HTTPError, ConnectTimeout, ReadTimeout) as error:
            self.logger.exception(str(error))
        if result:
            if result['features']:
                result_score = result['features'][0]['properties']['score']
                # TODO: this number was determined empirically, this should be handled in a better way thanks to a
                # web interface for instance with different propositions for the queried address
                if result_score <= 0.50:
                    return {'message': 'Address might not be the one you wanted. '
                                       'Are you sure you queried a complete address with a postal code ?'}

            else:
                return {'message': 'The queried address did not match any results, check if the address you entered'
                                   ' does not contains any typos.'}
            return result
        else:
            raise Exception('The request {} was not completed successfully'.format(url_to_query))
