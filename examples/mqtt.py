"""Airzone MQTT example functions."""

from collections.abc import Callable
from datetime import datetime, timezone
from threading import Event
import timeit
from typing import Any

from _secrets import MQTT_HOST, MQTT_PASS, MQTT_PORT, MQTT_TOPIC, MQTT_USER
import paho.mqtt.client as mqtt
from paho.mqtt.client import ConnectFlags, DisconnectFlags
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode

from airzone_mqtt.const import MQTT_TIMEOUT
from airzone_mqtt.mqttapi import PayloadType


class AirzoneMqttHelper:
    """Airzone MQTT Helper."""

    def __init__(self) -> None:
        """Airzone MQTT Helper init."""
        self.mqtt_client = mqtt.Client(CallbackAPIVersion.VERSION2)
        self.mqtt_event_connect = Event()
        self.mqtt_event_disconnect = Event()
        self.mqtt_event_subscribe = Event()
        self.mqtt_is_connected = False
        self.msg_callback: Callable[[str, bytes, datetime | None], None] | None = None

        self.mqtt_client.username_pw_set(
            username=MQTT_USER,
            password=MQTT_PASS,
        )

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_subscribe = self.on_subscribe

    def on_connect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None,
    ) -> None:
        # pylint: disable=unused-argument
        """MQTT connection event callback."""
        self.mqtt_is_connected = reason_code.value == 0

        self.mqtt_event_connect.set()

    def on_disconnect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: DisconnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None,
    ) -> None:
        # pylint: disable=unused-argument
        """MQTT disconnection event callback."""
        self.mqtt_is_connected = False

        self.mqtt_event_disconnect.set()

    def on_message(
        self,
        client: mqtt.Client,
        userdata: Any,
        message: mqtt.MQTTMessage,
    ) -> None:
        # pylint: disable=unused-argument
        """MQTT message event callback."""
        cur_dt = datetime.now(tz=timezone.utc)
        if self.msg_callback is not None:
            if message.retain:
                msg_dt = None
            else:
                msg_dt = cur_dt
            self.msg_callback(message.topic, message.payload, msg_dt)

    def on_subscribe(
        self,
        client: mqtt.Client,
        userdata: Any,
        mid: int,
        reason_codes: list[ReasonCode],
        properties: Properties | None,
    ) -> None:
        # pylint: disable=unused-argument
        """MQTT subscription event callback."""
        self.mqtt_event_subscribe.set()

    def connect(self) -> None:
        """Connect to MQTT broker."""
        self.mqtt_event_connect.clear()
        self.mqtt_event_disconnect.clear()
        self.mqtt_event_subscribe.clear()

        self.mqtt_client.connect(MQTT_HOST, MQTT_PORT)
        self.mqtt_client.loop_start()

    def connect_helper(self) -> None:
        """MQTT connection helper."""
        connect_start = timeit.default_timer()
        self.connect()
        self.mqtt_event_connect.wait(MQTT_TIMEOUT)
        connect_end = timeit.default_timer()
        print(f"MQTT connect time: {connect_end - connect_start}")

    def disconnect(self) -> None:
        """Disconnect from MQTT broker."""
        self.mqtt_event_connect.clear()
        self.mqtt_event_disconnect.clear()
        self.mqtt_event_subscribe.clear()

        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

    def disconnect_helper(self) -> None:
        """MQTT disconnection helper."""
        disconnect_start = timeit.default_timer()
        self.disconnect()
        self.mqtt_event_disconnect.wait(MQTT_TIMEOUT)
        disconnect_end = timeit.default_timer()
        print(f"MQTT disconnect time: {disconnect_end - disconnect_start}")

    def subscribe(self) -> None:
        """Perform a MQTT subscription."""
        self.mqtt_client.subscribe(MQTT_TOPIC)

    def subscribe_helper(self) -> None:
        """MQTT subscription helper."""
        subscribe_start = timeit.default_timer()
        self.subscribe()
        self.mqtt_event_subscribe.wait(MQTT_TIMEOUT)
        subscribe_end = timeit.default_timer()
        print(f"MQTT subscribe time: {subscribe_end - subscribe_start}")

    def publish(
        self,
        topic: str,
        payload: PayloadType = None,
        qos: int = 0,
        retain: bool = False,
    ) -> None:
        """Publish message on MQTT topic."""
        self.mqtt_client.publish(topic, payload, qos, retain)
