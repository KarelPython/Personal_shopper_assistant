import os
import requests
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

class ElectronicsAPIClient:
    def __init__(self,
                 api_id_env_var="TECHSPECS_API_ID",
                 api_key_env_var="TECHSPECS_API_KEY"):

        self.api_id = os.getenv(api_id_env_var)
        self.api_key = os.getenv(api_key_env_var)

        if not self.api_id:
            logger.error(f"API ID not found for {api_id_env_var}")
            raise ValueError(f"API ID environment variable {api_id_env_var} not set.")

        if not self.api_key:
            logger.error(f"Missing API key in environment variables: {api_key_env_var}")
            raise ValueError(f"API key environment variable {api_key_env_var} not set.")
        
        self.base_url = "https://api.techspecs.io/v5"
        self.headers = {
            "accept": "application/json",
            "x-api-id": self.api_id,    # API ID v hlavičce
            "x-api-key": self.api_key   # API klíč v hlavičce
        }
        logger.info("ElectronicsAPIClient initialized with TechSpecs API ID and Key.")

    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        
        url = f"{self.base_url}/{endpoint}"


        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
            return {"error": f"HTTP error: {http_err.response.status_code} - {http_err.response.text}"}
        
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Connection error occurred: {conn_err}")
            return {"error": "Could not connect to the API. Please check your internet connection."}
        
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"Timeout error occurred: {timeout_err}")
            return {"error": "The API request timed out."}
        
        except requests.exceptions.RequestException as req_err:
            logger.error(f"An unexpected error occurred during API request: {req_err}")
            return {"error": f"An unexpected error occurred: {req_err}"}
        
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return {"error": f"An unexpected error occurred: {e}"}
        
    def search_devices(self,
                        query: str,
                        category: str = "",
                        brand: str = "",
                        limit: int = 10,
                        page: int = 0,
                        keep_casing: bool = True) -> list[dict]:
        """
        Search for devices based on query, category, and brand.
        Returns a list of dictionaries with ID and name of the devices.
        """
        endpoint = "product/search"
        params = {
            "query": query,
            "page": page,
            "size": limit,
            "keepCasing": keep_casing
        }

        if category:
            params["category"] = category
        if brand:
            params["brand"] = brand

        logger.info(f"Searching for devices with query: '{query}', category: '{category}', brand: '{brand}'")
        data = self._make_request(endpoint, params)

        if "error" in data:
            return []

        if data and isinstance(data, dict) and "products" in data:
            return [{"id": p.get("id"), "name": p.get("name")} for p in data["products"] if p.get("id") and p.get("name")]
       
        else:
            logger.warning(f"Unexpected search response format or no products found for query '{query}': {data}")
            return []
        
    def get_device_specs(self, product_id: str, keep_casing: bool = True, lang: str = "en") -> dict:
        """
        Get detailed specifications for a specific device by product ID.
        Returns a dictionary with the device specifications.
        """
        endpoint = f"product/{product_id}"
        params = {
            "keepCasing": keep_casing,
            "language": lang
        }
        logger.info(f"Getting specs for product ID: '{product_id}' (lang: {lang})")
        data = self._make_request(endpoint, params)

        if "error" in data:
            return {}

        if data and isinstance(data, dict) and "id" in data: 
            return data
       
        else:
            logger.warning(f"Unexpected get_specs response format or no data for product ID '{product_id}': {data}")
            return {}

