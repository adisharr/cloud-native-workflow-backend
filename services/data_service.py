from datetime import datetime

_data_store = []

def ingest_data(source: str, records: list) -> dict:
    for rec in records:
        normalized = {k.strip().lower(): v for k, v in rec.items()}
        normalized["_source"] = source
        normalized["_ingested_at"] = datetime.utcnow().isoformat()
        _data_store.append(normalized)
    return {"source": source, "records_ingested": len(records), "status": "success"}

def get_records(source: str = None) -> list:
    if source:
        return [r for r in _data_store if r.get("_source") == source]
    return list(_data_store)
