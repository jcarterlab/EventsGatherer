import logging
import json

from eventsmonitor.scraping.selenium_fetcher import (
    initialise_driver,
    load_page,
    quit_driver,
)
from eventsmonitor.scraping.generic_parser import generic_parser
from eventsmonitor.scraping.visit_london_parser import visit_london_parser


# ----------------------------------------------------------------------
# LOGGING SETUP
# ----------------------------------------------------------------------

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# PARSER REGISTRY
# ----------------------------------------------------------------------

PARSERS = {
    'generic_parser': generic_parser,
    'visit_london_parser': visit_london_parser
}


# ----------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------

def extract_text(html, source):
    parser_name = source['parsing']['parser_name']

    parser = PARSERS.get(parser_name)

    if parser is None:
        raise ValueError(f'Unknown parser: {parser_name}')

    return parser(html, source)


# ----------------------------------------------------------------------
# ORCHESTRATION FUNCTIONS
# ----------------------------------------------------------------------

def scrape_content(config):
    selenium_used = False

    with open('sources.json', 'r', encoding='utf-8') as file:
        sources = json.load(file)

    texts = []

    for source in sources:
        if source['scraping']['requires_selenium']:
            driver = initialise_driver(config)
            html = load_page(driver, source)

            selenium_used = True
        else:
            continue

        if html is None:
            logger.warning(
                'Skipping source=%s because page did not load',
                source['name']
            )
            continue
        
        text = extract_text(html, source)
        texts.append(text)

    if selenium_used:
        quit_driver(driver)

    return ' '.join(texts)
