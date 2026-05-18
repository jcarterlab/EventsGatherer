import logging 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ----------------------------------------------------------------------
# LOGGING SETUP
# ----------------------------------------------------------------------
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------

def initialise_driver(config):
    headless = config.SELENIUM_HEADLESS
    window_size = config.SELENIUM_WINDOW_SIZE
    user_agent = config.SELENIUM_USER_AGENT

    logger.info(
        'Creating Chrome driver headless=%s window_size=%s',
        headless,
        window_size
    )

    options = Options()

    if headless:
        options.add_argument('--headless=new')

    options.add_argument(f'--window-size={window_size}')
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    if config.ENVIRONMENT == 'production':
        options.binary_location = '/usr/bin/chromium'

    return webdriver.Chrome(options=options)


def load_page(driver, source): 
    try:
        logger.info('Opening page url=%s', source['page_url'])
        driver.get(source['page_url'])

        WebDriverWait(driver, source['scraping']['wait_seconds']).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, source['scraping']['wait_selector'] ))
        )

        return driver.page_source
    
    except Exception: 
        logger.warning(
            'Error processing source url=%s',
            source['page_url'],
            exc_info=True
        )
        return None
    

def quit_driver(driver):
    logger.info('Closing Chrome driver')
    driver.quit()