from fastapi import APIRouter
from app.database import get_connection

router = APIRouter()

@router.get("/stats")
async def get_stats():
    conn = get_connection()
    c = conn.cursor()
    
    # Total requests
    c.execute("SELECT COUNT(*) FROM logs")
    total_requests = c.fetchone()[0]
    
    # Success responses (assumed to be 2xx)
    c.execute("SELECT COUNT(*) FROM logs WHERE status_code BETWEEN 200 AND 299")
    success_count = c.fetchone()[0]
    
    # Error responses (status_code >= 400)
    c.execute("SELECT COUNT(*) FROM logs WHERE status_code >= 400")
    error_count = c.fetchone()[0]
    
    # Average response time
    c.execute("SELECT AVG(response_time) FROM logs")
    avg_response_time = c.fetchone()[0] or 0
    
    # Top 5 most commonly accessed endpoints (replace undefined values)
    c.execute('''
        SELECT 
          CASE 
            WHEN path IS NULL OR path = '' OR path = 'undefined' THEN 'Unknown' 
            ELSE path 
          END as endpoint, COUNT(*) as count
        FROM logs
        GROUP BY endpoint
        ORDER BY count DESC
        LIMIT 5
    ''')
    endpoints = [{"endpoint": row[0], "count": row[1]} for row in c.fetchall()]
    
    conn.close()
    return {
        "total_requests": total_requests,
        "success_count": success_count,
        "error_count": error_count,
        "average_response_time": avg_response_time,
        "common_endpoints": endpoints
    }

