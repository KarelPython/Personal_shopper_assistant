from api_clients.llm_client import LLMClient
from api_clients.electronics_api_client import ElectronicsAPIClient
from utils.logger import logger
import json
from utils.i18n import get_text

    
class ElectronicsAdvisor:
    def __init__(self, llm_client: LLMClient, electronics_api_client: ElectronicsAPIClient):
        self.llm_client = llm_client
        self.electronics_api_client = electronics_api_client
        logger.info("ElectronicsAdvisor initialized with LLM and TechSpecs API clients.")

    def _format_specs_for_llm(self, specs: dict) -> str:
        if not specs:
            return "No specifications available."
        
        formatted_string = f"Device Name: {specs.get('name', 'N/A')}\n"
        relevant_keys = [
            "display", "processor", "ram", "storage", "camera", "battery", 
            "os", "dimensions", "weight", "features"
        ]

        for key in relevant_keys:
            if key in specs and specs[key]:
                value = specs[key]
                if isinstance(value, dict):
                    formatted_string += f"- {key.replace('_', ' ').title()}:\n"
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, (str, int, float, bool)) and sub_value != "":
                            formatted_string += f"  - {sub_key.replace('_', ' ').title()}: {sub_value}\n"
                elif isinstance(value, list):
                    formatted_string += f"- {key.replace('_', ' ').title()}: {', '.join(map(str, value))}\n"
                else:
                    if isinstance(value, (str, int, float, bool)) and value != "":
                        formatted_string += f"- {key.replace('_', ' ').title()}: {value}\n"
        return formatted_string.strip()
    
    def get_personalized_recommendation(self, user_requirements: str, lang: str = "en") -> str:
        logger.info(f"Generating personalized recommendation for requirements: '{user_requirements}' in lang: '{lang}'")

        category_options = "Smartphones, Tablety, Chytré hodinky, Notebooky, Stolní počítače".replace("Chytré hodinky", "Smartwatches")

        prompt_for_search_params = f"""
        Analyze the user's requirements for an electronic device.
        Extract the most suitable device category from: {category_options}. If no specific category is mentioned, state "all".
        Extract any specific brand mentioned (e.g., Apple, Samsung). If no brand, state "any".
        Identify key keywords/features (e.g., camera quality, battery life, performance, display, storage, portability, budget focus).
        
        User requirements: "{user_requirements}"

        Provide the output in a JSON format:
        {{"category": "category_name", "brand": "brand_name", "keywords": "comma-separated keywords"}}
        Example: {{"category": "Smartphones", "brand": "Samsung", "keywords": "great camera, long battery, good display"}}
        """

        llm_response_params = self.llm_client.get_completion(prompt_for_search_params, model="gpt-4o-mini")

        try:
            parsed_params = json.loads(llm_response_params)
            category_filter = parsed_params.get("category", "").strip()
            brand_filter = parsed_params.get("brand", "").strip()
            keywords_for_search = parsed_params.get("keywords", user_requirements).strip()
            
            if category_filter.lower() == "chytré hodinky":
                category_filter = "Smartwatches"
            elif category_filter.lower() == "notebooky":
                category_filter = "Notebooks"
            elif category_filter.lower() == "stolní počítače":
                category_filter = "Desktops"
            elif category_filter.lower() == "tablety":
                category_filter = "Tablets"
            elif category_filter.lower() == "smartphony":
                category_filter = "Smartphones"

            if category_filter.lower() == "all":
                category_filter = ""
            if brand_filter.lower() == "any":
                brand_filter = ""

            logger.info(f"LLM extracted: Category='{category_filter}', Brand='{brand_filter}', Keywords='{keywords_for_search}'")

        except json.JSONDecodeError:
            logger.error(f"Failed to parse LLM search params response as JSON: {llm_response_params}") 
            return get_text("error_llm_parse", lang)
        except Exception as e:
            logger.error(f"Unexpected error parsing LLM response: {e}")
            return get_text("error", lang)
        
        api_search_results = self.electronics_api_client.search_devices(
            query=keywords_for_search,
            category=category_filter,
            brand=brand_filter,
            limit=5)
        
        if not api_search_results:
            logger.warning(f"No devices found via TechSpecs API for search term: '{keywords_for_search}', category: '{category_filter}', brand: '{brand_filter}'")
            return get_text("no_devices_found", lang)
        
        detailed_specs_list = []
        for device_meta in api_search_results[:5]:
            specs = self.electronics_api_client.get_device_specs(device_meta["id"], lang=lang)
            if specs:
                detailed_specs_list.append(specs)
            else:
                logger.warning(f"Could not retrieve detailed specs for device ID: {device_meta['id']}")
        

        if not detailed_specs_list:
            logger.error("Could not retrieve detailed specifications for any of the found devices.")
            return get_text("error_no_detailed_specs", lang)
        

        formatted_specs = "\n\n---\n\n".join([self._format_specs_for_llm(s) for s in detailed_specs_list])

        recommendation_prompt = f"""
        Based on the user's requirements: "{user_requirements}"
        And the following detailed device specifications:

        {formatted_specs}

        Provide a personalized recommendation for the best electronic device from the listed options.
        Explain WHY this device fits the user's needs, specifically mentioning how its key features (e.g., display, processor, camera, battery life, design) align with the user's stated priorities.
        If multiple devices are suitable, recommend the single best one and briefly mention why others might also be considered, focusing on how well they match the *user's specific words and priorities*.
        Do not mention prices or cost, as this information is not available.
        Your response should be concise, helpful, and in {lang_to_english_name(lang)}.
        """
        logger.info(f"Generating personalized recommendation using LLM with detailed specs for lang: {lang}.")
        final_recommendation = self.llm_client.get_completion(recommendation_prompt, model="gpt-4o-mini")

        return final_recommendation
    
    def compare_devices(self, device_names: list[str], user_profile_summary: str = "", lang: str = "en") -> str:
        logger.info(f"Comparing devices: {device_names} with user profile: '{user_profile_summary}' in lang: '{lang}'")

        device_specs_to_compare = []
        for name in device_names:
            found = self.electronics_api_client.search_devices(query=name, limit=1, lang=lang)
            if found:
                specs = self.electronics_api_client.get_device_specs(found[0]["id"], lang=lang)
                if specs:
                    device_specs_to_compare.append(specs)
                else:
                    logger.warning(f"Could not retrieve detailed specs for device: {name}")
            else:
                logger.warning(f"Device '{name}' not found via TechSpecs API search.")

        if not device_specs_to_compare:
            return get_text("error_no_comparison_specs", lang)
        
        formatted_comparison_specs = "\n\n---\n\n".join([self._format_specs_for_llm(s) for s in device_specs_to_compare])

        comparison_prompt = f"""
        Compare the following electronic devices based on their detailed specifications.
        User's general preferences/summary: "{user_profile_summary}" (Use this to guide the importance of features).
        Highlight key differences and similarities that would be relevant to a user making a purchase decision.
        Organize the comparison clearly, focusing on important features like display, performance, camera, battery, and storage.
        Provide a summary explaining which device might be better for whom and why, *strictly based on specs and user preferences, not price*.
        Do not mention prices or cost.
        Your response should be concise, helpful, and in {lang_to_english_name(lang)}.

        Device specifications to compare:
        {formatted_comparison_specs}
        """
        logger.info(f"Generating device comparison using LLM with TechSpecs data for lang: {lang}.")
        comparison_result = self.llm_client.get_completion(comparison_prompt, model="gpt-4o-mini")
        return comparison_result
    
def lang_to_english_name(lang_code: str) -> str:
    if lang_code == "cs":
        return "Czech"
    return "English"