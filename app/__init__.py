from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router



origins = [
    "http://localhost:5173",
    "https://exp-frontend-flame.vercel.app" 
    ]

def create_app() -> FastAPI:
    app = FastAPI()
    #cors
    app.add_middleware(
        CORSMiddleware, 
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"]
    )
    # routes
    app.include_router(router)


    return app


