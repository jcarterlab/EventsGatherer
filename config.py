from dotenv import load_dotenv
from pathlib import Path
import os
import json

load_dotenv()

# --------------------------------------------------
# Environment
# --------------------------------------------------

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development') # development or production


# --------------------------------------------------
# Monitoring parameters
# --------------------------------------------------

LOCATION = os.getenv('LOCATION', 'London') # location
ENTITY_OF_CONCERN = os.getenv('ENTITY_OF_CONCERN', 'a hostel') # type of organisation
IDENTIFICATION_CONFIDENCE_THRESHOLD = int(os.getenv('IDENTIFICATION_CONFIDENCE_THRESHOLD', 95)) # percentage (0–100)


# --------------------------------------------------
# Scraping
# --------------------------------------------------

SELENIUM_HEADLESS = True
SELENIUM_WINDOW_SIZE = '1920,1080'
SELENIUM_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/136.0.0.0 Safari/537.36'
)


# --------------------------------------------------
# LLM
# --------------------------------------------------

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
LLM_RETRY_ATTEMPTS = int(os.getenv('LLM_RETRY_ATTEMPTS', 3)) # retries
LLM_WAIT_TIME = int(os.getenv('LLM_WAIT_TIME', 10)) # seconds
BASIC_MODEL = os.getenv('BASIC_MODEL', 'gemini-2.5-flash') # model type
ADVANCED_MODEL = os.getenv('ADVANCED_MODEL', 'gemini-2.5-pro') # model type


# --------------------------------------------------
# Email
# --------------------------------------------------

RESEND_API_KEY = os.getenv('RESEND_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL') or 'onboarding@resend.dev'
EMAIL_RETRY_ATTEMPTS = int(os.getenv('EMAIL_RETRY_ATTEMPTS', 3)) # retries
EMAIL_WAIT_TIME = int(os.getenv('EMAIL_WAIT_TIME', 2)) # second
TO_EMAIL = os.getenv('TO_EMAIL')