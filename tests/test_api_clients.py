import pytest
from unittest.mock import MagicMock, patch
import os
import requests
import urllib.parse

@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test_openai_key",
        "TECHSPECS_API_ID": "test_techspecs_id",
        "TECHSPECS_API_KEY": "test_techspecs_key"
    }):
        yield

from api_clients.llm_client import LLMClient
from utils.logger import logger
from utils.i18n import get_text, TRANSLATIONS

def test_llm_client_initialization_openai():
    client = LLMClient(api_key_env_var="OPENAI_API_KEY")
    assert client.api_key == "test_openai_key"
    assert client.client is not None

@patch('api_clients.llm_client.OpenAI')
def test_llm_get_completion_success(mock_openai):
    mock_instance = mock_openai.return_value
    mock_instance.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Mocked AI response"))]
    )

    client = LLMClient(api_key_env_var="OPENAI_API_KEY")
    response = client.get_completion("Test prompt for AI", model="gpt-4o-mini")
    assert response == "Mocked AI response"
    mock_instance.chat.completions.create.assert_called_once_with(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Test prompt for AI"}]
    )

@patch('api_clients.llm_client.OpenAI')
def test_llm_get_completion_api_error(mock_openai):
    mock_instance = mock_openai.return_value
    mock_instance.chat.completions.create.side_effect = Exception("API rate limit exceeded")

    client = LLMClient(api_key_env_var="OPENAI_API_KEY")
    response = client.get_completion("Error prompt")
    expected_error_message_from_llm_client = "Omlouváme se, došlo k chybě při zpracování vašeho požadavku."
    assert expected_error_message_from_llm_client in response


from api_clients.electronics_api_client import ElectronicsAPIClient

def test_electronics_api_client_initialization():
    client = ElectronicsAPIClient()
    assert client.api_id == "test_techspecs_id"
    assert client.api_key == "test_techspecs_key"
    assert "x-api-id" in client.headers
    assert "x-api-key" in client.headers

@patch('requests.get') # Mockuje funkci requests.get
def test_electronics_search_devices_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "products": [
            {"id": "prod1", "name": "Test Phone 1"},
            {"id": "prod2", "name": "Test Phone 2"}
        ]
    }
    mock_get.return_value = mock_response

    client = ElectronicsAPIClient()
    results = client.search_devices("test query", category="Smartphones")
    assert len(results) == 2
    assert results[0]["name"] == "Test Phone 1"
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    called_url = args[0]
    print(f"\nDEBUG: Called URL: {called_url}, Type: {type(called_url)}") # Debug print
    parsed_url = urllib.parse.urlparse(called_url)
    assert parsed_url.scheme == 'https'
    assert parsed_url.netloc == 'api.techspecs.io'
    assert parsed_url.path == '/v5/product/search'
    assert kwargs['params']['query'] == 'test query'
    assert kwargs['params']['category'] == 'Smartphones'

@patch('requests.get')
def test_electronics_get_device_specs_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "id": "prod1",
        "name": "Test Phone 1",
        "display": {"size": "6.1 inch", "resolution": "1080x2340"},
        "processor": "MockChip A1"
    }
    mock_get.return_value = mock_response

    client = ElectronicsAPIClient()
    specs = client.get_device_specs("prod1")
    assert specs["name"] == "Test Phone 1"
    assert "display" in specs
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    called_url = args[0]
    print(f"\nDEBUG: Called URL: {called_url}, Type: {type(called_url)}") # Debug print
    parsed_url = urllib.parse.urlparse(called_url)
    assert parsed_url.scheme == 'https'
    assert parsed_url.netloc == 'api.techspecs.io'
    assert parsed_url.path == '/v5/product/prod1'
    assert kwargs['params']['language'] == 'en'
    assert kwargs['params']['keepCasing'] == True

@patch('requests.get')
def test_electronics_api_request_http_error(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Client Error: Not Found for url: TEST_URL", response=mock_response
    )
    mock_get.return_value = mock_response

    client = ElectronicsAPIClient()
    with patch.object(logger, 'error') as mock_logger_error:
        result = client.search_devices("nonexistent") 
        
        assert isinstance(result, list) 
        assert not result

        mock_logger_error.assert_called_once()
        assert "HTTP error" in mock_logger_error.call_args[0][0]
        assert "404" in mock_logger_error.call_args[0][0]

    mock_get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()



    

