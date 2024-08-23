"""Basic Airzone MQTT client example."""

import asyncio
import json

from _secrets import MQTT_TOPIC
from mqtt import AirzoneMqttHelper

from airzone_mqtt.mqttapi import AirzoneMqttApi


async def main() -> None:
    """Basic Airzone MQTT client example."""
    airzone_mqtt = AirzoneMqttApi(MQTT_TOPIC)
    mqtt_helper = AirzoneMqttHelper()

    airzone_mqtt.mqtt_publish = mqtt_helper.publish
    mqtt_helper.msg_callback = airzone_mqtt.msg_callback

    mqtt_helper.connect_helper()
    mqtt_helper.subscribe_helper()

    print("Wait for API init...")
    await airzone_mqtt.update()
    print("***")

    airzone_data = airzone_mqtt.data()
    print(json.dumps(airzone_data, indent=4, sort_keys=True))
    print("***")

    print("Sleeping...")
    await asyncio.sleep(65)
    print("***")

    airzone_data = airzone_mqtt.data()
    print(json.dumps(airzone_data, indent=4, sort_keys=True))
    print("***")

    mqtt_helper.disconnect_helper()


if __name__ == "__main__":
    asyncio.run(main())
