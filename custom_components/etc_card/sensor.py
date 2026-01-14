from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SENSORS = {
    "total_fee": "本月 ETC 费用",
    "total_num": "本月 ETC 次数",
    "black_status": "ETC 黑名单状态",
}

class ETCSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:truck-off-road"

    def __init__(self, coordinator, key, name):
        super().__init__(coordinator)
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.card_no}_{key}"

    @property
    def native_value(self):
        data = self.coordinator.data

        if self.key == "total_fee":
            return data["data"]["total_data"]["total_fee"]
        if self.key == "total_num":
            return data["data"]["total_data"]["total_num"]
        if self.key == "black_status":
            return data["is_black_card"]

    @property
    def extra_state_attributes(self):
        if self.key == "black_status":
            return {
                "color": "red" if "该卡被列入黑名单中" in self.native_value else "green"
            }
        return {}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ETCSensor(coordinator, key, name)
        for key, name in SENSORS.items()
    )
