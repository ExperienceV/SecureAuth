from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount('/static', StaticFiles(directory='frontend'), name='static')

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set routers
from routers import home_router
from routers import auth_router

routers_list = [
    home_router.app,
    auth_router.app
]

for router in routers_list:
    app.include_router(router=router)
