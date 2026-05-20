"""
Application configuration settings.

Loads environment variables and defines application-wide
constants for scraping, LLM processing and email delivery.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Environment
# --------------------------------------------------

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
SOURCES_PATH = BASE_DIR / 'sources.json'


# --------------------------------------------------
# Monitoring parameters
# --------------------------------------------------

LOCATION = os.getenv('LOCATION', 'London')
ENTITY_OF_CONCERN = os.getenv('ENTITY_OF_CONCERN', 'a hostel')
IDENTIFICATION_CONFIDENCE_THRESHOLD = int(os.getenv('IDENTIFICATION_CONFIDENCE_THRESHOLD', 95))


# --------------------------------------------------
# Scraping
# --------------------------------------------------

SELENIUM_HEADLESS = os.getenv('SELENIUM_HEADLESS', 'true').lower() == 'true'
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
LLM_RETRY_ATTEMPTS = int(os.getenv('LLM_RETRY_ATTEMPTS', 4))
LLM_WAIT_TIME = int(os.getenv('LLM_WAIT_TIME', 5))
BASIC_MODEL = os.getenv('BASIC_MODEL', 'gemini-2.5-flash')
ADVANCED_MODEL = os.getenv('ADVANCED_MODEL', 'gemini-2.5-pro')


# --------------------------------------------------
# Email
# --------------------------------------------------

RESEND_API_KEY = os.getenv('RESEND_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL') or 'onboarding@resend.dev'
EMAIL_RETRY_ATTEMPTS = int(os.getenv('EMAIL_RETRY_ATTEMPTS', 3))
EMAIL_WAIT_TIME = int(os.getenv('EMAIL_WAIT_TIME', 2))
TO_EMAIL = os.getenv('TO_EMAIL')