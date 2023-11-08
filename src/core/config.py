import os
import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path

from src.helpers.prompts import assemble_chatgpt_model_description


class Settings(BaseSettings):
	DEBUG: bool = False
	ENVIRONMENT: str
	LOG_LEVEL: str = "INFO"

	OPENAPI_TITLE: str = "RoboFast Application"
	OPENAPI_VERSION: str = "v0.1"
	OPENAPI_DESCRIPTION: str = "RoboFast Application"
	BASE_URL: str = "http://testserver"
	OPENAPI_PATH: str = "openapi.yaml"
	DOC_PATH: str = "api/docs"

	NAME_HUMAN: str = "RoboFast Open Source"
	NAME_MODEL: str = "RoboFast"
	DESC_HUMAN: str = "Sample Application to demonstrate Auth0 and Stripe integration"
	DESC_MODEL: str = assemble_chatgpt_model_description()
	PLUGIN_AUTH_TYPE: str = "oauth"
	CONTACT_EMAIL: str = "info@robofastplugin.com"
	# Authentication
	STATE_SECRET_KEY: str  # For SessionMiddleware
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
	AUTH0_DOMAIN: str
	AUTH0_CLIENT_ID: str
	AUTH0_CLIENT_SECRET: str
	AUTH0_API_IDENTIFIER: str
	AUTH0_MGM_CLIENT_ID: str
	AUTH0_MGM_CLIENT_SECRET: str
	CHATGPT_AUTH_TOKEN: str = None  # The code you get after authenticating your app
	AUTH_ALGORITHM: str = "RS256"
	# Stripe
	STRIPE_SECRET_KEY: str

	class Config:
		env_prefix = "APP_"  # values from environment will be read with this prefix
		case_sensitive = True


# load appropriate .env file
env_file = '.env.prod' if os.getenv('ENVIRONMENT') == 'PRODUCTION' else '.env.dev'
env_path = Path(__file__).parent.parent.parent / env_file

load_dotenv(env_path)

settings = Settings()

# Configure the logger
logging.basicConfig(
	level=settings.LOG_LEVEL,
	format="%(asctime)s - %(levelname)s - %(message)s",
	handlers=[
		logging.StreamHandler()
	]
)
logger = logging.getLogger()
