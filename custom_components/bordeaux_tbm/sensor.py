"""TBM sensor platform."""
from datetime import timedelta
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN, CONF_LINE, CONF_STOP, CONF_DIRECTION, CONF_PREDICTIONS, CONF_SCAN_INTERVAL
from .tbm_api import get_next_departures

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigType, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the TBM sensor."""
    coordinator = TBMDataUpdateCoordinator(
        hass,
        entry.data[CONF_LINE],
        entry.data[CONF_STOP],
        entry.data[CONF_DIRECTION],
        entry.data[CONF_PREDICTIONS],
        entry.data[CONF_SCAN_INTERVAL]
    )
    
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([TBMSensor(coordinator)], True)

class TBMDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching TBM data."""

    def __init__(self, hass, line, stop, direction, predictions, scan_interval):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"TBM {line}",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.line = line
        self.stop = stop
        self.direction = direction
        self.predictions = predictions

    async def _async_update_data(self):
        """Update data via API."""
        return await self.hass.async_add_executor_job(
            get_next_departures,
            self.stop,
            self.line,
            self.direction,
            self.predictions
        )

class TBMSensor(CoordinatorEntity, SensorEntity):
    """Representation of a TBM sensor."""

    def __init__(self, coordinator: TBMDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.line}_{coordinator.stop}_{coordinator.direction}"
        self._attr_name = f"TBM {coordinator.line}"
        self.entity_description = SensorEntityDescription(
            key=f"tbm_{coordinator.line}",
            name=f"TBM {coordinator.line}",
            icon="mdi:tram"
        )
        
    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data and len(self.coordinator.data) > 0:
            predictions = []
            for departure in self.coordinator.data:
                delay_str = f"{departure['delay']}min"
                if int(departure['delay']) <= 1:
                    delay_str = "proche"
                predictions.append(f"{departure['destination']} ({delay_str})")
            return "\n".join(predictions)
        return "Aucun passage"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        attributes = {}
        for i, departure in enumerate(self.coordinator.data, 1):
            delay_str = f"{departure['delay']}min"
            if int(departure['delay']) <= 1:
                delay_str = "proche"

            attributes[f"passage_{i}"] = {
                "heure": departure['time'],
                "delai": delay_str,
                "destination": departure['destination']
            }
            attributes[f"passage_{i}_delay_detination"] = {
                f"{departure['destination']} {delay_str}"
            }
        return attributes
