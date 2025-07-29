import time
import random
import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "cnc/data"

# MongoDB Configuration
MONGO_URI = "mongodb://admin:password@localhost:27017"
MONGO_DB = "smart_factory"
MONGO_COLLECTION = "cnc_data"

# Initialize MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# Initialize MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Initialize CNC state
cnc_state = {
    "temperature": 65.0,       # degrees Celsius
    "vibration": 1.5,          # mm/s
    "spindle_speed": 3000,     # RPM
    "fault_code": 0
}

# Helper to simulate smooth change
def smooth_change(current, min_val, max_val, step=1.0):
    drift = random.uniform(-step, step)
    next_val = current + drift
    return round(max(min_val, min(max_val, next_val)), 2)

# Fault codes
FAULT_CODES = [0] * 20 + [101, 102, 205]

# Data generator
def generate_cnc_data():
    global cnc_state
    cnc_state["temperature"] = smooth_change(cnc_state["temperature"], 55, 85, step=0.5)
    cnc_state["vibration"] = smooth_change(cnc_state["vibration"], 0.5, 5.0, step=0.2)
    cnc_state["spindle_speed"] = int(smooth_change(cnc_state["spindle_speed"], 1000, 5000, step=100))
    cnc_state["fault_code"] = random.choice(FAULT_CODES)

    return {
        "timestamp": time.time(),
        "temperature": cnc_state["temperature"],
        "vibration": cnc_state["vibration"],
        "spindle_speed": cnc_state["spindle_speed"],
        "fault_code": cnc_state["fault_code"]
    }

if __name__ == "__main__":
    print("Starting CNC Simulator with MongoDB storage... Press Ctrl+C to stop.")
    try:
        while True:
            data = generate_cnc_data()
            payload = json.dumps(data)

            # Publish to MQTT
            client.publish(MQTT_TOPIC, payload)

            # Insert into MongoDB
            collection.insert_one(data)

            print(f"Pushed to MQTT and MongoDB: {payload}")
            time.sleep(2)

    except KeyboardInterrupt:
        print("CNC Simulator stopped.")
        client.disconnect()
        mongo_client.close()