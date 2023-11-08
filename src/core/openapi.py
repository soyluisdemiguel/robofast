from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from src.core.config import Settings

settings = Settings()


def chatgpt_openapi(app: FastAPI) -> dict:
	if app.openapi_schema:
		return app.openapi_schema
	openapi_schema = get_openapi(
		title=settings.OPENAPI_TITLE,
		version=settings.OPENAPI_VERSION,
		description=settings.OPENAPI_DESCRIPTION,
		routes=app.routes,
	)
	openapi_schema["info"]["x-logo"] = {
		"url": "/static/images/logo.png"
	}
	# Add server url
	openapi_schema["servers"] = [
		{
			"url": settings.BASE_URL,
			"description": "Production server",
		}
	]
	app.openapi_schema = openapi_schema
	return app.openapi_schema
