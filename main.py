from backend.database import engine, Base
from backend.routes import login,user,patients,doctor
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="CLINIC MANAGEMENT SYSTEM")

app.mount("/web", StaticFiles(directory="web"), name="web")
templates = Jinja2Templates(directory="web")

@app.get("/", response_class=HTMLResponse)
async def start(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

Base.metadata.create_all(bind=engine)

app.include_router(login.router)
app.include_router(user.router)
app.include_router(patients.router)
app.include_router(doctor.router)