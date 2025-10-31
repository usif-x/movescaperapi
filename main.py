from fastapi import APIRouter, Depends, FastAPI

from app.router import routers

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
