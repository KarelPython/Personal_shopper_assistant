import pytest
from unittest.mock import MagicMock, patch
from core.advisor import ElectronicsAdvisor
from api_clients.llm_client import LLMClient
from api_clients.electronics_api_client import ElectronicsAPIClient

@pytest.fixture
def mock_llm_client():
    # Provides a mock for LLMClient
    mock_client = MagicMock(spec=LLMClient)
    mock_client.get_completion.return_value = '{"category": "Smartphones", "brand": "Samsung", "keywords": "great camera, long battery"}'
    return mock_client

@pytest.fixture
def mock_electronics_api_client():
    # Provides a mock for ElectronicsAPIClient
    mock_client = MagicMock(spec=ElectronicsAPIClient)
    
    # Mock for search_devices
    mock_client.search_devices.return_value = [
        {"id": "samsung_s24", "name": "Samsung Galaxy S24 Ultra"},
        {"id": "iphone_15", "name": "iPhone 15 Pro"}
    ]

    # Mock for get_device_specs
    def get_specs_side_effect(device_id, **kwargs):
        if device_id == "samsung_s24":
            return {
                "id": "samsung_s24",
                "name": "Samsung Galaxy S24 Ultra",
                "display": {"size": "6.8-inch", "resolution": "QHD+"},
                "processor": "Snapdragon 8 Gen 3",
                "camera": {"main": "200MP"},
                "battery": "5000 mAh",
                "os": "Android"
            }
        elif device_id == "iphone_15":
            return {
                "id": "iphone_15",
                "name": "iPhone 15 Pro",
                "display": {"size": "6.1-inch", "resolution": "Super Retina XDR"},
                "processor": "A17 Pro",
                "camera": {"main": "48MP"},
                "battery": "4000 mAh", # Simplified value for the test
                "os": "iOS"
            }
        return {}
    mock_client.get_device_specs.side_effect = get_specs_side_effect

    return mock_client

@pytest.fixture
def advisor(mock_llm_client, mock_electronics_api_client):
    # Creates an Advisor instance with mocked clients
    return ElectronicsAdvisor(mock_llm_client, mock_electronics_api_client)

def test_get_personalized_recommendation_success(advisor, mock_llm_client, mock_electronics_api_client):
    user_req = "I need a phone with a great camera and long battery life, preferably a Samsung."

    # We mock the second LLM answer for the final recommendation
    mock_llm_client.get_completion.side_effect = [
        '{"category": "Smartphones", "brand": "Samsung", "keywords": "great camera, long battery"}', # První volání pro extrakci parametrů
        "Based on your needs, the Samsung Galaxy S24 Ultra is highly recommended due to its 200MP camera and 5000 mAh battery." # Druhé volání pro finální doporučení
    ]

    recommendation = advisor.get_personalized_recommendation(user_req, lang="en")

    assert "Samsung Galaxy S24 Ultra is highly recommended" in recommendation
    assert mock_llm_client.get_completion.call_count == 2 # Two LLM calls
    assert mock_electronics_api_client.search_devices.called # Checking that the search API was called
    assert mock_electronics_api_client.get_device_specs.called # Checking that the specifications API was called


def test_compare_devices_success(advisor, mock_llm_client, mock_electronics_api_client):
    device_names = ["Samsung S24 Ultra", "iPhone 15 Pro"]
    user_profile = "I prioritize camera quality and battery life."

    # We mock LLM answer for comparison
    mock_llm_client.get_completion.return_value = "The Samsung S24 Ultra has a better camera and larger battery, while iPhone 15 Pro offers superior performance for gaming."

    comparison_result = advisor.compare_devices(device_names, user_profile, lang="en")

    assert "Samsung S24 Ultra has a better camera" in comparison_result
    assert "iPhone 15 Pro offers superior performance" in comparison_result
    assert mock_electronics_api_client.search_devices.call_count == 2 # Called for each device
    assert mock_electronics_api_client.get_device_specs.call_count == 2 # Called for each device

def test_get_personalized_recommendation_no_devices_found(advisor, mock_llm_client, mock_electronics_api_client):
    user_req = "I need a very rare phone model."
    mock_llm_client.get_completion.return_value = '{"category": "Smartphones", "brand": "RareBrand", "keywords": "rare model"}'
    mock_electronics_api_client.search_devices.return_value = [] # We simulate that nothing was found

    recommendation = advisor.get_personalized_recommendation(user_req, lang="en")
    assert "No devices found matching your criteria" in recommendation
