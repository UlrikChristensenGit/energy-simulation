import datetime as dt

from calculations.data.integrations.dataset import Dataset
from dashboard.cache import cache


@cache.memoize()
def get_spot_prices(price_area: str):
    spot_prices = Dataset("spot_prices").read()

    start_time = dt.datetime(2024, 6, 1, 0, 0, 0)
    end_time = dt.datetime(2025, 5, 1, 0, 0, 0)

    spot_prices = spot_prices.sel(
        time_utc=slice(start_time, end_time),
        price_area=price_area,
    )

    spot_prices = spot_prices.compute()

    return spot_prices
