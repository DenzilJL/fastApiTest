from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
import time
from sqlalchemy.orm import Session
from .. import models, schema, utilis, oauth2
from ..database import get_db

router = APIRouter(prefix='/posts', tags=["Posts Request"])


@router.get("/", response_model=List[schema.PostResp])
async def getPost(response: Response, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    result = db.query(models.Post).limit(limit).all()  # limit query parameter
    result = db.query(models.Post).limit(limit).offset(
        skip).all()  # skip  query parameter

    result = db.query(models.Post).filter(
        # search  query parameter
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    if len(result) > 0:

        response.status_code = status.HTTP_200_OK
        return result
        # return {"data": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="zero record found")


@router.post("/", response_model=schema.PostResp)
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


@router.get("/{id}", response_model=schema.PostResp)
async def getPost(id: int, response: Response, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id).first()

    if result:

        response.status_code = status.HTTP_200_OK
        return result
        # return {"data": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="zero record found")


@router.put("/{id}")
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


# @router.patch("/posts/{id}")
# async def patchUpdatePost(id: int, response: Response):
#     result_post = find_post(id)
#     if result_post:
#         response.status_code = status.HTTP_200_OK
#         return {"data": result_post}
#     # response.status_code = status.HTTP_404_NOT_FOUND
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail="element not found")
#     return {"error": "id not found"}


@router.delete("/{id}")
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
