import json
import time
from datetime import datetime
from flask import Flask, request, jsonify

from app.db import db
from app.models import Workflow, Run, RunLog

def create_app() -> Flask:
    app = Flask(__name__)

    # SQLite DB in the project root (created automatically)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workflow.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Create tables on first run
    with app.app_context():
        db.create_all()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/workflows")
    def create_workflow():
        data = request.get_json(silent=True) or {}
        name = data.get("name")
        steps = data.get("steps")

        if not name or not isinstance(steps, list) or len(steps) == 0:
            return jsonify({"error": "Provide: name (string), steps (non-empty list)"}), 400

        wf = Workflow(name=name, steps_json=json.dumps(steps))
        db.session.add(wf)
        db.session.commit()

        return jsonify({"id": wf.id, "name": wf.name, "steps": steps}), 201

    @app.get("/workflows")
    def list_workflows():
        workflows = Workflow.query.order_by(Workflow.created_at.desc()).all()
        out = []
        for wf in workflows:
            out.append({
                "id": wf.id,
                "name": wf.name,
                "steps": json.loads(wf.steps_json),
                "created_at": wf.created_at.isoformat() + "Z"
            })
        return jsonify(out), 200

    @app.post("/workflows/<int:wf_id>/run")
    def run_workflow(wf_id: int):
        wf = Workflow.query.get(wf_id)
        if not wf:
            return jsonify({"error": "Workflow not found"}), 404

        run = Run(workflow_id=wf.id, status="RUNNING")
        db.session.add(run)
        db.session.commit()

        steps = json.loads(wf.steps_json)

        try:
            for i, step in enumerate(steps, start=1):
                db.session.add(RunLog(run_id=run.id, message=f"Step {i}/{len(steps)}: {step} - started"))
                db.session.commit()

                # Simulate work
                time.sleep(0.2)

                db.session.add(RunLog(run_id=run.id, message=f"Step {i}/{len(steps)}: {step} - completed"))
                db.session.commit()

            run.status = "COMPLETED"
            run.finished_at = datetime.utcnow()
            db.session.commit()

        except Exception as e:
            run.status = "FAILED"
            run.finished_at = datetime.utcnow()
            db.session.add(RunLog(run_id=run.id, message=f"ERROR: {str(e)}"))
            db.session.commit()

        return jsonify({"run_id": run.id, "status": run.status}), 200

    @app.get("/runs/<int:run_id>")
    def get_run(run_id: int):
        run = Run.query.get(run_id)
        if not run:
            return jsonify({"error": "Run not found"}), 404

        logs = RunLog.query.filter_by(run_id=run.id).order_by(RunLog.created_at.asc()).all()

        return jsonify({
            "run_id": run.id,
            "workflow_id": run.workflow_id,
            "status": run.status,
            "started_at": run.started_at.isoformat() + "Z",
            "finished_at": (run.finished_at.isoformat() + "Z") if run.finished_at else None,
            "logs": [{"time": l.created_at.isoformat() + "Z", "message": l.message} for l in logs]
        }), 200

    return app

app = create_app()

if __name__ == "__main__":
    # For local dev
    app.run(host="0.0.0.0", port=5000, debug=True)
