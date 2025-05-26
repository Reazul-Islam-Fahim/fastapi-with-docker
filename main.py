from fastapi import FastAPI
from database.db import Base, engine
from routes.auth import registration, login
from fastapi.middleware.cors import CORSMiddleware
from routes.users import users
from routes.categories import categories
from routes.sub_categories import sub_categories
from routes.brands import brands
from routes.vendor import vendors
from routes.bank_details import bank_details
from routes.best_seller import best_seller
from routes.product_features import product_features

from fastapi.staticfiles import StaticFiles

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_models()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/")
def hi():
	return {"hello from" : "pooz store"}

# Mount static directory
app.mount("/resources", StaticFiles(directory="resources"), name="resources")


app.include_router(registration.router)
app.include_router(login.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(sub_categories.router)
app.include_router(brands.router)
app.include_router(vendors.router)
app.include_router(bank_details.router)
app.include_router(best_seller.router)
app.include_router(product_features.router)