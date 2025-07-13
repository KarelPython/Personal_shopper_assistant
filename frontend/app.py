import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import streamlit as st
import json

from api_clients.llm_client import LLMClient
from api_clients.electronics_api_client import ElectronicsAPIClient
from core.advisor import ElectronicsAdvisor
from data_manager.database import DatabaseManager
from utils.i18n import get_text
from utils.logger import logger


@st.cache_resource
def get_llm_client():
    try:
        return LLMClient(api_key_env_var="OPENAI_API_KEY")
    except ValueError as e:
        logger.error(f"Failed to initialize OpenAI LLM client: {e}. No LLM client available. Check the .env file.")
        st.error("Error: no API key found for OpenAI LLM client. Check the .env file.")
        st.stop()

@st.cache_resource
def get_electronics_api_client():
    try:
        return ElectronicsAPIClient()
    except ValueError as e:
        logger.error(f"Failed to initialize ElectronicsAPIClient: {e}. Check TECHSPECS_API_ID and TECHSPECS_API_KEY in .env.")
        st.error("Error: API keys for TechSpecs are not available. Please check your .env file.")
        st.stop()

@st.cache_resource
def get_database_manager():
    db_manager = DatabaseManager()
    db_manager.connect()
    return db_manager


llm_client_instance = get_llm_client()
electronics_api_client_instance = get_electronics_api_client()
db_manager_instance = get_database_manager()
advisor_instance = ElectronicsAdvisor(llm_client_instance, electronics_api_client_instance)


def run_app():

    if 'lang' not in st.session_state:
        st.session_state.lang = "en"
    if 'current_user_id' not in st.session_state:
        st.session_state.current_user_id = os.getenv("USER", "default_user")
    if 'requirements_input' not in st.session_state:
        st.session_state.requirements_input = ""
    if 'compare_input' not in st.session_state:
        st.session_state.compare_input = ""

    with st.sidebar:
        st.title(get_text("select_language", st.session_state.lang))
        lang_options = {"English": "en", "Čeština": "cs"}
        selected_lang_name = st.radio(
            "",
            list(lang_options.keys()),
            index=list(lang_options.values()).index(st.session_state.lang)
        )
        st.session_state.lang = lang_options[selected_lang_name]

        st.markdown("---")

        st.text_input(
            get_text("user_id_label", st.session_state.lang),
            value=st.session_state.current_user_id,
            key="user_id_input_sidebar"
        )

        st.session_state.current_user_id = st.session_state.user_id_input_sidebar

        col1, col2 = st.columns(2)
        with col1:
            if st.button(get_text("save_profile", st.session_state.lang)):
                if st.session_state.current_user_id:
                    current_preferences = {
                        "requirements_input": st.session_state.get("requirements_input", ""),
                        "compare_input": st.session_state.get("compare_input", ""),
                    }
                    db_manager_instance.save_user_profile(
                        st.session_state.current_user_id,
                        json.dumps(current_preferences),
                        json.dumps([])
                    )
                    st.success(get_text("profile_saved", st.session_state.lang))
                else:
                    st.warning(get_text("no_user_id_warning", st.session_state.lang))

        with col2:
            if st.button(get_text("load_profile", st.session_state.lang)):
                if st.session_state.current_user_id:
                    profile = db_manager_instance.get_user_profile(st.session_state.current_user_id)
                    if profile:
                        loaded_prefs = json.loads(profile["preferences"])
                        st.session_state.requirements_input = loaded_prefs.get("requirements_input", "")
                        st.session_state.compare_input = loaded_prefs.get("compare_input", "")
                        st.success(get_text("profile_loaded", st.session_state.lang))
                    else:
                        st.info(get_text("no_profile_found", st.session_state.lang))
                else:
                    st.warning(get_text("no_user_id_warning", st.session_state.lang))

    st.title(get_text("welcome_title", st.session_state.lang))
    st.markdown("---")


    st.header(get_text("get_recommendation", st.session_state.lang))
    user_requirements = st.text_area(
        get_text("enter_requirements", st.session_state.lang),
        height=100,
        key="requirements_input"
    )

    if st.button(get_text("get_recommendation_button", st.session_state.lang), key="recommend_button"):
        if user_requirements:
            with st.spinner(get_text("loading", st.session_state.lang)):
                try:
                    recommendation = advisor_instance.get_personalized_recommendation(
                        user_requirements,
                        lang=st.session_state.lang
                    )
                    st.subheader(get_text("recommendation_for_you", st.session_state.lang))
                    st.write(recommendation)
                except Exception as e:
                    logger.error(f"Error getting recommendation: {e}")
                    st.error(get_text("error", st.session_state.lang))
        else:
            st.warning(get_text("enter_requirements_warning", st.session_state.lang))

    st.markdown("---")

    st.header(get_text("compare_devices", st.session_state.lang))
    device_names_input = st.text_input(
        get_text("enter_device_names", st.session_state.lang),
        key="compare_input"
    )

    if st.button(get_text("compare", st.session_state.lang), key="compare_button"):
        if device_names_input:
            device_list = [name.strip() for name in device_names_input.split(',') if name.strip()]
            if device_list:
                with st.spinner(get_text("loading", st.session_state.lang)):
                    try:
                        user_profile_summary = ""
                        if st.session_state.current_user_id:
                            profile = db_manager_instance.get_user_profile(st.session_state.current_user_id)
                            if profile and profile['preferences']:
                                user_profile_summary = json.loads(profile['preferences']).get("requirements_input", "")
                        
                        comparison = advisor_instance.compare_devices(
                            device_list,
                            user_profile_summary,
                            lang=st.session_state.lang
                        )
                        st.subheader(get_text("comparison_result", st.session_state.lang))
                        st.write(comparison)
                    except Exception as e:
                        logger.error(f"Error comparing devices: {e}")
                        st.error(get_text("error", st.session_state.lang))
            else:
                st.warning(get_text("enter_device_names_warning", st.session_state.lang))
        else:
            st.warning(get_text("enter_device_names_warning", st.session_state.lang))

    st.markdown("---")

    st.subheader(get_text("future_work_title", st.session_state.lang))
    st.write(get_text("future_work_description", st.session_state.lang))

run_app()