import logging
from bs4 import BeautifulSoup


# ----------------------------------------------------------------------
# LOGGING SETUP
# ----------------------------------------------------------------------

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------

def get_h2_count(content_div):
    valid_h2s = []

    started = False

    for element in content_div.descendants:

        if not getattr(element, 'name', None):
            continue

        if (
            element.name == 'h2'
            and element.get_text(strip=True).startswith('1.')
        ):
            started = True

        if started and element.name == 'h2':
            valid_h2s.append(element)

    return len(valid_h2s)

    
# ----------------------------------------------------------------------
# ORCHESTRATION FUNCTIONS
# ----------------------------------------------------------------------

def visit_london_parser(html): 
    soup = BeautifulSoup(html, 'html.parser')

    content_div = soup.find('div', class_='cf content-body')

    for tag in content_div.find_all(['figure', 'figcaption']):
        tag.decompose()

    h2_count = get_h2_count(content_div)

    output = []
    summary_panels_seen = 0
    started = False

    for element in content_div.descendants:

        if not getattr(element, 'name', None):
            continue

        if not started:
            if (
                element.name == 'h2' 
                and element.get_text(strip=True).startswith('1.')
            ):
                started = True
            else:
                continue

        if element.get_text(strip=True) == 'You may also like:':
            break

        classes = element.get('class', [])

        if (
            element.name == 'div'
            and 'panel' in classes
            and 'panel-article-summary' in classes
        ):
            if summary_panels_seen >= (h2_count - 4):
                break
            else:
                summary_panels_seen += 1
                continue

        if element.name in ['h2', 'p']:

            text = element.get_text(' ', strip=True)

            if text:
                output.append(f'<{element.name}>{text}</{element.name}>')

    return '\n'.join(output) 