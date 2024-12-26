"""Constants for the Bordeaux TBM integration."""
from typing import Final

DOMAIN: Final = "bordeaux_tbm"
PLATFORMS: Final = ["sensor"]

CONF_LINE = "line"
CONF_STOP = "stop"
CONF_DIRECTION = "direction"
CONF_PREDICTIONS = "predictions"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 10
DEFAULT_PREDICTIONS = 3

BASE_URL = "https://bdx.mecatran.com/utw/ws/siri/2.0/bordeaux/"
API_KEY = "opendata-bordeaux-metropole-flux-gtfs-rt"