"""Main file for project.

Description:
- This program is main file for project.
- It is used to create FastAPI object and add all routes to it.

"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles

from fastapi_boilerplate.apps.route import router
from fastapi_boilerplate.core.config import settings
from fastapi_boilerplate.core.helper import custom_generate_unique_id
from fastapi_boilerplate.middleware.exception_handling import (
    exception_handling,
)


# Application Lifespan Manager
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager.

    :Description:
    - This function manages application lifecycle.
    - Creates database tables on startup.

    :Args:
    - `app` (FastAPI): FastAPI application instance.

    :Yields:
    - Application runtime.

    """
    yield


# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_TITLE,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
)


# Add Static Files
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")


# Add CORS Middleware
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_methods=settings.BACKEND_CORS_METHODS,
    allow_headers=settings.BACKEND_CORS_HEADERS,
    allow_credentials=True,
)

# Custom http middleware
app.middleware(middleware_type="http")(exception_handling)


# Custom Exception Handler for RequestValidationError
@app.exception_handler(exc_class_or_status_code=RequestValidationError)
async def validation_exception_handler(
    _: Request, err: RequestValidationError
) -> ORJSONResponse:
    """Handle FastAPI request validation errors."""
    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "data": None,
            "error": [
                {
                    "field": error.get("loc", ["unknown"])[-1],
                    "message": error.get("msg", "Invalid input"),
                    "input": error.get("input", None),
                }
                for error in err.errors()
            ],
        },
    )


# Custom Exception Handler for HTTPException
@app.exception_handler(exc_class_or_status_code=HTTPException)
async def http_exception_handler(
    _: Request, err: HTTPException
) -> ORJSONResponse:
    """Handle FastAPI HTTP exceptions."""
    return ORJSONResponse(
        status_code=err.status_code,
        content={
            "success": False,
            "message": err.detail,
            "data": None,
            "error": str(err),
        },
    )


# Root Route
@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Home page",
    response_description="Home page",
    tags=["Root"],
)
async def root() -> dict[str, str]:
    """Root Route.

    :Description:
    - This function is used to create root route.

    :Args:
    - `None`

    :Returns:
    - `dict[str, str]`: Welcome message.

    """
    return {"detail": f"Welcome to {settings.PROJECT_TITLE}"}


# Custom Swagger Route
@app.get(
    path=f"{settings.DOCS_URL}",
    status_code=status.HTTP_200_OK,
    summary="Swagger UI",
    description="This is Swagger UI.",
    response_description="Swagger UI",
    include_in_schema=False,
    tags=["Documentation"],
)
async def custom_swagger_ui_html() -> HTMLResponse:
    """Custom Swagger UI HTML.

    :Description:
    - This function is used to create a custom swagger UI HTML page.

    :Args:
    - `None`

    :Returns:
    - `HTMLResponse`: Swagger UI HTML page.

    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "",
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    )


# Custom Redoc Route
@app.get(
    path=f"{settings.REDOC_URL}",
    status_code=status.HTTP_200_OK,
    summary="Redoc UI",
    description="This is Redoc UI.",
    response_description="Redoc UI",
    include_in_schema=False,
    tags=["Documentation"],
)
async def custom_redoc_ui_html() -> HTMLResponse:
    """Custom Redoc UI HTML.

    :Description:
    - This function is used to create a custom redoc UI HTML page.

    :Args:
    - `None`

    :Returns:
    - `HTMLResponse`: Redoc UI HTML page.

    """
    return get_redoc_html(
        openapi_url=app.openapi_url or "",
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


# Add all file routes to app
app.include_router(router=router)
