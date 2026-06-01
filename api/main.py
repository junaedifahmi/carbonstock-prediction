from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import APP_NAME, APP_VERSION, APP_DESCRIPTION
from models import Engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.engine = Engine()

    yield

    # Shutdown
    # app.state.engine.close()  # if needed


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
)


@app.get("/")
async def health_check():
    return {"service": app.title}


@app.post("/predict")
async def predict():
    engine = app.state.engine

    result = await engine.ainvoke()
    return {"result": result}
