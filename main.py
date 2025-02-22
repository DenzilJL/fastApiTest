from fastapi import FastAPI
from fastapi.params import *
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    name: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host='localhost', database="fastApiProject",
                                user="postgres", password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connected")
        break
    except Exception as error:
        print("connection failed")
        print("exceptionError: ", error)
        time.sleep(4)

# path operations


@app.get("/")  # decorator /route path
async def root():  # function by default async with any name
    return {"message": "Hello World"}


@app.get("/posts")
async def getPosts():
    cursor.execute(""" SELECT * FROM posts """)
    result = cursor.fetchall()

    return {"message": result}


@app.post("/posts")
async def createPosts(payload: Post):
    return {"message": payload}
