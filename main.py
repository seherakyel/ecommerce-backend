from fastapi import FastAPI
import models
from database import engine
from routers import products

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(products.router)

@app.get("/")
def ana_sayfa():
    return {"mesaj": "Merhaba, backend çalışıyor!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)