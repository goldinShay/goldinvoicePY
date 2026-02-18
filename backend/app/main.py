from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.api import contacts, invoices, auth

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.include_router(contacts.router)
app.include_router(invoices.router)
app.include_router(auth.router)

@app.get("/", response_class=HTMLResponse)
def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})
