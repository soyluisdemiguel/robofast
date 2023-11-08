import jwt
from typing import Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security.oauth2 import OAuth2PasswordBearer
from src.core.config import logger, settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

security = HTTPBearer()


def decode_jwt_token(token: str, auth_domain: str, audience: str) -> Dict[str, Any]:
	jwks_url = f'https://{auth_domain}/.well-known/jwks.json'
	jwks_client = jwt.PyJWKClient(jwks_url)
	header = jwt.get_unverified_header(token)
	key = jwks_client.get_signing_key(header["kid"]).key
	decoded = jwt.decode(token, key, [header["alg"]], audience=audience)
	return decoded


async def get_current_user(authorization: str) -> Dict[str, Any]:
	if not authorization or not authorization.startswith("Bearer "):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

	access_token = authorization[7:]
	try:
		decoded_token = decode_jwt_token(
			token=access_token,
			auth_domain=settings.AUTH0_DOMAIN,
			audience=settings.AUTH0_API_IDENTIFIER
		)
	except jwt.PyJWTError as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}")

	return decoded_token
