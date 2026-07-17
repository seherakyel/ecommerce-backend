import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI

import models
from database import engine
from routers import cart, orders, products

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Backend")
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)


@app.get("/")
def ana_sayfa():
    return {"mesaj": "Merhaba, backend çalışıyor!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
