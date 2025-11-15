from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from api.middlewares import UserConfigEnvUpdateMiddleware
from api.v1.webhook.router import API_V1_WEBHOOK_ROUTER
from api.v1.mock.router import API_V1_MOCK_ROUTER
from starlette.staticfiles import StaticFiles
from utils.get_env import get_app_data_directory_env


if os.getenv("DISABLE_LIFESPAN") == "true":
    app = FastAPI()
else:
    from api.lifespan import app_lifespan
    app = FastAPI(lifespan=app_lifespan)


# Routers
app.include_router(API_V1_WEBHOOK_ROUTER)
app.include_router(API_V1_MOCK_ROUTER)
if os.getenv("HEAVY_FEATURES_ENABLED") == "true":
    from api.v1.ppt.router import API_V1_PPT_ROUTER
    app.include_router(API_V1_PPT_ROUTER)

# Middlewares
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(UserConfigEnvUpdateMiddleware)

# Static app data
try:
    os.makedirs(get_app_data_directory_env(), exist_ok=True)
except PermissionError:
    os.environ["APP_DATA_DIRECTORY"] = "/tmp/app_data"
    os.makedirs(get_app_data_directory_env(), exist_ok=True)
app.mount("/app_data", StaticFiles(directory=get_app_data_directory_env()), name="app_data")

# Health endpoint
@app.get("/health")
async def health():
    return {"ok": True}

# Root endpoint
@app.get("/")
async def root():
    frontend_url = os.getenv("FRONTEND_URL")
    frontend_base_url = os.getenv("FRONTEND_BASE_URL")
    frontend_host = os.getenv("FRONTEND_HOST")

    if frontend_url:
        return RedirectResponse(url=f"{frontend_url.rstrip('/')}/dashboard")
    if frontend_base_url:
        return RedirectResponse(url=f"{frontend_base_url.rstrip('/')}/dashboard")
    if frontend_host:
        host = frontend_host.strip()
        if host.startswith("http://") or host.startswith("https://"):
            return RedirectResponse(url=f"{host.rstrip('/')}/dashboard")
        if "." in host:
            return RedirectResponse(url=f"https://{host}/dashboard")
        return RedirectResponse(url=f"https://{host}.onrender.com/dashboard")
    return RedirectResponse(url="https://presenton.ai/dashboard")
