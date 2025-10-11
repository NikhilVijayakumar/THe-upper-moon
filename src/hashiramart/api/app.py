from fastapi import FastAPI

from hashiramart.api.routers import auth, users, products, recommendations, forecasting, data_cleaning

app = FastAPI(title="HashiraMart AI System")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(recommendations.router)
app.include_router(forecasting.router)
app.include_router(data_cleaning.router)