from fastapi import FastAPI

from hashiramart.api.routers import auth, users, products, recommendations, forecasting, bigdata_hdfs, synthetic

app = FastAPI(title="HashiraMart AI System")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(recommendations.router)
app.include_router(forecasting.router)
app.include_router(bigdata_hdfs.router)
app.include_router(synthetic.router)