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
    url = 'http://localhost:8502/v1.5/payattable/check'
    response = requests.post(url, headers=headers, json={'requestId': 'string', 'gatewayId': 'freedompay', 'industryType': 'foodAndBeverage', 'configuration': [{'key': 'string', 'value': 'string'}], 'tags': [{'key': 'string', 'value': 'string'}], 'storedCredential': {'transactionType': 'recurringInitial', 'numberOfInstalments': 1, 'instalmentNumber': 1, 'complianceDatavalue': 'string'}, 'checkData': {'checkNumber': 'CHK-1001', 'checkOpenDate': '2024-06-01T12:00:00Z', 'locationId': 'string', 'registerId': '1', 'clerkId': '2', 'clerkCardNumber': 'string', 'tableNumber': 'string', 'totalAmount': 1, 'taxAmount': 1, 'unpaidAmount': 1, 'tipBasisAmount': 1, 'accessFilters': {'clerks': [{'clerkId': '2', 'clerkCardNumber': 'string'}]}}, 'messageData': {'messageLine1': 'string', 'messageLine2': 'string'}, 'receiptData': {'headerText': ['string'], 'checkItemsData': [{'amount': 100.0, 'description': 'string', 'quantity': 1}]}, 'cultureName': 'string', 'currencyCode': 'USD'})
    assert response.status_code == 200
