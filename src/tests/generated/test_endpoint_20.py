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
    url = 'http://localhost:8502/v1.5/card/info'
    response = requests.post(url, headers=headers, json={'encryptedCardData': {'deviceType': 'string', 'entryMode': 'string', 'encryptionMode': 'string', 'encryptionKeySerialNumber': 'string', 'encryptedData': 'string', 'encryptedTrack1': 'string', 'encryptedTrack1Length': 1, 'encryptedTrack2': 'string', 'encryptedTrack2Length': 1, 'cardHolderName': 'string'}})
    assert response.status_code == 200
