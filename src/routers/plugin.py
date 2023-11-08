from fastapi import APIRouter

from src.endpoints.plugin import ai_plugin_manifest, legal, healthcheck, home_page

main_router = APIRouter()

main_router.add_api_route(
	path="/.well-known/ai-plugin.json",
	endpoint=ai_plugin_manifest,
	methods=["GET"],
)

main_router.add_api_route(
	path="/",
	endpoint=home_page,
	methods=["GET"],
	summary='Home page for the app',
	description='Returns a simple HTML page showing app is running',
	operation_id="home_page"
)

main_router.add_api_route(
	path="/healthcheck",
	endpoint=healthcheck,
	methods=["GET"],
	summary='Check if the server is up and running.',
	description='Returns a simple message if the server is up and running.',
	operation_id="healthcheck",
)

main_router.add_api_route(
	path="/legal",
	endpoint=legal,
	methods=["GET"],
	summary='Show legal page',
	description='Show legal page',
	operation_id="legal_page"
)
