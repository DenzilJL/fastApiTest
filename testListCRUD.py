from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


def find_post(id):
    found_item = False
    for post in my_post:
        if post['id'] == id:

            return post

    return found_item


def find_index_post(id):
    found_item = False
    for i, post in enumerate(my_post):
        if post['id'] == id:
            return i

    return found_item


class Post (BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_post = [{"title": "title1", "content": "content1", "published": False, "id": 1}, {
    "title": "title2", "content": "content2", "published": True, "id": 2}]


@app.get("/")  # decorator /route path
async def root():  # function by default async with any name
    return {"message": "Hello World"}


@app.get("/posts")
async def getPost():
    return {"data": my_post}


@app.post("/posts")
async def createPost(newPost: Post, response: Response):
    my_post_dict = newPost.dict()
    my_post_dict['id'] = len(my_post) + 1
    my_post.append(my_post_dict)

    response.status_code = status.HTTP_201_CREATED

    return {"data": my_post}


@app.get("/posts/{id}")
async def getPost(id: int, response: Response):
    result_post = find_post(id)
    if result_post:
        response.status_code = status.HTTP_200_OK
        return {"data": result_post}

    # response.status_code = status.HTTP_404_NOT_FOUND
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="element not found")
    # return {"error": "id not found"}


@app.put("/posts/{id}")
async def putUpdatePost(id: int, updatedPost: Post, response: Response):
    index = find_index_post(id)
    if index:
        dict_post = updatedPost.dict()
        dict_post['id'] = id
        my_post[index] = dict_post
        response.status_code = status.HTTP_200_OK
        return {"data": my_post}
    # response.status_code = status.HTTP_404_NOT_FOUND
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="element not found")
    return {"error": "id not found"}


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
    result_post = find_post(id)
    if result_post:
        my_post.remove(result_post)
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"message": "post deleted",
                "data": my_post}
    # response.status_code = status.HTTP_404_NOT_FOUND
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="element not found")
    # return {"error": "id not found"}
