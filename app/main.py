from fastapi import FastAPI
from app.routes.usuario import router as usuario_router
from app.routes.restaurante import router as restaurante_router
from app.routes.review import router as review_router

app = FastAPI()

app.include_router(usuario_router)
app.include_router(restaurante_router)
app.include_router(review_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
