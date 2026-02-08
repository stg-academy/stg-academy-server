from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, user, course, session, lecture, attendance, certification, enroll
from .database import engine
from .models.user import User, Course, Session, Lecture, Attendance, Certification

app = FastAPI(title="STG Academy API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(course.router)
app.include_router(session.router)
app.include_router(lecture.router)
app.include_router(attendance.router)
app.include_router(certification.router)
app.include_router(enroll.router)

@app.get("/")
async def root():
    return {"message": "STG Academy API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
