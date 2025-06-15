from fastapi import FastAPI, Depends, HTTPException, status, Request, Cookie, Response, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Annotated, Optional
import os
import jwt
from dotenv import load_dotenv
from jwt import PyJWTError
from models.daily_summary import DailySummary
from datetime import datetime
from fastapi import Body

import models

models.create_db_tables()

app = FastAPI(
    title="MONA (My Own Navigation Assistant) API",
    description="Backend API for tracking routines, goals, thoughts, and emotions.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

users_db = {
    "admin": {"password": "1234", "nickname": "관리자"},
    "test": {"password": "1234", "nickname": "테스터"},
}
emotion_entries = {}
user_data_store = {}
today = datetime.today().date()
now = datetime.now()

class DummyRoutine:
    def __init__(self, title, deadline, is_complete):
        self.title = title
        self.deadline = deadline
        self.is_complete = is_complete

class DummyGoal:
    def __init__(self, title, deadline, progress):
        self.title = title
        self.deadline = deadline
        self.progress = progress

class DummyEmotion:
    def __init__(self, emotion_type, level, date):
        self.emotion_type = emotion_type
        self.level = level
        self.date = date

class DummyThought:
    def __init__(self, content, created_at):
        self.content = content
        self.created_at = created_at

class DummyUser:
    def __init__(self, nickname):
        self.nickname = nickname
        self.username = nickname
        self.routines = []
        self.goals = []
        self.emotions = []
        self.thoughts = []

tester = DummyUser("테스터")
tester.routines = [
    DummyRoutine("아침 운동", today, True),
    DummyRoutine("명상하기", today, False)
]
tester.goals = [
    DummyGoal("기술 블로그 쓰기", today, 0.7)
]
tester.emotions = [
    DummyEmotion("불안", 3, now),
    DummyEmotion("기대", 2, now)
]
tester.thoughts = [
    DummyThought("오늘은 생각이 많았지만 마음을 정리했다.", now)
]

user_data_store["테스터"] = tester
user_data_store["관리자"] = DummyUser("관리자")

def get_user_data_by_nickname(nickname: str):
    user = user_data_store.get(nickname)
    if not user:
        raise ValueError(f"nickname '{nickname}'에 해당하는 사용자 데이터가 없습니다.")
    return user

@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse("/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/token")
async def login_process(
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    user = users_db.get(username)
    if not user or user["password"] != password:
        return HTMLResponse(content='''<script>alert("아이디 또는 비밀번호가 틀렸습니다."); window.location.href='/login';</script>''', status_code=401)

    response = RedirectResponse(url="/home", status_code=302)
    response.set_cookie("username", username)
    return response

@app.post("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("username")
    return response

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, username: str = Cookie(None)):
    if not username or username not in users_db:
        return RedirectResponse("/login")
    nickname = users_db[username]["nickname"]
    user = get_user_data_by_nickname(nickname)

    today = datetime.today().date()
    summary = DailySummary(today, user).generate()

    return templates.TemplateResponse("home.html", {
        "request": request,
        "nickname": nickname,
        "summary_text": summary
    })

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_user(user: dict = Body(...)):
    username = user.get("username")
    password = user.get("password")
    nickname = user.get("nickname")

    if not username or not password or not nickname:
        return JSONResponse(status_code=400, content={"detail": "모든 필드를 입력해주세요."})

    if username in users_db:
        return JSONResponse(status_code=409, content={"detail": "이미 존재하는 아이디입니다."})

    users_db[username] = {"password": password, "nickname": nickname}
    return JSONResponse(status_code=200, content={"message": "회원가입이 완료되었습니다."})

@app.get("/emotions", response_class=HTMLResponse)
async def get_emotions_page(request: Request, username: str = Cookie(None)):
    if username is None or username not in users_db:
        return RedirectResponse(url="/login")

    nickname = users_db[username]["nickname"]
    return templates.TemplateResponse("emotions.html", {"request": request, "nickname": nickname})

@app.get("/emotions/", response_class=JSONResponse)
def get_emotion_entries(username: str = Cookie(None)):
    if username is None or username not in users_db:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    return emotion_entries.get(username, [])

@app.post("/emotions/")
def add_emotion(entry: dict, username: str = Cookie(None)):
    if username is None or username not in users_db:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    entry["date"] = datetime.now().isoformat()
    if username not in emotion_entries:
        emotion_entries[username] = []
    emotion_entries[username].append(entry)
    return {"status": "ok"}

@app.get("/routines", response_class=HTMLResponse)
async def get_routines(request: Request, username: str = Cookie(None)):
    if not username or username not in users_db:
        return RedirectResponse("/login")
    nickname = users_db[username]["nickname"]
    return templates.TemplateResponse("routines.html", {"request": request, "nickname": nickname})

@app.get("/goal", response_class=HTMLResponse)
async def get_goal_page(request: Request, username: str = Cookie(None)):
    if not username or username not in users_db:
        return RedirectResponse("/login")
    nickname = users_db[username]["nickname"]
    return templates.TemplateResponse("goal.html", {"request": request, "nickname": nickname})

@app.get("/thought", response_class=HTMLResponse)
async def get_thought_page(request: Request, username: str = Cookie(None)):
    if not username or username not in users_db:
        return RedirectResponse("/login")
    nickname = users_db[username]["nickname"]
    return templates.TemplateResponse("thought.html", {"request": request, "nickname": nickname})

@app.get("/summary/generate")
async def generate_summary(username: str = Cookie(None)):
    if not username or username not in users_db:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    nickname = users_db[username]["nickname"]
    user = get_user_data_by_nickname(nickname)

    today = datetime.today().date()
    summary_text = DailySummary(today, user).generate()

    return {"summary": summary_text}

@app.get("/theme", response_class=HTMLResponse)
async def theme_setting_page(request: Request, username: str = Cookie(None)):
    if not username or username not in users_db:
        return RedirectResponse("/login")
    nickname = users_db[username]["nickname"]
    return templates.TemplateResponse("theme.html", {"request": request, "nickname": nickname})
