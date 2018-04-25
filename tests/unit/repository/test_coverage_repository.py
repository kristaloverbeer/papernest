import pytest

from src.database.schema.mobile_sites_schema import MobileSitesSchema
from src.repository.coverage_repository import CoverageRepository
from src.services.data_gouv_service import DataGouvService


@pytest.mark.parametrize('test_queried_address,expected_metadata', [
    ('42 rue papernest, 75011 Paris', ({'SFR': {'2G': True, '3G': True, '4G': True},
                                        'bouygues': {'2G': True, '3G': True, '4G': True},
                                        'free': {'2G': False, '3G': True, '4G': True},
                                        'orange': {'2G': True, '3G': True, '4G': True}}, 200)
     ),
    ('10 boulevard richard wallace, 92800 Puteaux', ({'SFR': {'2G': True, '3G': True, '4G': True},
                                                      'bouygues': {'2G': True, '3G': True, '4G': True},
                                                      'free': {'2G': False, '3G': True, '4G': True},
                                                      'orange': {'2G': True, '3G': True, '4G': True}}, 200)
     ),
    ('66 satan street, 666 Hell', ({'message': 'The queried address did not match any results, check if the '
                                               'address you entered does not contains any typos.'}, 400)
     ),
    ('84 rue blahblah, 75011 Paris', ({'message': 'Address might not be the one you wanted. Are you sure you '
                                                  'queried a complete address with a postal code ?'}, 400)
     ),
])
def test_should_return_correctly_formatted_coverage_information_given_queried_address(
        test_queried_address,
        expected_metadata,
):
    # Given
    geolocalisation_service = DataGouvService()
    mobile_sites_schema = MobileSitesSchema()
    coverage_repository = CoverageRepository(geolocalisation_service, mobile_sites_schema)
    # When
    result = coverage_repository.get_coverage_information(test_queried_address)
    # Then
    assert result == expected_metadata
