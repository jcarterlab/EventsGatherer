"""
Generic HTML parsing utilities.

Provides parser functions for extracting textual content
from scraped HTML sources using BeautifulSoup.

The generic parser extracts text using configurable CSS
selectors defined in the source configuration.
"""

import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def generic_parser(html, source):
    """
    Extract text content from HTML using a selector-based parser.

    Args:
        html: Raw HTML content as a string.
        source: Single source configuration dictionary containing
            parsing settings.

    Returns:
        str | None: Extracted text content if successful,
            otherwise None.
    """
    soup = BeautifulSoup(html, 'html.parser')

    elements = soup.find_all(source['parsing']['generic_scrape_selector'])

    if not elements:
        logger.warning(
            'No elements found website=%s',
            source['name']
        )
        return None
    
    text = ' '.join(
        element.get_text(separator=' ', strip=True)
        for element in elements
    )

    if not text:
        logger.warning(
            'No text found website=%s',
            source['name']
        )
        return None

    logger.info(
        'Extracted %s words', 
        len(text.split())
    )

    return text