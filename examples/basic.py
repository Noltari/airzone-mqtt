"""Basic Airzone MQTT client example."""

import asyncio
import time

from mqtt import AirzoneMqttHelper

from airzone_mqtt.mqttapi import AirzoneMqttApi


async def main() -> None:
    """Basic Airzone MQTT client example."""
    airzone_mqtt = AirzoneMqttApi()
    mqtt_helper = AirzoneMqttHelper()

    airzone_mqtt.mqtt_publish = mqtt_helper.publish
    mqtt_helper.msg_callback = airzone_mqtt.msg_callback

    mqtt_helper.connect_helper()
    mqtt_helper.subscribe_helper()

    airzone_mqtt.mqtt_publish("test/airzone", "test start")

    print("Sleeping...")
    time.sleep(65)
    print("***")

    airzone_mqtt.mqtt_publish("test/airzone", "test end")

    mqtt_helper.disconnect_helper()


if __name__ == "__main__":
    asyncio.run(main())
