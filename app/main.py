from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, likes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(CORS)


@app.get("/")
# Decorator @ with get request for our app/ HTTP request methods and (/) root path
# Function &
def root():

    # Data for the user
    return {"message": "Welcome to my API"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(likes.router)
