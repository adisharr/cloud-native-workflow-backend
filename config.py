import os

class Config:
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = False
    MAX_PAYLOAD_SIZE = 1024 * 1024
    SERVICE_NAME = "workflow-automation-backend"
    VERSION = "1.0.0"
