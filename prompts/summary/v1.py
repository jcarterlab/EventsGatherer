"""
Summary prompt version 1.

This prompt is used to identify and summarise events
that may be relevant to the configured entity of concern.
"""

import logging
import textwrap


logger = logging.getLogger(__name__)


PROMPT_NAME = 'summary'
VERSION = 'v1'


def build_summary_prompt(text, config):

    location = config.LOCATION
    entity = config.ENTITY_OF_CONCERN
    threshold = config.IDENTIFICATION_CONFIDENCE_THRESHOLD

    logger.info(
        'Building summary prompt',
        extra={
            'prompt_version': VERSION,
            'prompt_name': PROMPT_NAME,
            'location': location,
            'entity': entity,
            'text_length': len(text),
        }
    )

    instructions = textwrap.dedent(f'''
        You are a highly skilled analyst.

        I'm going to give you scraped article text concerning events in {location}.

        I want you to summarise the events which might be of interest to {entity}.

        Only include events you are at least {threshold}% sure are relevant.

        This is the article text:
    ''').strip()

    formatted_text = f'''<TEXT>\n\n{text}\n\n</TEXT>'''.strip()

    prompt = f'''{instructions}\n\n{formatted_text}'''

    logger.debug(
        'Summary prompt:\n%s', 
        prompt
    )

    return prompt