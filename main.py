"""Main file for project.

Description:
- This program is main file for project.
- It is used to create FastAPI object and add all routes to it.

"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi_boilerplate.core.config import settings
from fastapi_boilerplate.core.helper import custom_generate_unique_id

app = FastAPI(
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    generate_unique_id_function=custom_generate_unique_id,
    title=settings.PROJECT_TITLE,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION,
)

# Add Static Files
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_methods=settings.BACKEND_CORS_METHODS,
    allow_headers=settings.BACKEND_CORS_HEADERS,
    allow_credentials=True,
)


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
    - `None`

    """
    return {"detail": f"Welcome to {settings.PROJECT_TITLE}"}


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
    - `swagger_ui_html` (HTMLResponse): Swagger UI HTML page.

    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "",
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    )


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
    - `redoc_ui_html` (HTMLResponse): Redoc UI HTML page.

    """
    return get_redoc_html(
        openapi_url=app.openapi_url or "",
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )
