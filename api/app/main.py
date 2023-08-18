from app.routers import auth, root, users, category, product

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



def create_application() -> FastAPI:
    application = FastAPI(title="Lateshop", debug=True)
    application.include_router(auth.router)
    application.include_router(users.router)
    application.include_router(category.router)
    application.include_router(product.router)


    application.include_router(root.router)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    application.mount("/static", StaticFiles(directory="app/static"), name="static")

    return application


app = create_application()
