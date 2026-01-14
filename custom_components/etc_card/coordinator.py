from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

class ETCCoordinator(DataUpdateCoordinator):
    async def _async_update_data(self):
        # TODO: replace with real request
        return {
            "fee": 123.45,
            "count": 6,
            "black": False
        }
