import time
import json
import math
import random
import paho.mqtt.client as mqtt

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "plc/data"

class PLC_Simulator:
    def __init__(self):
        self.motor_running = False
        self.conveyor_belt = False
        self.pressure = 20.0  # PSI
        self.flow_rate = 10.0  # L/min
        self.operating_mode = "normal"  # or "fault"
        self.t = 0  # internal time counter for math waveforms

    def update_inputs(self):
        # Simulate real input logic
        if random.random() < 0.01:
            self.emergency_stop = True
        else:
            self.emergency_stop = False

        self.start_button = not self.emergency_stop and random.random() < 0.8
        self.safety_door = random.random() > 0.95  # door open 5% of the time

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
        # Use sine wave + noise for realistic analog sensor simulation
        self.t += 1
        base_pressure = 30 + 10 * math.sin(self.t / 30)
        base_flow = 12 + 5 * math.sin(self.t / 20 + 1)

        # Simulate load changes and noise
        self.pressure = round(base_pressure + random.uniform(-1.5, 1.5), 2)
        self.flow_rate = round(base_flow + random.uniform(-1.0, 1.0), 2)

    def calculate_error_code(self):
        if self.emergency_stop:
            return 403  # Emergency stop triggered
        elif self.safety_door:
            return 301  # Safety door open
        elif self.pressure > 48:
            return 302  # Overpressure
        elif self.flow_rate < 5:
            return 401  # Flow too low
        else:
            return 0  # No error

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

# MQTT Event Handlers
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker")

if __name__ == "__main__":
    print("Starting Realistic PLC Simulator... Press Ctrl+C to stop.")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    plc = PLC_Simulator()

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        while True:
            plc_data = plc.generate_data()
            message = json.dumps(plc_data)
            print(f"[{time.strftime('%H:%M:%S')}] Published: {message}")
            client.publish(MQTT_TOPIC, message)
            time.sleep(3)

    except KeyboardInterrupt:
        print("Simulator stopped.")
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"Error: {e}")
        client.loop_stop()
        client.disconnect()