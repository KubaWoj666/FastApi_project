from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, users, auth, votes, comment

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
app.include_router(comment.router)


@app.get("/")
def firs_rout():
    return {"massage": "Hello world"}




