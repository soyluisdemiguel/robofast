from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.routers.plugin import main_router
from src.routers.payment import payment_router
from src.core.openapi import chatgpt_openapi
from src.core.config import settings, logger

origins = [
	["*"],
]

app = FastAPI(
	title=settings.OPENAPI_TITLE,
	description=settings.OPENAPI_DESCRIPTION,
	version=settings.OPENAPI_VERSION,
	openapi_url=f"/{settings.OPENAPI_PATH}",
	docs_url=f"/{settings.DOC_PATH}",
	debug=settings.DEBUG,
)

logger.info("Creating routers")
app.include_router(main_router, prefix="")
app.include_router(payment_router)

logger.info("Mounting static files")
app.mount("/static", StaticFiles(directory="static"), name="static")

logger.info("Overriding openapi generator")
app.openapi = lambda: chatgpt_openapi(app)

logger.info("Adding Session middleware")
app.add_middleware(SessionMiddleware, secret_key=settings.STATE_SECRET_KEY)

logger.info("Adding CORS middleware")
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
logger.info("FastAPI application created and configured")
