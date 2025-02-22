from fastapi import FastAPI, Response, status, HTTPException, Depends

from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schema, utilis
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get('/sqlAlchemy')
def testmycode(db: Session = Depends(get_db)):
    return {
        "status": "success"
    }


@app.get("/")  # decorator /route path
async def root():  # function by default async with any name
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schema.PostResp])
async def getPost(response: Response, db: Session = Depends(get_db)):
    result = db.query(models.Post).all()

    if len(result) > 0:

        response.status_code = status.HTTP_200_OK
        return result
        # return {"data": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="zero record found")


@app.post("/posts", response_model=schema.PostResp)
async def createPost(newPost: schema.Post, response: Response, db: Session = Depends(get_db)):
    inserted_post = models.Post(**newPost.dict())
    '''inserted_post = models.Post(
        title=newPost.title, description=newPost.description, published=newPost.published)'''
    db.add(inserted_post)
    db.commit()
    db.refresh(inserted_post)
    response.status_code = status.HTTP_201_CREATED
    return inserted_post
    # return {"data": inserted_post}


@app.get("/posts/{id}", response_model=schema.PostResp)
async def getPost(id: int, response: Response, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id).first()

    if result:

        response.status_code = status.HTTP_200_OK
        return result
        # return {"data": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="zero record found")


@app.put("/posts/{id}")
async def putUpdatePost(id: int, updatedPost: schema.Post, response: Response, db: Session = Depends(get_db)):
    updated_post_record = db.query(models.Post).filter(
        models.Post.id == id)
    update_post_record = updated_post_record.first()
    if update_post_record:
        updated_post_record.update(
            updatedPost.dict(), synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_200_OK
        return {"data": "updated_post_record"}
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
async def deletePost(id: int, response: Response, db: Session = Depends(get_db)):
    delete_post_record = db.query(models.Post).filter(models.Post.id == id)
    if delete_post_record.first():
        # delete_post_record.delete()
        delete_post_record.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"data": "record deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="element not found")

# Users CRUD


@app.get("/users", response_model=List[schema.UserResp])
async def getUsers(response: Response, db: Session = Depends(get_db)):
    result = db.query(models.User).all()

    if len(result) > 0:

        response.status_code = status.HTTP_200_OK
        return result
        # return {"data": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="zero record found")


@app.post("/users", response_model=schema.UserResp)
async def createUser(newUser: schema.User, response: Response, db: Session = Depends(get_db)):
    # Hash password
    newUser.password = utilis.passwordHash(newUser.password)
    inserted_user = models.User(**newUser.dict())
    '''inserted_user = models.User(
        title=newUser.title, description=newUser.description, published=newUser.published)'''
    db.add(inserted_user)
    db.commit()
    db.refresh(inserted_user)
    response.status_code = status.HTTP_201_CREATED
    return inserted_user
    # return {"data": inserted_post}


@app.get("/users/{id}", response_model=schema.UserResp)
async def getUser(id: int, response: Response, db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.id == id).first()

    if result:

        response.status_code = status.HTTP_200_OK
        return result
        # return {"data": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="zero record found")


@app.put("/users/{id}")
async def putUpdateUser(id: int, updatedUser: schema.User, response: Response, db: Session = Depends(get_db)):
    updated_user_record = db.query(models.User).filter(
        models.User.id == id)
    update_user_record = updated_user_record.first()
    if update_user_record:
        updated_user_record.update(
            updatedUser.dict(), synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_200_OK
        return {"data": "updated_post_record"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="element not found")


@app.delete("/users/{id}")
async def deleteUser(id: int, response: Response, db: Session = Depends(get_db)):
    delete_user_record = db.query(models.User).filter(models.User.id == id)
    if delete_user_record.first():
        # delete_user_record.delete()
        delete_user_record.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"data": "record deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="element not found")
