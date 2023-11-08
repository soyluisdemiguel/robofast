from typing import Any, Dict
import httpx
from src.core.config import settings
from fastapi import Request, HTTPException, Query, status, Response
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from jose import jwk, jwt


def get_chatgpt_headers(request: Request):
	headers_dict = dict(request.headers)
	return headers_dict


async def decode_access_token(access_token: str):
	try:
		async with httpx.AsyncClient() as client:
			resp = await client.get(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
			resp.raise_for_status()
			jwks = resp.json()
	except httpx.RequestError as exc:
		# Connection error
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
			detail=f"Authentication service not available: {str(exc)}"
		)
	except httpx.HTTPStatusError as exc:
		# Invalid response from server
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=f"Bad response from authentication service: {str(exc)}"
		)

	try:
		header = jwt.get_unverified_header(access_token)
	except jwt.JWTError as exc:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"Failed to decode token header: {str(exc)}"
		)

	rsa_key = {}
	for key in jwks.get("keys", []):
		if key.get("kid") == header.get("kid"):
			rsa_key = {
				"kty": key.get("kty"),
				"kid": key.get("kid"),
				"use": key.get("use"),
				"alg": key.get("alg"),
				"n": key.get("n"),
				"e": key.get("e"),
			}
			break

	if not rsa_key:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Could not find the appropriate key to decode the token."
		)

	key = jwk.construct(rsa_key)
	pem_key = key.to_pem().decode('utf-8')

	try:
		payload = jwt.decode(
			access_token,
			pem_key,
			algorithms=["RS256"],
			audience=settings.AUTH0_API_IDENTIFIER,
			issuer=f"https://{settings.AUTH0_DOMAIN}/",
		)
	except jwt.JWTError as exc:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"Failed to decode token: {str(exc)}"
		)

	return payload


async def get_token_data(authorization: str) -> Dict[str, Any]:
	"""
	Dependency to extract and validate the current user from the Bearer token.
	"""
	if not authorization.startswith("Bearer "):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

	access_token = authorization[7:]

	try:
		decoded_payload = await decode_access_token(access_token)  # Add await here
		return decoded_payload
	except HTTPException as exc:
		# Re-raise the HTTPException from decode_access_token
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
	except Exception as exc:
		# Catch any other exceptions
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(exc)}")


def get_user_status(decoded_payload: Dict[str, Any]) -> str:
	"""
	Dummy function to get user status. Replace with your actual logic.
	"""
	# For demonstration, we assume the user is "active" if the 'sub' field exists
	return "active" if decoded_payload.get("sub") else "inactive"
