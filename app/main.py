from fastapi import FastAPI
from app.routers import intake
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set API endpoints on router
app.include_router(intake.router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)


