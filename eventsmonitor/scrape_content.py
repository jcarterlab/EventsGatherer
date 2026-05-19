"""
Content scraping orchestration utilities.

Coordinates:
- page fetching
- parser selection
- content extraction

Supports both Selenium-based and non-Selenium scraping
workflows.
"""

import logging
import json

from eventsmonitor.scraping.selenium_fetcher import (
    initialise_driver,
    load_page,
    quit_driver,
)

from eventsmonitor.scraping.generic_parser import generic_parser
from eventsmonitor.scraping.visit_london_parser import visit_london_parser


logger = logging.getLogger(__name__)


PARSERS = {
    'generic_parser': generic_parser,
    'visit_london_parser': visit_london_parser,
}


def extract_text(html, source):
    """
    Extract text using the configured parser.

    Args:
        html: Raw HTML content as a string.
        source: Single source configuration dictionary containing
            parsing settings.
    Returns:
        str | None: Extracted text if successful,
            otherwise None.
    """
    parser_name = source['parsing']['parser_name']

    parser = PARSERS.get(parser_name)

    if parser is None:
        raise ValueError(
            f'Unknown parser: {parser_name}'
        )

    return parser(html, source)


def scrape_content(config):
    """
    Scrape and extract text content from configured sources.

    Args:
        config: Application configuration object.

    Returns:
        str: Combined extracted text from all sources.
    """
    with open(config.SOURCES_PATH, 'r', encoding='utf-8') as file:
        sources = json.load(file)

    texts = []

    driver = None

    try:
        for source in sources:

            logger.info(
                'Processing source=%s',
                source['name']
            )
            if source['scraping']['requires_selenium']:

                if driver is None:
                    driver = initialise_driver(config)

                html = load_page(driver, source)

            else:
                continue

            if html is None:
                logger.warning(
                    'Skipping source=%s because page did not load',
                    source['name']
                )
                continue
            
            text = extract_text(html, source)

            if text:
                texts.append(text)

    finally:
        if driver is not None:
            quit_driver(driver)

    return ' '.join(texts)