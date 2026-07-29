import os
import sys
import models
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database import engine
from routers import cart, orders, products, auth
from routers import favorites
from routers import addresses

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Backend")
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(auth.router)
app.include_router(favorites.router)
app.include_router(addresses.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home_page():
    return {"mesaj": "Merhaba, backend çalışıyor!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
