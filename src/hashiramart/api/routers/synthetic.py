from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import os
import datetime
import random

router = APIRouter(prefix="/synthetic", tags=["Synthetic Data"])

class RecommenderParams(BaseModel):
    num_users: int = 100
    num_products: int = 50
    avg_purchases_per_user: int = 10
    max_purchases_per_user: Optional[int] = 20
    start_date: Optional[str] = "01-01-2024"
    end_date: Optional[str] = "31-12-2024"
    categories: Optional[List[str]] = None
    sparsity: float = 0.9  # fraction of no-purchase
    seed: Optional[int] = 42



class ForecastingParams(BaseModel):
    start_date: str = "01-01-2024"
    end_date: str = "31-12-2024"
    num_products: int = 50
    categories: Optional[List[str]] = None
    holidays: Optional[List[str]] = None
    trend_strength: float = 1.0
    seasonality_strength: float = 1.0
    noise_level: float = 5.0
    promotion_effect: float = 1.5
    promotion_days: Optional[List[str]] = None
    seed: Optional[int] = 42

@router.post("/generate/recommender")
def create_recommender_data(params: RecommenderParams):
    random.seed(params.seed)
    np.random.seed(params.seed)

    # Generate users, products, categories
    users = [f"user_{i}" for i in range(params.num_users)]
    products = [f"product_{i}" for i in range(params.num_products)]

    categories = [f"category_{i % 5}" for i in range(params.num_products)]

    product_categories = dict(zip(products, categories))

    start_date = pd.to_datetime(params.start_date, format='%d-%m-%Y')
    end_date = pd.to_datetime(params.end_date, format='%d-%m-%Y')
    date_range_days = (end_date - start_date).days

    data = []
    for user in users:
        # Number of purchases (bounded by max_purchases_per_user)
        purchases = min(np.random.poisson(params.avg_purchases_per_user), params.max_purchases_per_user or 100)

        # Sparsity: probability to skip purchase event
        for _ in range(purchases):
            if random.random() < params.sparsity:
                continue
            product = np.random.choice(products)
            purchase_date = start_date + pd.Timedelta(days=random.randint(0, date_range_days))
            data.append({
                "user_id": user,
                "product_id": product,
                "category": product_categories[product],
                "purchase_date": purchase_date,
                "quantity": np.random.randint(1, 5)
            })

    df = pd.DataFrame(data)

    # Save synthetic data file
    file_path = "/data/synthetic/recommender_data.parquet"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_parquet(file_path)

    return {"message": "Synthetic recommender data generated", "file": file_path}




@router.post("/generate/forecasting")
def create_forecasting_data(params: ForecastingParams):
    random.seed(params.seed)
    np.random.seed(params.seed)

    # Parse dates with format dd-mm-yyyy
    start_date = pd.to_datetime(params.start_date, format='%d-%m-%Y')
    end_date = pd.to_datetime(params.end_date, format='%d-%m-%Y')

    dates = pd.date_range(start_date, end_date)
    products = [f"product_{i}" for i in range(params.num_products)]

    # Generate synthetic categories
    categories = [f"category_{i % 5}" for i in range(params.num_products)]
    product_categories = dict(zip(products, categories))

    # Generate synthetic holidays - pick 10 random dates as holidays
    holidays = pd.to_datetime(np.random.choice(dates, size=10, replace=False))

    # Generate synthetic promotion days - pick 15 different random dates
    promotion_days = pd.to_datetime(np.random.choice(dates.difference(holidays), size=15, replace=False))

    data = []

    for product in products:
        base = np.random.uniform(50, 150) * params.trend_strength  # base sales multiplier

        # Seasonality: sinusoidal pattern with adjustable strength
        seasonality = params.seasonality_strength * 10 * np.sin(np.linspace(0, 2 * np.pi, len(dates)))

        # Noise
        noise = np.random.normal(0, params.noise_level, len(dates))

        sales = base + seasonality + noise

        for i, date in enumerate(dates):
            sale = sales[i]

            if date in holidays:
                sale *= 2.0  # double sales on holidays

            if date in promotion_days:
                sale *= params.promotion_effect

            sale = max(sale, 0)

            data.append({
                "date": date,
                "product_id": product,
                "category": product_categories[product],
                "sales": sale
            })

    df = pd.DataFrame(data)

    file_path = "/data/synthetic/forecasting_data.parquet"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_parquet(file_path)

    return {"message": "Synthetic forecasting data generated", "file": file_path}

