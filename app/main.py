from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.routes import routers as v1_routers
from app.core.config import configs
from app.core.container import Container
from app.util.designpatterns import singleton


@singleton
class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            openapi_url=f"{configs.API}/openapi.json",
            version="0.0.1",
        )

        # set db and container
        self.container = Container()
        self.db = self.container.db()
        # self.db.create_database()

        # set cors
        if configs.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"

        self.app.include_router(v1_routers, prefix=configs.API_V1_STR)


app_creator = AppCreator()
app = app_creator.app
db = app_creator.db
container = app_creator.container
def create_app():
    _app = FastAPI(
        title=configs.PROJECT_NAME,
        docs_url=f"{configs.API_PREFIX}/docs",
        redoc_url=f"{configs.API_PREFIX}/redoc",
        openapi_url=f"{configs.API_PREFIX}/openapi.json",
        version="0.0.1",
    )

    # set db and container
    container = Container()
    _app.container = container
    _app.db = container.db()

    # set cors
    if configs.BACKEND_CORS_ORIGINS:
        _app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @_app.exception_handler(CustomHttpException)
    async def http_exception_handler(
        request: Request,  # Don't remove it because it is used internally.
        exc: CustomHttpException,
    ) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"title": exc.title, "description": exc.description})

    # set routes
    @_app.get(f"{configs.API_PREFIX}/healthcheck", status_code=status.HTTP_200_OK)
    def healthcheck():
        return {"status": "OK"}

    @_app.get("/", status_code=status.HTTP_200_OK)
    def root():
        return {"status": "OK"}

    _app.include_router(v1_router, prefix=configs.API_V1_PREFIX)
    logger.info(f"app created. Its ENV_NAME: {configs.ENV}")
    return _app


app = create_app()
