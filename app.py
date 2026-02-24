from flask import Flask
from config import Config
from logger import setup_logger
from routes.workflow import workflow_bp
from routes.data import data_bp

app = Flask(__name__)
app.config.from_object(Config)
logger = setup_logger()

app.register_blueprint(workflow_bp, url_prefix="/api/workflow")
app.register_blueprint(data_bp, url_prefix="/api/data")

@app.route("/health")
def health():
    logger.info("Health check called")
    return {"status": "ok", "service": "workflow-automation-backend"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
