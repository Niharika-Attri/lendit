from fastapi import FastAPI
from app.api.item import router as items_router
from app.api.user import router as users_router
from app.api.auth import router as auth_router

app = FastAPI(title="Lendit")

# Include routers
app.include_router(items_router)
app.include_router(users_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Welcome to Lendit"}