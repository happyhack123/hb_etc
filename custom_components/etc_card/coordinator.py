import requests
import re
import json
import time
from datetime import datetime

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .const import UPDATE_INTERVAL

class ETCCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, card_no: str):
        super().__init__(
            hass,
            logger=None,
            name="ETC Coordinator",
            update_interval=UPDATE_INTERVAL,
        )
        self.card_no = card_no

    async def _async_update_data(self):
        return await self.hass.async_add_executor_job(self._fetch_data)

    def _fetch_data(self):
        try:
            status = self.get_card_status()
            bill = self.get_bill(status)
            return bill
        except Exception as err:
            raise UpdateFailed(err)

    def get_card_status(self):
        response = requests.get(
            "https://www.02712122.com/HBGSWechatAPIServer/index.php/rechargetest/etcserver/cardblackForMiniProgram",
            params={"cardno": self.card_no},
            timeout=10,
        )
        return re.findall('span id="blackType">(.*?)</span>', response.text)[0]

    def get_bill(self, card_status):
        response = requests.post(
            "https://www.02712122.com/HBGSWechatAPIServer/index.php/BillApi/billHome",
            data={
                "cardNo": self.card_no,
                "startDate": datetime.now().strftime("%Y-%m"),
                "endDate": datetime.now().strftime("%Y-%m"),
                "flag": "0",
                "pageNum": "1",
                "pageSize": "999",
            },
            timeout=10,
        )

        data = response.json()
        data["cardNo"] = self.card_no
        data["is_black_card"] = card_status
        data["Act_time"] = time.strftime("%Y-%m-%d %H:%M:%S")

        return self._remove_yen(data)

    def _remove_yen(self, data):
        json_str = json.dumps(data, ensure_ascii=False).replace("¥", "")
        return json.loads(json_str)


