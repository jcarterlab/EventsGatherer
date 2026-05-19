"""
Selenium page fetching utilities.

Provides helper functions for:
- Chrome WebDriver initialization
- dynamic page loading
- safe driver shutdown

Used for sources requiring JavaScript rendering.
"""

import logging 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logger = logging.getLogger(__name__)


def initialise_driver(config):
    """
    Create and configure a Chrome WebDriver instance.

    Args:
        config: Application configuration object containing
            Selenium settings.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    headless = config.SELENIUM_HEADLESS
    window_size = config.SELENIUM_WINDOW_SIZE
    user_agent = config.SELENIUM_USER_AGENT

    logger.info(
        'Creating Chrome driver headless=%s window_size=%s',
        headless,
        window_size
    )

    options = Options()

    # Use system-installed Chromium in containerized production environments
    if config.ENVIRONMENT == 'production':
        options.binary_location = '/usr/bin/chromium'

    if headless:
        options.add_argument('--headless=new')

    options.add_argument(f'--window-size={window_size}')
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    return webdriver.Chrome(options=options)


def load_page(driver, source): 
    """
    Load a page and wait for the configured selector to appear.

    Args:
        driver: Active Selenium WebDriver instance.
        source: Single source configuration dictionary
            containing page URL and scraping settings.

    Returns:
        str | None: Rendered page HTML if successful,
            otherwise None.
    """
    page_url = source['page_url']
    wait_seconds = source['scraping']['wait_seconds']
    wait_selector = source['scraping']['wait_selector']

    try:
        logger.info('Opening page url=%s', page_url)

        driver.get(page_url)

        WebDriverWait(driver, wait_seconds).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    wait_selector
                )
            )
        )

        return driver.page_source
    
    except Exception: 
        logger.warning(
            'Error loading page url=%s',
            page_url,
            exc_info=True
        )
        return None
    

def quit_driver(driver):
    """
    Close the Chrome WebDriver instance safely.

    Args:
        driver: Active Selenium WebDriver instance.
    """
    logger.info('Closing Chrome driver')

    driver.quit()