from .routers import post, user
from fastapi import FastAPI
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)

# @app.get('/sqlAlchemy')
# def testmycode(db: Session = Depends(get_db)):
#     return {
#         "status": "success"
#     }


@app.get("/")  # decorator /route path
async def root():  # function by default async with any name
    return {"message": "Hello World"}
