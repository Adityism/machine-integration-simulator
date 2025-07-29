import time
import json
import math
import random
import paho.mqtt.client as mqtt
from pymongo import MongoClient

# MongoDB Setup
mongo_client = MongoClient("mongodb://admin:password@localhost:27017/")
db = mongo_client["smart_factory"]
collection = db["plc_data"]

# MQTT Config
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "plc/data"

class PLC_Simulator:
    def __init__(self):
        self.motor_running = False
        self.conveyor_belt = False
        self.pressure = 20.0
        self.flow_rate = 10.0
        self.operating_mode = "normal"
        self.t = 0

    def update_inputs(self):
        self.emergency_stop = random.random() < 0.01
        self.start_button = not self.emergency_stop and random.random() < 0.8
        self.safety_door = random.random() > 0.95

    def update_outputs(self):
        if self.emergency_stop or self.safety_door:
            self.motor_running = False
            self.conveyor_belt = False
            self.alarm_light = True
        elif self.start_button:
            self.motor_running = True
            self.conveyor_belt = True
            self.alarm_light = False
        else:
            self.motor_running = False
            self.conveyor_belt = False
            self.alarm_light = False

    def update_analogs(self):
        self.t += 1
        base_pressure = 30 + 10 * math.sin(self.t / 30)
        base_flow = 12 + 5 * math.sin(self.t / 20 + 1)

        self.pressure = round(base_pressure + random.uniform(-1.5, 1.5), 2)
        self.flow_rate = round(base_flow + random.uniform(-1.0, 1.0), 2)

    def calculate_error_code(self):
        if self.emergency_stop:
            return 403
        elif self.safety_door:
            return 301
        elif self.pressure > 48:
            return 302
        elif self.flow_rate < 5:
            return 401
        return 0

    def generate_data(self):
        self.update_inputs()
        self.update_outputs()
        self.update_analogs()

        return {
            "timestamp": time.time(),
            "input_states": {
                "emergency_stop": self.emergency_stop,
                "start_button": self.start_button,
                "safety_door": self.safety_door
            },
            "output_states": {
                "motor_running": self.motor_running,
                "alarm_light": self.alarm_light,
                "conveyor_belt": self.conveyor_belt
            },
            "analog_inputs": {
                "pressure": self.pressure,
                "flow_rate": self.flow_rate
            },
            "error_codes": self.calculate_error_code()
        }

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ MQTT connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        collection.insert_one(data)
        print(f"📥 Inserted data @ {time.strftime('%H:%M:%S', time.localtime(data['timestamp']))}")
    except Exception as e:
        print("⚠️ MongoDB insert error:", e)

# Main Runtime
if __name__ == "__main__":
    print("🚀 Starting Combined PLC Simulator + MQTT + MongoDB...")

    simulator = PLC_Simulator()

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()

        while True:
            data = simulator.generate_data()
            payload = json.dumps(data)
            mqtt_client.publish(MQTT_TOPIC, payload)
            print(f"📤 Published: {payload}")
            time.sleep(3)

    except KeyboardInterrupt:
        print("🛑 Stopping...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
    except Exception as e:
        print("❗ Error:", e)
        mqtt_client.loop_stop()
        mqtt_client.disconnect()