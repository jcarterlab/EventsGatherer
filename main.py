import logging
import config

from google import genai

from eventsmonitor.scrape_content import scrape_content
from eventsmonitor.email_summary import send_email
from eventsmonitor.summarise_content import summarise_content


# ----------------------------------------------------------------------
# LOGGING SETUP
# ----------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# MAIN PIPELINE
# ----------------------------------------------------------------------

def run_pipeline(client, config):
    text = scrape_content(config)    
    summary = summarise_content(client, text, config)
    send_email(summary, config.TO_EMAIL, config)



# ----------------------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------------------

if __name__ == '__main__':
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    run_pipeline(client, config)