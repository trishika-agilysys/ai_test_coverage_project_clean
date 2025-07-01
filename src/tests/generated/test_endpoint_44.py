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
    url = 'http://localhost:8502/v1.5/transaction/credit'
    response = requests.post(url, headers=headers, json={'requestId': 'string', 'gatewayId': 'freedompay', 'industryType': 'foodAndBeverage', 'configuration': [{'key': 'string', 'value': 'string'}], 'tags': [{'key': 'string', 'value': 'string'}], 'storedCredential': {'transactionType': 'recurringInitial', 'numberOfInstalments': 1, 'instalmentNumber': 1, 'complianceDatavalue': 'string'}, 'invoiceData': {'invoiceId': '123456789', 'invoiceDate': '2024-06-01T12:00:00Z'}, 'transactionData': {'registerId': '1', 'clerkId': '2', 'transactionDate': 'string', 'referenceCode': '123ABC', 'transactionAmount': 1, 'taxAmount': 1, 'surchargeAmount': 1, 'allowPartialTransactionAmount': True}, 'lodgingData': {'folioNumber': 'string', 'guestName': 'string', 'checkInDate': 'string', 'checkOutDate': 'string', 'expectedDuration': 1, 'chargeType': 'lodging', 'chargeCode': 'default', 'noShow': True, 'roomNumber': '101', 'dailyRoomRate': 1, 'dailyRoomTax': 1, 'extraChargesTotalAmount': 1, 'extraChargesTypes': ['restaurant']}, 'billingAddress': {'firstName': 'string', 'middleName': 'string', 'lastName': 'string', 'addressLine1': 'string', 'addressLine2': 'string', 'city': 'string', 'state': 'string', 'postalCode': 'string', 'country': 'string', 'phoneNumber': 'string'}, 'cardPresent': True, 'cardholderPresent': True, 'encryptedCardData': {'deviceType': 'string', 'entryMode': 'string', 'encryptionMode': 'string', 'encryptionKeySerialNumber': 'string', 'encryptedData': 'string', 'encryptedTrack1': 'string', 'encryptedTrack1Length': 1, 'encryptedTrack2': 'string', 'encryptedTrack2Length': 1, 'cardHolderName': 'string'}})
    assert response.status_code == 200
