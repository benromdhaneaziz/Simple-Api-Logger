import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.database import get_connection

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        # Read and store the body so it can be logged and replayed
        body_bytes = await request.body()
        request_body = body_bytes.decode("utf-8") if body_bytes else ""
        
        # Reassign the request's receive method so the downstream handler can read the body again
        async def receive():
            return {"type": "http.request", "body": body_bytes}
        request._receive = receive

        try:
            response = await call_next(request)
        except Exception as exc:
            process_time = time.time() - start_time
            # Log the request with a status code of 500 if an exception occurs
            self.log_request(request, request_body, 500, process_time)
            raise exc  # Re-raise so FastAPI returns a 500 error
        else:
            process_time = time.time() - start_time
            self.log_request(request, request_body, response.status_code, process_time)
            return response

    def log_request(self, request: Request, request_body: str, status_code: int, process_time: float):
        conn = get_connection()
        try:
            c = conn.cursor()
            c.execute(
                "INSERT INTO logs (method, path, request_body, status_code, response_time) VALUES (?, ?, ?, ?, ?)",
                (request.method, str(request.url), request_body, status_code, process_time)
            )
            conn.commit()
        finally:
            conn.close()
