TRANSLATIONS = {
    "en": {
        "welcome_title": "AI Personal Shopper & Electronics Advisor",
        "select_language": "Select Language",
        "cz_lang": "Čeština",
        "en_lang": "English",
        "enter_requirements": "Enter your requirements (e.g., 'I need a phone with a great camera for travel and long battery life'):",
        "get_recommendation": "Get Recommendation",
        "recommendation_for_you": "Recommendation for you:",
        "compare_devices": "Compare Devices",
        "enter_device_names": "Enter device names to compare (comma-separated, e.g., 'iPhone 15 Pro, Samsung Galaxy S24 Ultra'):",
        "compare": "Compare",
        "comparison_result": "Comparison Result:",
        "about_me": "About Me (for personalized advice):",
        "save_profile": "Save Profile",
        "profile_saved": "Profile saved!",
        "profile_loaded": "Profile loaded!",
        "no_profile": "No profile found for this user ID.",
        "user_id_label": "Your User ID (e.g., 'user123'):",
        "loading": "Loading...",
        "error": "An error occurred. Please try again.",
        "model_explanation_title": "Understanding the AI Model's Choices",
        "model_explanation_desc": "Our AI analyzes your needs by breaking them down into technical parameters and then cross-references them with device specifications. It considers factors like performance, camera quality, battery life, and your budget to suggest the best match.",
        "future_work_title": "Future Work",
        "future_work_desc": "In future iterations, we plan to integrate real-time price tracking, expand device categories (laptops, smartwatches), enable direct purchase links, and enhance AI with more nuanced user feedback loops. We also aim to incorporate advanced sentiment analysis for deeper review insights and predictive analytics for market trends.",
        "error_llm_parse": "I could not fully understand your requirements. Please try again with clearer descriptions.",
        "no_devices_found": "No devices found matching your criteria. Please try different requirements.",
        "error_no_detailed_specs": "Could not retrieve detailed specifications for the recommended devices.",
        "error_no_comparison_specs": "Could not retrieve specifications for the specified devices. Please check the names and try again.",
        "load_profile": "Load Profile",
        "no_user_id_warning": "Please enter a User ID to save/load your profile.",
        "enter_requirements_warning": "Please enter your requirements.",
        "enter_device_names_warning": "Please enter device names to compare."
    },
    "cs": {
        "welcome_title": "AI Osobní Nákupčí a Elektronický Poradce",
        "select_language": "Vyberte jazyk",
        "cz_lang": "Čeština",
        "en_lang": "English",
        "enter_requirements": "Zadejte své požadavky (např. 'Potřebuji telefon s parádním foťákem na cestování a dlouhou výdrží baterie'):",
        "get_recommendation": "Získat doporučení",
        "recommendation_for_you": "Doporučení pro vás:",
        "compare_devices": "Porovnat zařízení",
        "enter_device_names": "Zadejte názvy zařízení k porovnání (oddělené čárkami, např. 'iPhone 15 Pro, Samsung Galaxy S24 Ultra'):",
        "compare": "Porovnat",
        "comparison_result": "Výsledek porovnání:",
        "about_me": "O mně (pro personalizované rady):",
        "save_profile": "Uložit profil",
        "profile_saved": "Profil uložen!",
        "profile_loaded": "Profil načten!",
        "no_profile": "Pro toto ID uživatele nebyl nalezen žádný profil.",
        "user_id_label": "Vaše uživatelské ID (např. 'user123'):",
        "loading": "Načítám...",
        "error": "Došlo k chybě. Zkuste to prosím znovu.",
        "model_explanation_title": "Pochopení voleb AI modelu",
        "model_explanation_desc": "Naše AI analyzuje vaše potřeby tím, že je rozděluje na technické parametry a poté je křížově porovnává se specifikacemi zařízení. Bere v úvahu faktory jako výkon, kvalitu fotoaparátu, životnost baterie a váš rozpočet, aby navrhla nejlepší shodu.",
        "future_work_title": "Budoucí práce",
        "future_work_desc": "V budoucích iteracích plánujeme integrovat sledování cen v reálném čase, rozšířit kategorie zařízení (notebooky, chytré hodinky), povolit přímé nákupní odkazy a vylepšit AI o nuance zpětné vazby od uživatelů. Naším cílem je také začlenit pokročilou analýzu sentimentu pro hlubší náhledy na recenze a prediktivní analýzu pro trendy na trhu.",
        "error_llm_parse": "Nemohl(a) jsem plně porozumět vašim požadavkům. Zkuste to prosím znovu s jasnějším popisem.",
        "no_devices_found": "Nebyly nalezeny žádné zařízení odpovídající vašim kritériím. Zkuste prosím jiné požadavky.",
        "error_no_detailed_specs": "Nepodařilo se načíst podrobné specifikace pro doporučená zařízení.",
        "error_no_comparison_specs": "Nepodařilo se načíst specifikace pro zadaná zařízení. Zkontrolujte prosím názvy a zkuste to znovu.",
        "load_profile": "Načíst profil",
        "no_user_id_warning": "Zadejte prosím uživatelské ID pro uložení/načtení profilu.",
        "enter_requirements_warning": "Zadejte prosím vaše požadavky.",
        "enter_device_names_warning": "Zadejte prosím názvy zařízení k porovnání."
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """
    Vrátí lokalizovaný text pro daný klíč a jazyk.
    Pokud klíč nebo jazyk neexistuje, vrátí klíč samotný nebo anglickou verzi.
    """
    # Zkusí vrátit text pro zadaný jazyk, jinak se vrátí k angličtině
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)