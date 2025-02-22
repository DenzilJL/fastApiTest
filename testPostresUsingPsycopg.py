from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()


while True:
    try:
        dbconn = psycopg2.connect(host='localhost', database="fastApiProject",
                                  user="postgres", password='postgres', cursor_factory=RealDictCursor)
        cursor = dbconn.cursor()
        print("database connected")
        break
    except Exception as error:
        print("connection failed")
        print("exceptionError: ", error)
        time.sleep(4)


class Post (BaseModel):
    title: str
    content: str
    is_published: bool = True


@app.get("/")  # decorator /route path
async def root():  # function by default async with any name
    return {"message": "Hello World"}


@app.get("/posts")
async def getPost(response: Response):
    cursor.execute(""" SELECT * FROM posts """)
    result = cursor.fetchall()
    if len(result) > 0:

        response.status_code = status.HTTP_200_OK
        return {"data": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="zero record found")


@app.post("/posts")
async def createPost(newPost: Post, response: Response):
    cursor.execute(""" INSERT INTO posts (title,content,is_published) values(%s,%s,%s)  returning *""",
                   (newPost.title, newPost.content, newPost.is_published))
    my_post = cursor.fetchone()
    dbconn.commit()
    response.status_code = status.HTTP_201_CREATED

    return {"data": my_post}


@app.get("/posts/{id}")
async def getPost(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts where id = %s""", (str(id)))
    result = cursor.fetchall()
    if len(result) > 0:

        response.status_code = status.HTTP_200_OK
        return {"data": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="zero record found")


@app.put("/posts/{id}")
async def putUpdatePost(id: int, updatedPost: Post, response: Response):
    cursor.execute(
        """ Update posts set title= %s,content=%s,is_published=%s where id = %s  returning *""", (updatedPost.title, updatedPost.content, updatedPost.is_published, str(id)))
    updated_post_record = cursor.fetchone()
    dbconn.commit()
    if updated_post_record:
        response.status_code = status.HTTP_200_OK
        return {"data": updated_post_record}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="element not found")


# @app.patch("/posts/{id}")
# async def patchUpdatePost(id: int, response: Response):
#     result_post = find_post(id)
#     if result_post:
#         response.status_code = status.HTTP_200_OK
#         return {"data": result_post}
#     # response.status_code = status.HTTP_404_NOT_FOUND
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail="element not found")
#     return {"error": "id not found"}


@app.delete("/posts/{id}")
async def deletePost(id: int, response: Response):
    cursor.execute(
        """ delete from posts where id = %s  returning *""", (str(id)))
    delete_post_record = cursor.fetchone()
    dbconn.commit()
    if delete_post_record:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"data": "record deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="element not found")
