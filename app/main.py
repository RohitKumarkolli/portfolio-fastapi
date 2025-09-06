from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
import os

app = FastAPI(title="Sunil Kumar Maddela - Portfolio")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Gmail credentials (use environment variables in production)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "yourgmail@gmail.com")  # Gmail account
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_app_password")   # App password

# Pydantic model for contact form
class Contact(BaseModel):
    name: str
    email: str
    message: str

# routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/experience", response_class=HTMLResponse)
async def experience(request: Request):
    return templates.TemplateResponse("experience.html", {"request": request})

@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})

@app.get("/achievements", response_class=HTMLResponse)
async def achievements(request: Request):
    return templates.TemplateResponse("achievements.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.post("/contact")
async def submit_contact(contact: Contact):
    subject = f"New Contact Form Message from {contact.name}"
    body = f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "sunilkumar.iiit862@gmail.com"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return JSONResponse({"status": "success", "message": "Message sent successfully!"})
    except Exception as e:
        return JSONResponse({"status": "error", "message": f"Failed to send message: {str(e)}"})