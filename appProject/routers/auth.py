from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schema, oauth2
from ..database import get_db
from ..utilis import passwordHash, passwordVerify

router = APIRouter(prefix='/auth', tags=["Auth Request"])


@router.post("/login")
# async def loginUser(userCredential: schema.UserLogin, response: Response, db: Session = Depends(get_db)):
async def loginUser(response: Response, userCredential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # contains only username,password
    # result = db.query(models.User).filter(
    #     models.User.email == userCredential.email).first()
    result = db.query(models.User).filter(
        models.User.email == userCredential.username).first()
    if result:
        if passwordVerify(userCredential.password, result.password):
            access_token = oauth2.create_access_token(
                data={"user_id": result.id})
            response.status_code = status.HTTP_202_ACCEPTED
            return {"token": access_token}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credential")

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credential")
