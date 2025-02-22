from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
import time
from sqlalchemy.orm import Session
from .. import models, schema, utilis
from ..database import get_db

router = APIRouter()


@router.get("/users", response_model=List[schema.UserResp])
async def getUsers(response: Response, db: Session = Depends(get_db)):
    result = db.query(models.User).all()

    if len(result) > 0:

        response.status_code = status.HTTP_200_OK
        return result
        # return {"data": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="zero record found")


@router.post("/users", response_model=schema.UserResp)
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


@router.get("/users/{id}", response_model=schema.UserResp)
async def getUser(id: int, response: Response, db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.id == id).first()

    if result:

        response.status_code = status.HTTP_200_OK
        return result
        # return {"data": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="zero record found")


@router.put("/users/{id}")
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


@router.delete("/users/{id}")
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
