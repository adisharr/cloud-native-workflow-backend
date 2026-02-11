from datetime import datetime
from app.db import db

class Workflow(db.Model):
    __tablename__ = "workflows"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    steps_json = db.Column(db.Text, nullable=False)  # store list of steps as a JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Run(db.Model):
    __tablename__ = "runs"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="PENDING")  # PENDING/RUNNING/COMPLETED/FAILED
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)

class RunLog(db.Model):
    __tablename__ = "run_logs"

    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey("runs.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
