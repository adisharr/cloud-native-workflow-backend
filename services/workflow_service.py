from datetime import datetime

_workflow_store = {}
SUPPORTED_ACTIONS = {"transform", "validate", "notify", "aggregate"}

def execute_workflow(workflow_id: str, steps: list) -> dict:
    results = []
    for i, step in enumerate(steps):
        action = step.get("action", "").lower()
        params = step.get("params", {})
        if action not in SUPPORTED_ACTIONS:
            raise ValueError(f"Unsupported action '{action}' at step {i+1}")
        step_result = _run_step(action, params)
        results.append({"step": i+1, "action": action, "status": "success", "output": step_result})
    record = {
        "workflow_id": workflow_id,
        "status": "completed",
        "steps_executed": len(steps),
        "results": results,
        "executed_at": datetime.utcnow().isoformat()
    }
    _workflow_store[workflow_id] = record
    return record

def get_workflow_status(workflow_id: str) -> dict:
    return _workflow_store.get(workflow_id)

def _run_step(action: str, params: dict) -> dict:
    if action == "transform":
        return {"transformed_fields": list(params.keys()), "rows_affected": params.get("row_count", 0)}
    elif action == "validate":
        return {"validated": True, "rules_applied": params.get("rules", [])}
    elif action == "notify":
        return {"notification_sent": True, "channel": params.get("channel", "email")}
    elif action == "aggregate":
        return {"aggregation": params.get("function", "sum"), "result": 42}
    return {}
