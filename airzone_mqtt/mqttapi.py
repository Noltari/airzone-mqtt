"""Airzone MQTT API."""

from collections.abc import Callable
from datetime import datetime
import logging

PayloadType = str | int | float | None

_LOGGER = logging.getLogger(__name__)


class AirzoneMqttApi:
    """Airzone MQTT API."""

    def __init__(self) -> None:
        """Airzone MQTT API init."""
        self._api_init_done: bool = False

        self.mqtt_publish: Callable[[str, PayloadType, int, bool], None] | None = None

    def msg_callback(self, topic: str, payload: bytes, dt: datetime | None) -> None:
        """Airzone MQTT message callback."""
        _LOGGER.warning(
            "msg_callback: topic=%s payload=%s datetime=%s", topic, payload, dt
        )
