import time
from fastapi import APIRouter, Request, HTTPException, Query
from app.database import get_connection
from app.models import LogEntry

router = APIRouter()

@router.post("/log")
async def create_log(log_entry: LogEntry, request: Request):
    """
    Log a new message.
    Validates incoming JSON, inserts a new log into the SQLite database,
    and returns the log ID and response time.
    """
    # Trigger a 500 error if message is "trigger500"
    if log_entry.message == "trigger500":
        _ = 1 / 0  # This will raise ZeroDivisionError resulting in a 500 error

    start_time = time.time()
    body_str = log_entry.json()
    
    conn = get_connection()
    c = conn.cursor()
    # Insert log data with a default status_code of 200
    c.execute('''
        INSERT INTO logs (method, path, request_body, status_code, response_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (request.method, request.url.path, body_str, 200, 0.0))
    log_id = c.lastrowid
    conn.commit()
    conn.close()
    
    response_time = time.time() - start_time
    # Update the response_time for the log entry
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE logs SET response_time = ? WHERE id = ?', (response_time, log_id))
    conn.commit()
    conn.close()
    
    return {"status": "logged", "id": log_id, "response_time": response_time}

@router.get("/logs")
async def get_logs(limit: int = Query(100, description="Max number of logs to return"),
                   status_code: int = Query(None, description="Optional status code to filter by")):
    """
    Retrieve log entries.
    Optionally limit the number of returned logs and filter by status code.
    """
    conn = get_connection()
    c = conn.cursor()
    
    query = "SELECT id, timestamp, method, path, request_body, status_code, response_time FROM logs"
    params = []
    if status_code is not None:
        query += " WHERE status_code = ?"
        params.append(status_code)
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    
    c.execute(query, tuple(params))
    rows = c.fetchall()
    conn.close()
    
    logs = []
    for row in rows:
        logs.append({
            "id": row[0],
            "timestamp": row[1],
            "method": row[2],
            "path": row[3],
            "request_body": row[4],
            "status_code": row[5],
            "response_time": row[6]
        })
    return logs
