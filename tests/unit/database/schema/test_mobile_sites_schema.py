import pytest

from src.database.schema.mobile_sites_schema import MobileSitesSchema


@pytest.mark.parametrize('postcode,expected_postcode_data', [
    (12, {}),
    (28120, {'28120': {'SFR': {'2G': True, '3G': True, '4G': True},
                       'bouygues': {'2G': True, '3G': True, '4G': True},
                       'free': {'2G': False, '3G': True, '4G': True},
                       'orange': {'2G': True, '3G': True, '4G': True}}}
     ),
    (25410, {'25410': {'SFR': {'2G': True, '3G': True, '4G': True},
                       'bouygues': {'2G': True, '3G': True, '4G': True},
                       'free': {'2G': False, '3G': True, '4G': True}}}),
    (75001, {'75001': {'SFR': {'2G': True, '3G': True, '4G': True},
                       'bouygues': {'2G': True, '3G': True, '4G': True},
                       'free': {'2G': False, '3G': True, '4G': True},
                       'orange': {'2G': True, '3G': True, '4G': True}}}
     ),
    (92800, {'92800': {'SFR': {'2G': True, '3G': True, '4G': True},
                       'bouygues': {'2G': True, '3G': True, '4G': True},
                       'free': {'2G': False, '3G': True, '4G': True},
                       'orange': {'2G': True, '3G': True, '4G': True}}})
])
def test_should_return_data_specific_to_given_postcode(postcode, expected_postcode_data):
    # Given
    mobile_sites_schema = MobileSitesSchema()
    # When
    serialized_result = mobile_sites_schema.serialize(postcode)
    # Then
    assert serialized_result == expected_postcode_data
