from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.route import router
from schemas.models import GenericReponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix="/rectangles")


@app.get("/", response_model=GenericReponse)
async def display():
    return GenericReponse(status="Good. Go to /docs")
