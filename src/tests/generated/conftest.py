import pytest
import requests

@pytest.fixture
def base_url():
    """Base URL for the API."""
    return "http://localhost:8502"  # Replace with your actual API base URL

@pytest.fixture
def headers():
    """Common headers for API requests."""
    return {
        "Content-Type": "application/json",
        "Authorization": "PMAK-6852cde6134d13000180adc0-0a0c477664d3aa340e51077f563a400e82e"  # Replace with your actual auth token
    }
