import pytest
from utils.i18n import get_text, TRANSLATIONS # We also import TRANSLATIONS for direct content testing

def test_get_text_english():
    assert get_text("welcome_title", "en") == "AI Personal Shopper & Electronics Advisor"
    assert get_text("error", "en") == "An error occurred. Please try again."

def test_get_text_czech():
    assert get_text("welcome_title", "cs") == "AI Osobní Nákupčí a Elektronický Poradce"
    assert get_text("error", "cs") == "Došlo k chybě. Zkuste to prosím znovu."

def test_get_text_non_existent_key():
    assert get_text("non_existent_key", "en") == "non_existent_key" # It should return the key itself
    assert get_text("non_existent_key", "cs") == "non_existent_key"

def test_get_text_unsupported_language_falls_back_to_english():
    assert get_text("welcome_title", "fr") == "AI Personal Shopper & Electronics Advisor" # It should fall into English