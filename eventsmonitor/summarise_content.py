"""
LLM summarisation module.

Coordinates:
- prompt construction
- LLM requests
- response validation
- retry handling
"""

import logging
import time

from prompts.summary import v1


logger = logging.getLogger(__name__)


def summarise_content(client, text, config):
    """
    Generate a summary using the configured LLM.

    Builds a summary prompt, submits it to the configured
    model, validates the response and retries failed
    requests using exponential backoff.

    Args:
        client: Initialised Gemini API client.
        text: Scraped text to summarise.
        config: Application configuration object.

    Returns:
        str | None: Generated summary text if successful,
            otherwise None.
    """

    retry_attempts = config.LLM_RETRY_ATTEMPTS
    llm_wait_time = config.LLM_WAIT_TIME
    model = config.BASIC_MODEL

    prompt = v1.build_summary_prompt(text, config)

    for attempt in range(1, retry_attempts + 1):

        start_time = time.perf_counter()

        try: 

            response = client.models.generate_content(
                model=model, 
                contents=prompt
            )

            if not response.candidates:
                raise ValueError('No candidates returned')

            response_text = response.text

            summary_text = response_text.strip() if response_text else ''

            if not summary_text:
                raise ValueError('Empty summary text returned')
            
            duration = round(time.perf_counter() - start_time, 2)
            
            logger.info(
                'LLM request completed model=%s duration=%.2fs prompt_words=%d response_words=%d',
                model,
                duration,
                len(prompt.split()),
                len(summary_text.split())
            )
            
            return summary_text

        except Exception:

            if attempt < retry_attempts:

                backoff_time = llm_wait_time * (2 ** (attempt - 1))

                logger.warning(
                    'LLM call failed model=%s attempt=%d/%d retrying_in=%ds',
                    model,
                    attempt,
                    retry_attempts,
                    backoff_time,
                    exc_info=True
                )

                time.sleep(backoff_time)

            else: 

                duration = round(time.perf_counter() - start_time, 2)

                logger.error(
                    'LLM call failed after %d attempts model=%s duration=%.2fs',
                    retry_attempts,
                    model,
                    duration,
                    exc_info=True
                )

                return None