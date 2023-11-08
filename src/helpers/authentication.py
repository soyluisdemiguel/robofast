import httpx
import time

from src.core.config import settings, logger


class Auth0RequestError(Exception):
	"""Custom exception for Auth0 request errors."""


class Auth0UserManagement:
	def __init__(self):
		self.domain = settings.AUTH0_DOMAIN
		self.client_id = settings.AUTH0_MGM_CLIENT_ID
		self.client_secret = settings.AUTH0_MGM_CLIENT_SECRET
		self.token = self._get_management_api_token()

	MAX_RETRIES = 3
	RETRY_DELAY = 1  # seconds

	def _make_request(self, method, url, headers=None, json=None):
		client_error = None  # Variable to store client error

		for i in range(self.MAX_RETRIES):
			try:
				response = httpx.request(method, url, headers=headers, json=json)
				response.raise_for_status()
				return response
			except httpx.HTTPStatusError as e:
				if 400 <= e.response.status_code < 500:
					# For client errors, store the error and break the loop
					client_error = e
					break
				else:
					# For server errors, log the error and retry
					logger.error(f"Server error: {e}. Retrying...")
					time.sleep(self.RETRY_DELAY)
			except httpx.RequestError as e:
				# For request errors, log the error and retry
				logger.error(f"Request failed: {e}. Retrying...")
				time.sleep(self.RETRY_DELAY)
			except Exception as e:
				# For other exceptions, log the error and raise Auth0RequestError
				logger.error(f"Unexpected error: {e}")
				raise Auth0RequestError(f"Failed to make request: {e}")

		if client_error:  # Check if a client error occurred
			logger.error(f"Client error: {client_error}; Status code: {client_error.response.status_code}")
			raise Auth0RequestError(f"Client error: {client_error}")

		logger.error("Max retries reached. Request failed.")
		raise Auth0RequestError("Max retries reached. Request failed.")

	def _get_management_api_token(self):
		url = f"https://{self.domain}/oauth/token"
		headers = {"Content-Type": "application/json"}
		payload = {
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"audience": f"https://{self.domain}/api/v2/",
			"grant_type": "client_credentials"
		}

		response = self._make_request("POST", url, headers=headers, json=payload)
		if response:
			return response.json().get("access_token")
		return None

	def get_user_info(self, user_id):
		url = f"https://{self.domain}/api/v2/users/{user_id}"
		headers = {"Authorization": f"Bearer {self.token}"}
		try:
			response = self._make_request("GET", url, headers=headers)
		except Exception as e:
			raise Auth0RequestError(f"Failed to get user info for user_id: {user_id}. Error: {e}")
		if response:
			return response.json()
		raise Auth0RequestError(f"Failed to get user info for user_id: {user_id}")

	def update_user_metadata(self, user_id, app_metadata=None, user_metadata=None):
		url = f"https://{self.domain}/api/v2/users/{user_id}"
		headers = {
			"Authorization": f"Bearer {self.token}",
			"Content-Type": "application/json"
		}
		payload = {}
		if app_metadata is not None:
			payload["app_metadata"] = app_metadata
		if user_metadata is not None:
			payload["user_metadata"] = user_metadata

		if not payload:
			raise ValueError(f"app_metadata and user_metadata cannot both be None. user_id: {user_id}")

		response = self._make_request("PATCH", url, headers=headers, json=payload)
		if response:
			return response.json()
		raise Auth0RequestError(f"Failed to update user metadata for user_id: {user_id}")

