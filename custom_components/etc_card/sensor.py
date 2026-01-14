from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ETCFeeSensor(coordinator),
        ETCCountSensor(coordinator),
        ETCBlackSensor(coordinator),
    ])

class ETCFeeSensor(CoordinatorEntity, SensorEntity):
    name = "ETC 本月费用"
    icon = "mdi:truck-off-road"
    native_unit_of_measurement = "¥"

    @property
    def native_value(self):
        return self.coordinator.data["fee"]

class ETCCountSensor(CoordinatorEntity, SensorEntity):
    name = "ETC 本月次数"
    icon = "mdi:truck-off-road"

    @property
    def native_value(self):
        return self.coordinator.data["count"]

class ETCBlackSensor(CoordinatorEntity, SensorEntity):
    name = "ETC 黑名单状态"
    icon = "mdi:truck-off-road"

    @property
    def native_value(self):
        return "黑名单" if self.coordinator.data["black"] else "正常"

    @property
    def extra_state_attributes(self):
        return {
            "is_black": self.coordinator.data["black"]
        }
