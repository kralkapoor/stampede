import os

from dotenv import load_dotenv
from openai import OpenAI

from handling.exception.configuration_error import ConfigurationError


def create_openai_client():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        raise ConfigurationError("No API key was loaded to the system environment")
    client = OpenAI(
        api_key=OPENAI_API_KEY, organization=os.getenv("OPENAI_ORG_ID"), project=os.getenv("OPENAI_PROJECT_ID")
    )
    return client
