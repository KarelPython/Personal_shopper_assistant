Ok, here's a `README.md` file in English that should allow anyone to set up and run your application, including clear instructions for Streamlit.

-----

# AI Personal Shopper & Electronics Advisor

## Overview

The AI Personal Shopper & Electronics Advisor is an innovative application designed to help users make informed purchasing decisions for electronic devices. Leveraging the power of Large Language Models (LLMs) and a third-party TechSpecs API, it provides personalized recommendations and detailed comparisons of mobile phones based on user-defined requirements, without focusing on pricing (at this stage).

The application is built with a modular and extensible architecture, allowing for future enhancements such as real-time price tracking, broader product categories, and advanced AI features.

-----

## Features

  * **Personalized Recommendations:** Get tailored suggestions for mobile phones by describing your needs in natural language (e.g., "I need a phone with a great camera for travel and long battery life").
  * **Detailed Device Comparison:** Compare multiple devices side-by-side with AI-generated insights highlighting key differences and similarities based on technical specifications.
  * **Multilingual Support:** Seamlessly switch between English and Czech for the user interface.
  * **User Profile Management:** Save and load your preferences for a consistent and personalized experience.
  * **AI Model Explanation:** Understand how the AI processes your requests and generates recommendations.

-----

## Technologies Used

  * **Python 3.8+**: The core programming language.
  * **Streamlit**: For creating the interactive web-based user interface.
  * **OpenAI API / Gemini API**: For Large Language Model capabilities (natural language processing, recommendation generation, comparison analysis).
  * **TechSpecs API**: For fetching detailed electronic device specifications.
  * **Requests**: For making HTTP requests to external APIs.
  * **python-dotenv**: For securely managing API keys and environment variables.
  * **SQLite**: A lightweight, file-based database for storing user profiles and preferences.
  * **Pytest**: For unit testing key components of the application.
  * **Logging**: For internal application monitoring and debugging.

-----

## Setup and Installation

Follow these steps to set up and run the application locally.

### 1\. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/your-username/personal-shopper-assistant.git
cd personal-shopper-assistant
```

### 2\. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies:

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3\. Install Dependencies

Once the virtual environment is active, install the required Python packages:

```bash
pip install -r requirements.txt
```

Make sure your `requirements.txt` file contains:

```
streamlit
openai          # or google-generativeai if you primarily use Gemini
requests
python-dotenv
pytest
pytest-mock
```

### 4\. Configure API Keys

You will need API keys for the AI models and the TechSpecs API.

1.  **Create a `.env` file** in the root directory of your project (the same directory as `README.md`).

2.  **Add your API keys** to this `.env` file. Replace the placeholder values with your actual keys:

    ```env
    # TechSpecs API keys (mandatory for device data)
    TECHSPECS_API_ID="YOUR_TECHSPECS_API_ID"
    TECHSPECS_API_KEY="YOUR_TECHSPECS_API_KEY"

    # AI Model API keys (choose at least one)
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY" # Only if you want to use Gemini
    ```

    **Important:** Do NOT commit your `.env` file to version control (e.g., Git). It's already included in `.gitignore` to prevent this.

-----

## Running the Application

The application uses Streamlit for its user interface.

### To Start the Streamlit App:

1.  Ensure your virtual environment is activated.

2.  Navigate to the project's root directory in your terminal.

3.  Run the Streamlit application:

    ```bash
    streamlit run frontend/app.py
    ```

This command will open the application in your default web browser (usually at `http://localhost:8501`).

-----

## Running Tests

The project includes unit tests to ensure the reliability of its core components.

### To Run the Tests:

1.  Ensure your virtual environment is activated.

2.  Navigate to the project's root directory in your terminal.

3.  Run Pytest:

    ```bash
    pytest
    ```

You should see a summary of passed and failed tests. All tests should pass for the application to be considered stable.

-----

## Project Structure

```
personal_shopper/
├── api_clients/            # Modules for interacting with external APIs (LLM, TechSpecs)
│   ├── __init__.py
│   ├── llm_client.py       # Handles communication with OpenAI/Gemini
│   └── electronics_api_client.py # Handles communication with TechSpecs API
├── config/                 # Configuration files (currently minimal)
│   └── __init__.py
├── core/                   # Core application logic (AI Advisor)
│   ├── __init__.py
│   └── advisor.py          # Contains the main recommendation and comparison logic
├── data_manager/           # Handles data storage and retrieval (SQLite)
│   ├── __init__.py
│   └── database.py         # Manages database connections and operations
├── frontend/               # Streamlit application files
│   ├── __init__.py
│   └── app.py              # The main Streamlit app for the UI
├── tests/                  # Unit tests for the project's modules
│   ├── __init__.py
│   ├── test_api_clients.py # Tests API client interactions
│   ├── test_advisor.py     # Tests the core advisor logic
│   └── test_utils.py       # Tests utility functions
├── utils/                  # Utility functions (logging, internationalization)
│   ├── __init__.py
│   ├── i18n.py             # Handles multilingual text translations
│   └── logger.py           # Configures application logging
├── .env                    # Environment variables (API keys - DO NOT COMMIT!)
├── .gitignore              # Specifies files/directories to ignore in Git
├── README.md               # This documentation file
└── requirements.txt        # Lists project dependencies
```

-----

## Future Work

This project is designed to be extensible, and several enhancements are planned or can be explored:

  * **Real-time Price Tracking:** Integrate a reliable Price API to include current market prices in recommendations and comparisons, and suggest the best deals.
  * **Expanded Device Categories:** Extend the application beyond mobile phones to include laptops, tablets, smartwatches, televisions, and other electronics.
  * **Advanced AI Features:** Implement more sophisticated AI models for nuanced user profiling, predictive analytics (e.g., future price drops, new model releases), and interactive conversational flows.
  * **Sentiment Analysis for Reviews:** Utilize NLP to summarize user reviews, extracting common pros and cons for each device to provide a more holistic view.
  * **User Account System:** Develop a more robust user authentication and profile management system for persistent settings and personalized history.
  * **Visualizations:** Enhance the UI with interactive charts and graphs for clearer data comparison and trend analysis.
  * **Direct Purchase Links:** Provide links to e-commerce sites where recommended products can be purchased.
  * **Deployment Optimization:** Optimize the application for cloud deployment platforms (e.g., Streamlit Cloud, PythonAnywhere, Heroku) for wider accessibility.