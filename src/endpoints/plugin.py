from fastapi import Request
from fastapi.templating import Jinja2Templates

from src.core.config import settings

plugin_templates = Jinja2Templates(directory="src/templates")


async def healthcheck():
	return {"status": "ok"}


def get_headers_dict(request: Request):
	headers_dict = dict(request.headers)
	return headers_dict


async def ai_plugin_manifest():
	return {
		"schema_version": "v1",
		"name_for_human": settings.NAME_HUMAN,
		"name_for_model": settings.NAME_MODEL,
		"description_for_human": settings.DESC_HUMAN,
		"description_for_model": settings.DESC_MODEL,
		"auth": {
			"type": settings.PLUGIN_AUTH_TYPE,
			"client_url": f'https://{settings.AUTH0_DOMAIN}/authorize',
			"scope": "openid email offline_access",
			"audience": settings.AUTH0_API_IDENTIFIER,
			"authorization_url": f'https://{settings.AUTH0_DOMAIN}/oauth/token',
			"authorization_content_type": "application/json",
			"verification_tokens": {
				"openai": settings.CHATGPT_AUTH_TOKEN
			}
		},
		"api": {
			"type": "openapi",
			"url": f"{settings.BASE_URL}/{settings.OPENAPI_PATH}",
			"is_user_authenticated": True
		},
		"logo_url": f"{settings.BASE_URL}/static/images/logo.png",
		"contact_email": "info@robofastplugin.com",
		"legal_info_url": f"{settings.BASE_URL}/legal"
	}


async def legal(request: Request):
	return plugin_templates.TemplateResponse("legal.html", {"request": request})


async def home_page(request: Request):
	return plugin_templates.TemplateResponse("home.html", {"request": request})
