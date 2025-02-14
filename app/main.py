from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import init_db
from app.middleware import LoggingMiddleware
from app.routers import logs, stats

app = FastAPI()

# Initialize the database (creates table if it doesn't exist)
init_db()

# Add the logging middleware to capture all requests (including those causing errors)
app.add_middleware(LoggingMiddleware)

# Mount API routers with the prefix /api
app.include_router(logs.router, prefix="/api")
app.include_router(stats.router, prefix="/api")

# Mount static files and setup templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
