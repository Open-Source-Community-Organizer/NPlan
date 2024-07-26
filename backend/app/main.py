import os
import time
import json
import logging
from app.api.api import api_router
from fastapi import FastAPI, Request
from fastapi.middleware import cors

from app.utils.email_handler import MAILTRAP_BEARER_TOKEN
from app.utils.observability import PrometheusMiddleware, metrics, setting_otlp, uvicorn_logger

print(f"MAILTRAP_BEARER_TOKEN: {MAILTRAP_BEARER_TOKEN}") #trying to see what the token is

APP_NAME = os.environ.get("APP_NAME", "backend")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")

app = FastAPI(
    title="NPLAN FastAPI Swagger",
    description="""NPLAN Swagger to test CRUD API endpoints.""",
    root_path="/api/v1",
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    return await Logging_Middleware.log_request(request, call_next)


app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)

app.include_router(api_router)

setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)


class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
