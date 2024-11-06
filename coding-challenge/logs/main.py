from datetime import datetime

from fastapi import FastAPI, HTTPException

from customer_stats import CustomerStatsProvider
from log_data import LogDataProvider

app = FastAPI()

DB_FILE = 'log_data.db'

@app.get("/customers/{customer_id}/stats")
async def customer_stats(customer_id: int, from_date: str):
    try:
        datetime.strptime(from_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, should be YYYY-MM-DD")

    csp = CustomerStatsProvider(log_provider=LogDataProvider(DB_FILE))

    stats = csp.get_customer_stats(customer_id, from_date)
    if stats is None:
        raise HTTPException(status_code=404, detail="Customer not found or no data available")

    return stats
