from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.core.config import APP_NAME, FRONTEND_URL

from app.user.user_api import router as user_router
from app.driver.driver_api import router as driver_router
from app.ride.ride_api import router as ride_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME)

# ✅ CORS from ENV
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(driver_router, prefix="/api/drivers", tags=["Drivers"])
app.include_router(ride_router, prefix="/api/rides", tags=["Rides"])
