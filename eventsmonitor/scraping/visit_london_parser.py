"""
Visit London HTML parsing utilities.

Provides parser functions for extracting structured textual
content from Visit London event pages using BeautifulSoup.

The parser preserves lightweight HTML structure (h2/p tags)
to improve downstream LLM summarisation quality.
"""

import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


# Event extraction begins at the first numbered h2 heading
START_HEADING_PREFIX = '1.'

# Parsing stops when the recommendation section is reached
STOP_HEADING_TEXT = 'You may also like:'

# Used to identify summary panel containers during traversal
SUMMARY_PANEL_CLASS = 'panel-article-summary'

# Adjusts summary panel stopping logic after final event section
SUMMARY_PANEL_OFFSET = 4


def get_h2_count(content_div):
    """
    Count valid section h2 tags (i.e. events).

    Args:
        content_div: BeautifulSoup tag containing the main
            page content.

    Returns:
        int: Number of valid h2 section headings.
    """
    valid_h2s = []

    started = False

    for element in content_div.descendants:

        if not getattr(element, 'name', None):
            continue

        if (
            element.name == 'h2'
            and element.get_text(strip=True).startswith(START_HEADING_PREFIX)
        ):
            started = True

        if started and element.name == 'h2':
            valid_h2s.append(element)

    return len(valid_h2s)


def visit_london_parser(html, _source): 
    """
    Extract structured event text from a Visit London page.

    Removes image-related content, skips introductory text
    and preserves h2/p structure for downstream LLM
    summarisation.

    Args:
        html: Raw HTML content as a string.
        _source: Unused source configuration dictionary.

    Returns:
        str: Structured extracted content containing h2 and
            p tags.
    """
    soup = BeautifulSoup(html, 'html.parser')

    content_div = soup.find('div', class_='cf content-body')

    if not content_div:
        logger.warning('No content div found')
        return None

    # Remove image-related content from extraction
    for tag in content_div.find_all(['figure', 'figcaption']):
        tag.decompose()

    h2_count = get_h2_count(content_div)

    output = []
    summary_panels_seen = 0
    started = False

    for element in content_div.descendants:

        if not getattr(element, 'name', None):
            continue

        # Ignore introductory content before the first event section
        if not started:
            if (
                element.name == 'h2' 
                and element.get_text(strip=True).startswith('1.')
            ):
                started = True
            else:
                continue

        # Stop when recommendation section is reached
        if (
            element.get_text(strip=True) 
            == STOP_HEADING_TEXT
        ):
            break

        classes = element.get('class', [])

        # Stop once final event summary panel is reached
        if (
            element.name == 'div'
            and 'panel' in classes
            and SUMMARY_PANEL_CLASS in classes
        ):
            if summary_panels_seen >= (h2_count - SUMMARY_PANEL_OFFSET):
                break
            else:
                summary_panels_seen += 1
                continue

        if element.name in ['h2', 'p']:

            text = element.get_text(
                ' ', 
                strip=True
            )

            if text:
                output.append(
                    f'<{element.name}>{text}</{element.name}>'
                )

    return '\n'.join(output) 