from fastapi import FastAPI

from api.routes.manga_routes import router as manga_router
from api.routes.order_routes import router as order_router
from api.routes.user_routes import router as user_router

app = FastAPI(title="MangaBookStore API", version="1.0")

app.include_router(manga_router, prefix="/api", tags=["Manga"])
app.include_router(order_router, prefix="/api", tags=["Orders"])
app.include_router(user_router, prefix="/api", tags=["Users"])

@app.get("/")
def root():
    return {"message": "MangaBookStore API is running"}