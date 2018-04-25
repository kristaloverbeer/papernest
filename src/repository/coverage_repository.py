class CoverageRepository:
    def __init__(self, geolocalisation_service, mobile_sites_schema):
        self.geolocalisation_service = geolocalisation_service
        self.mobile_sites_schema = mobile_sites_schema

    def get_coverage_information(self, queried_address):
        queried_address_information = self.geolocalisation_service.get_address_information(queried_address)
        if 'message' in queried_address_information:
            return queried_address_information, 400

        address_postcode = queried_address_information['features'][0]['properties']['postcode']
        providers_data_per_postcode = self.mobile_sites_schema.serialize(address_postcode)[address_postcode]

        return providers_data_per_postcode, 200
