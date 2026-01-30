from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, users
from .database import engine
from .models.user import User, Course, Class, Lecture, Attendance, Certification

app = FastAPI(title="STG Academy API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "STG Academy API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
