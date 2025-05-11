from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoreData(BaseModel):
    score: int

def init_db():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, score INTEGER)")
    conn.commit()
    conn.close()

init_db()

@app.post("/score")
def save_score(data: ScoreData):
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("INSERT INTO scores (score) VALUES (?)", (data.score,))
    conn.commit()
    conn.close()
    return {"message": "Score saved."}

@app.get("/highscore")
def get_highscore():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("SELECT MAX(score) FROM scores")
    result = c.fetchone()[0]
    conn.close()
    return {"highscore": result or 0}