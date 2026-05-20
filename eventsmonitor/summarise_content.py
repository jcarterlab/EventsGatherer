import logging

import time

from prompts.summary import v1


logger = logging.getLogger(__name__)


def summarise_content(client, text, config):

    retry_attempts = config.LLM_RETRY_ATTEMPTS
    llm_wait_time = config.LLM_WAIT_TIME
    basic_model = config.BASIC_MODEL

    prompt = v1.build_summary_prompt(text, config)

    response = client.models.generate_content(
        model=basic_model, 
        contents=prompt
    )

    response_text = response.text

    summary_text = response_text.strip() if response_text else ''

    if not summary_text:
        raise ValueError('Empty summary text returned')
    
    return summary_text
