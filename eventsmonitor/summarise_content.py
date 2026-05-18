import logging
import time


# ----------------------------------------------------------------------
# LOGGING SETUP
# ----------------------------------------------------------------------

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# PROMPT FUNCTIONS
# ----------------------------------------------------------------------

def build_events_text_summarisation_prompt(text, config):

    location = config.LOCATION
    entity = config.ENTITY_OF_CONCERN
    threshold = config.IDENTIFICATION_CONFIDENCE_THRESHOLD

    return f'''
    You are a highly skilled analyst. 

    I'm going to give you scraped article text concerning events in {location}.
    I want you summarise the events which might be of interest to {entity}. 

    Only include events you are at least {threshold}% sure are relevant. 
        
    This is the article text: 

    <TEXT>
    {text}
    </TEXT>
    '''


# ----------------------------------------------------------------------
# ORCHESTRATION FUNCTIONS
# ----------------------------------------------------------------------

def summarise_content(client, text, config):

    retry_attempts = config.LLM_RETRY_ATTEMPTS
    llm_wait_time = config.LLM_WAIT_TIME
    basic_model = config.BASIC_MODEL

    prompt = build_events_text_summarisation_prompt(text, config)

    response = client.models.generate_content(
        model=basic_model, 
        contents=prompt
    )

    response_text = response.text

    summary_text = response_text.strip() if response_text else ''

    if not summary_text:
        raise ValueError('Empty summary text returned')
    
    return summary_text
