import requests
import pytest

@pytest.fixture
def base_url():
    return 'http://localhost:8502'

@pytest.fixture
def headers():
    return {
        'Authorization': 'PMAK-6852cde6134d13000180adc0-0a0c477664d3aa340e51077f563a400e82e',
        'Content-Type': 'application/json'
    }


def test_endpoint(base_url, headers):
    url = 'http://localhost:8502/v1.5/operation/eodbatchprocess'
    response = requests.post(url, headers=headers, json={'requestId': 'string', 'gatewayId': 'freedompay', 'industryType': 'foodAndBeverage', 'configuration': [{'key': 'string', 'value': 'string'}], 'tags': [{'key': 'string', 'value': 'string'}], 'storedCredential': {'transactionType': 'recurringInitial', 'numberOfInstalments': 1, 'instalmentNumber': 1, 'complianceDatavalue': 'string'}})
    assert response.status_code == 200
