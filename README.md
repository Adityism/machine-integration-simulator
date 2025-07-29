# Smart Manufacturing Telemetry + Monitoring System

This project aims to simulate an end-to-end Industry 4.0 pipeline for smart manufacturing, integrating CNC machines, PLCs, SCADA concepts, and predictive maintenance.

## Project Structure

- `simulators/`: Contains Python scripts for CNC and PLC simulation.
- `node-red/`: Node-RED flows and configurations.
- `mqtt/`: Mosquitto MQTT broker configurations.
- `mongo/`: MongoDB initialization scripts.
- `prometheus/`: Prometheus configurations.
- `grafana/`: Grafana dashboards.
- `analytics/`: Python scripts for predictive maintenance.

## Setup and Installation

Detailed setup instructions will be provided in a separate documentation file.

## Components

- **CNC Machine (simulated)**: Generates telemetry data (temperature, vibration, spindle speed, fault codes).
- **PLC (simulated)**: Generates input/output states, error codes, simulated Modbus registers.
- **SCADA (concept)**: Implemented using Node-RED + dashboards for control and monitoring.
- **OPC UA**: Simulated machine-to-server communication.
- **MTConnect**: Extracts CNC-specific telemetry data.
- **MQTT**: Used for device-to-server data transfer via Mosquitto broker.
- **Node-RED**: Orchestrates message routing, basic logic, and UI widgets.
- **Prometheus + Grafana**: Real-time monitoring, metrics, and visualizations.
- **MongoDB**: Persistent storage of raw machine data and PLC signals.
- **Predictive Maintenance**: Analyzes logs, detects anomalies, and simulates failure prediction using Python (pandas, NumPy).

## Technical Stack

| Layer             | Tool                      |
|-------------------|---------------------------|
| Simulation        | Python scripts            |
| Protocols         | MQTT, OPC UA, MTConnect   |
| Message Broker    | Mosquitto                 |
| Data Orchestration| Node-RED                  |
| Database          | MongoDB                   |
| Monitoring        | Prometheus                |
| Dashboard         | Grafana                   |
| Analytics         | Python (pandas, NumPy)    |

## System Architecture

1. Simulated CNC generates MTConnect + OPC UA data.
2. Simulated PLC sends Modbus-style digital/analog signals via MQTT.
3. Node-RED connects all sources, routes messages, and sends to MongoDB + Prometheus.
4. Prometheus scrapes system metrics.
5. Grafana visualizes data in real-time.
6. Python batch job reads MongoDB, runs anomaly detection, and flags issues.
7. Alerts are shown in Grafana or via Node-RED dashboard.

cd simulators && python3 cnc_simulator.py
cd simulators && python3 plc_simulator.py   
python3 -m venv .venv && source .venv/bin/activate && pip install jupyter && jupyter notebook