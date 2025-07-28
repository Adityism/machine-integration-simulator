# Smart Manufacturing Telemetry + Monitoring System: Detailed Setup Guide

**Author: Manus AI**

## 1. Introduction

This document provides a comprehensive guide to setting up and understanding the Smart Manufacturing Telemetry + Monitoring System. This project simulates a full Industry 4.0 pipeline, integrating various components like CNC machines, PLCs, SCADA concepts, and predictive maintenance. The goal is to demonstrate a realistic and scalable architecture suitable for a smart factory or industrial automation R&D environment, covering core aspects of machine integration using industrial protocols and tools.

## 2. System Overview

The system simulates a smart factory environment where CNC machines and PLCs generate telemetry data. This data is then collected, processed, stored, and visualized in real-time. The project simulates both machine telemetry (CNC) and controller-level state changes (PLC) using real industrial data protocols. The end-to-end pipeline is designed to:

- Generate telemetry data from simulated CNC machines (temperature, vibration, spindle speed, fault codes).
- Generate input/output states, error codes, and simulated Modbus registers from simulated PLCs.
- Collect and process data using industrial protocols like MQTT, OPC UA, and MTConnect.
- Store raw machine data and PLC signals persistently in MongoDB.
- Orchestrate message routing, basic logic, and UI widgets using Node-RED.
- Provide real-time monitoring, metrics, and visualizations through Prometheus and Grafana.
- Analyze logs, detect anomalies, and simulate failure prediction using Python for predictive maintenance.

## 3. Components and Technical Stack

This section details each mandatory component used in the project, explaining its purpose and how it integrates into the overall system.




### 3.1. CNC Machine (Simulated)

**Purpose:** To generate realistic telemetry data that mimics the output of a Computer Numerical Control (CNC) machine. This data includes parameters such as temperature, vibration, spindle speed, and various fault codes. In a real industrial setting, CNC machines are critical for precision manufacturing, and their operational data is vital for monitoring performance and predicting maintenance needs.

**Role in this project:** The `cnc_simulator.py` script generates synthetic data points for these parameters. While simulated, the data is structured to resemble actual MTConnect and OPC UA outputs, allowing for realistic testing of data ingestion and processing pipelines. This simulation is crucial for developing and testing the system without requiring physical hardware.

**Why it was used:** Simulating CNC data allows for a controlled environment to test the data collection, protocol handling (MTConnect, OPC UA), and subsequent analysis without the complexities and costs associated with real CNC machinery. It provides a consistent data stream for development and debugging.

### 3.2. PLC (Simulated)

**Purpose:** To simulate the behavior of a Programmable Logic Controller (PLC), which is the backbone of industrial automation. PLCs control industrial processes and generate data related to input/output states, error codes, and register values (e.g., Modbus registers). This data is essential for understanding the operational status of automated processes.

**Role in this project:** The `plc_simulator.py` script generates simulated PLC data, including boolean states for inputs (e.g., emergency stop, start button) and outputs (e.g., motor running, alarm light), as well as analog values (e.g., pressure, flow rate) and error codes. This data is designed to be transmitted via MQTT, simulating a common industrial communication method.

**Why it was used:** Similar to the CNC simulator, the PLC simulator provides a controlled and reproducible source of industrial control data. It enables the development and testing of MQTT-based data ingestion and the integration with Node-RED for processing and visualization, without needing actual PLC hardware.

### 3.3. SCADA (Concept with Node-RED + Dashboards)

**Purpose:** Supervisory Control and Data Acquisition (SCADA) systems are used for monitoring and controlling industrial processes. They collect data from various sources, present it to operators through graphical interfaces, and allow for remote control of equipment.

**Role in this project:** While a full-fledged SCADA system is complex, this project implements SCADA *concepts* using Node-RED and its dashboard capabilities. Node-RED is used to create a web-based interface that visualizes real-time data from the simulated CNC and PLC, and potentially allows for basic control actions (though control actions are not explicitly implemented in the initial phase of this project).

**Why it was used:** Node-RED offers a low-code, flow-based programming environment that is ideal for rapid prototyping of industrial applications. Its built-in dashboard functionality makes it suitable for creating SCADA-like interfaces quickly, demonstrating data visualization and operational monitoring without extensive front-end development.

### 3.4. OPC UA

**Purpose:** OPC Unified Architecture (OPC UA) is a platform-independent, service-oriented architecture that integrates all the functionality of the individual OPC Classic specifications into one extensible framework. It is a secure, reliable, and interoperable communication standard for industrial automation.

**Role in this project:** In this simulated environment, the CNC simulator is designed to generate data that *would* typically be transmitted via OPC UA. While a full OPC UA server and client implementation is beyond the scope of a simple Python script, the project acknowledges its importance by structuring the CNC data in a way that is compatible with OPC UA concepts. This ensures that the data format is realistic for future integration with actual OPC UA systems.

**Why it was used:** OPC UA is a cornerstone of Industry 4.0 for secure and reliable data exchange. Including its conceptual presence ensures the simulated system reflects modern industrial communication standards, making the architecture scalable and relevant.

### 3.5. MTConnect

**Purpose:** MTConnect is an open, royalty-free manufacturing technical standard that provides a common language for manufacturing equipment to communicate. It defines a standardized XML schema for machine data, making it easier to collect, analyze, and utilize data from diverse manufacturing assets.

**Role in this project:** The CNC simulator is designed to generate telemetry data in a format that aligns with MTConnect. This means the data points (temperature, vibration, spindle speed, fault codes) are analogous to those found in an MTConnect data stream. This conceptual integration ensures that the simulated CNC data is industrially relevant and can be easily adapted for actual MTConnect parsing.

**Why it was used:** MTConnect is specifically designed for machine tool data, providing rich context for manufacturing operations. Its inclusion ensures that the simulated CNC data is not generic but adheres to a widely adopted industrial standard, enhancing the realism and practical applicability of the system.

### 3.6. MQTT

**Purpose:** Message Queuing Telemetry Transport (MQTT) is a lightweight messaging protocol for small sensors and mobile devices, optimized for high-latency or unreliable networks. It operates on a publish/subscribe model, making it efficient for IoT and industrial applications where many devices need to send data to a central broker.

**Role in this project:** MQTT is used as the primary protocol for the PLC simulator to send its data (input/output states, analog values, error codes) to the central system. A Mosquitto MQTT broker acts as the central hub for all MQTT messages, which are then consumed by Node-RED for further processing.

**Why it was used:** MQTT's lightweight nature and publish/subscribe model make it ideal for connecting numerous industrial devices. Its efficiency and widespread adoption in IoT and industrial settings make it a mandatory component for a realistic smart factory simulation.

### 3.7. Node-RED

**Purpose:** Node-RED is a flow-based programming tool for wiring together hardware devices, APIs, and online services in new and interesting ways. It provides a browser-based editor that makes it easy to connect flows using a wide range of nodes.

**Role in this project:** Node-RED serves as the central data orchestration layer. It subscribes to MQTT topics from the PLC simulator, processes the incoming data, and then routes it to various destinations, including MongoDB for persistent storage and potentially Prometheus for monitoring. It also hosts the SCADA-like dashboards for visualization and basic control.

**Why it was used:** Node-RED's visual programming interface and extensive library of nodes (including MQTT, MongoDB, and HTTP nodes) make it exceptionally well-suited for rapidly building data pipelines and creating interactive dashboards. It simplifies the integration of diverse data sources and destinations within the industrial environment.

### 3.8. Prometheus + Grafana

**Purpose:** Prometheus is an open-source monitoring system with a dimensional data model, flexible query language (PromQL), and an alert manager. Grafana is an open-source platform for monitoring and observability, allowing users to create dynamic and interactive dashboards from various data sources, including Prometheus.

**Role in this project:** Prometheus is used to collect time-series metrics from various components of the system, such as Node-RED. Grafana then connects to Prometheus to visualize these metrics in real-time dashboards, providing operators and engineers with insights into the system's performance and health. This combination forms the core of the real-time monitoring and visualization capabilities.

**Why it was used:** Prometheus and Grafana are a powerful and widely adopted combination for monitoring in modern IT and industrial environments. They provide robust capabilities for data collection, querying, and visualization, essential for maintaining operational awareness in a smart factory.

### 3.9. MongoDB

**Purpose:** MongoDB is a NoSQL document database designed for scalability and flexibility. It stores data in flexible, JSON-like documents, meaning fields can vary from document to document and data structure can be changed over time.

**Role in this project:** MongoDB is used for the persistent storage of raw machine data and PLC signals. Data ingested by Node-RED from the simulators is stored in MongoDB, providing a historical record for later analysis, including predictive maintenance tasks.

**Why it was used:** MongoDB's flexible schema is well-suited for storing diverse and evolving industrial telemetry data, which may not always fit neatly into a rigid relational database structure. Its scalability also makes it appropriate for handling large volumes of time-series data generated in a smart factory.

### 3.10. Predictive Maintenance (Python with pandas, NumPy)

**Purpose:** Predictive maintenance involves using data analysis techniques to predict when equipment failure might occur, allowing maintenance to be performed proactively rather than reactively. This minimizes downtime and optimizes maintenance schedules.

**Role in this project:** A Python script (`predictive_maintenance.ipynb`) utilizes libraries like pandas and NumPy to analyze the historical data stored in MongoDB. This module performs basic anomaly detection and simulates failure prediction based on predefined thresholds or patterns in the data. It can also generate alerts based on these predictions.

**Why it was used:** Python, with its rich ecosystem of data science libraries (pandas for data manipulation, NumPy for numerical operations, scikit-learn for machine learning), is an industry standard for data analysis and predictive modeling. This allows for the implementation of sophisticated algorithms to derive insights from the collected telemetry data.




## 4. Setup Instructions

This section provides step-by-step instructions for setting up each component of the Smart Manufacturing Telemetry + Monitoring System. We will primarily use Docker for ease of deployment and consistency across different operating systems (Linux, Mac, Windows). Ensure you have Docker and Docker Compose installed on your system before proceeding.

### 4.1. Prerequisites: Docker and Docker Compose

To run this project, you need Docker and Docker Compose. These tools allow you to run applications in isolated containers, simplifying dependency management and deployment.

- **Docker Desktop (for Windows/Mac) or Docker Engine (for Linux):**
  - **Download Link:** [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
  - **Installation:** Follow the instructions on the Docker website specific to your operating system. For Linux, you might need to follow the official Docker Engine installation guide for your distribution.
  - **Verification:** Open a terminal or command prompt and run:
    ```bash
    docker --version
    docker compose version
    ```
    You should see version numbers for both Docker and Docker Compose, indicating a successful installation.

### 4.2. Project Structure

First, ensure you have the correct project structure. The `docker-compose.yml` file in the root directory orchestrates all the services. The project should be organized as follows:

```
/smart-factory/
├── simulators/
│   ├── cnc_simulator.py
│   ├── plc_simulator.py
│   └── requirements.txt
├── node-red/
│   └── flows.json
├── mqtt/
│   └── mosquitto.conf
├── mongo/
│   └── init.js
├── prometheus/
│   └── prometheus.yml
├── grafana/
│   └── dashboards/
│       └── plc_dashboard.json
├── analytics/
│   └── predictive_maintenance.ipynb
├── README.md
└── docker-compose.yml
```

### 4.3. Mosquitto MQTT Broker Setup

Mosquitto is a lightweight open-source message broker that implements the MQTT protocol. It will handle all MQTT communication between our simulated PLC and Node-RED.

**Configuration File (`mqtt/mosquitto.conf`):**

This file configures the Mosquitto broker. It enables persistence, logs to a file, and sets up listeners for standard MQTT (port 1883) and WebSockets (port 9001). Anonymous access is allowed for simplicity in this simulation.

```conf
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log

listener 1883
allow_anonymous true

listener 9001
protocol websockets
```

**How to Start:**

The Mosquitto service is defined in the `docker-compose.yml` file. Navigate to the `/smart-factory/` directory in your terminal and run:

```bash
docker compose up -d mosquitto
```

This command will pull the `eclipse-mosquitto` Docker image (if not already present), create a container named `mosquitto`, and start the broker in detached mode (`-d`).

**How to Test:**

You can test the Mosquitto broker by subscribing to a topic and publishing a message. You can use a tool like `mqtt-explorer` (a graphical MQTT client) or command-line tools like `mosquitto_sub` and `mosquitto_pub` (which come with Mosquitto installation or can be run from a Docker container).

**Using `mosquitto_sub` and `mosquitto_pub` (from another terminal/container):**

1. **Subscribe to a topic:**
   ```bash
   docker run --rm -it --network smart-factory_default eclipse-mosquitto mosquitto_sub -h mosquitto -t test/topic
   ```
   (Note: `smart-factory_default` is the default network created by Docker Compose for your project. You might need to adjust this if you change the network name in `docker-compose.yml`.)

2. **Publish a message:**
   ```bash
   docker run --rm -it --network smart-factory_default eclipse-mosquitto mosquitto_pub -h mosquitto -t test/topic -m "Hello MQTT!"
   ```

If the subscription terminal receives "Hello MQTT!", your Mosquitto broker is working correctly.




### 4.4. MongoDB Setup

MongoDB is used for persistent storage of raw machine data and PLC signals. It provides a flexible schema, which is ideal for the varied data types encountered in industrial telemetry.

**Initialization Script (`mongo/init.js`):**

This script is executed when the MongoDB container starts for the first time. It creates a user with read/write access to the `smart_factory` database.

```javascript
db.createUser({
  user: "admin",
  pwd: "password",
  roles: [
    {
      role: "readWrite",
      db: "smart_factory",
    },
  ],
});
```

**How to Start:**

The MongoDB service is defined in the `docker-compose.yml` file. From the `/smart-factory/` directory, run:

```bash
docker compose up -d mongodb
```

This command will pull the `mongo` Docker image, create a container named `mongodb`, and start the database service in detached mode. The `init.js` script will be executed upon the first startup to set up the user.

**How to Test:**

You can test the MongoDB connection and user creation by connecting to the MongoDB instance from within another Docker container or using a MongoDB client tool.

**Using `mongosh` (from another terminal/container):**

1. **Connect to MongoDB:**
   ```bash
   docker run --rm -it --network smart-factory_default mongo mongosh mongodb://admin:password@mongodb:27017/smart_factory
   ```

2. **Verify connection and user:**
   Once connected, you should see the `smart_factory` database. You can try inserting a test document:
   ```javascript
   db.test_collection.insertOne({ "message": "MongoDB is working!" })
   ```
   And then find it:
   ```javascript
   db.test_collection.find()
   ```

If the insert and find operations are successful, your MongoDB setup is correct.




### 4.5. Node-RED Setup

Node-RED acts as the central data orchestration layer, connecting various data sources, routing messages, and providing a visual interface for monitoring and control.

**Flows File (`node-red/flows.json`):**

This file contains the Node-RED flows that define the data processing logic. It includes nodes for:

-   **MQTT Input:** Subscribes to `plc/data` from the Mosquitto broker.
-   **MongoDB Output:** Stores the incoming PLC data into the `plc_data` collection in the `smart_factory` database.
-   **Dashboard Nodes:** Extracts specific values (e.g., pressure, flow rate, motor status, error codes) from the PLC data and displays them on a web-based dashboard.

**How to Start:**

The Node-RED service is defined in the `docker-compose.yml` file. From the `/smart-factory/` directory, run:

```bash
docker compose up -d node-red
```

This command will pull the `nodered/node-red` Docker image, create a container named `node-red`, and start the service in detached mode. The `flows.json` file will be automatically loaded.

**How to Access and Test:**

Node-RED will be accessible via your web browser at `http://localhost:1880`. Open this URL. You should see the Node-RED editor with the pre-configured flows. To view the dashboard, navigate to `http://localhost:1880/ui`.

1.  **Verify MQTT Connection:** In the Node-RED editor, double-click the "PLC Data In" MQTT input node. Ensure its status shows "Connected". If not, check your Mosquitto setup.
2.  **Verify MongoDB Connection:** Double-click the "Store to MongoDB" MongoDB output node. Ensure its status shows "Connected". If not, check your MongoDB setup.
3.  **Start PLC Simulator:** To see data flowing, you need to run the PLC simulator. Open a new terminal, navigate to `/home/ubuntu/smart-factory/simulators/` and run:
    ```bash
    python3 plc_simulator.py
    ```
    You should see data being printed in the terminal where the simulator is running. In the Node-RED editor, the "Debug PLC Data" node should start showing incoming messages in the debug sidebar. On the Node-RED dashboard (`http://localhost:1880/ui`), you should see the gauges and indicators updating with real-time data.




### 4.6. Prometheus and Grafana Setup

Prometheus is a monitoring system that collects metrics, and Grafana is used to visualize these metrics through interactive dashboards.

**Prometheus Configuration (`prometheus/prometheus.yml`):**

This file configures Prometheus to scrape metrics from itself and from the Node-RED instance.

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  - job_name: 'node-red'
    static_configs:
      - targets: ['node-red:1880'] # Node-RED metrics endpoint
```

**Grafana Dashboard (`grafana/dashboards/plc_dashboard.json`):**

This JSON file defines a Grafana dashboard for visualizing PLC data, specifically focusing on pressure. You can import this dashboard into Grafana.

**How to Start:**

Both Prometheus and Grafana services are defined in the `docker-compose.yml` file. From the `/smart-factory/` directory, run:

```bash
docker compose up -d prometheus grafana
```

This command will pull the respective Docker images, create containers, and start both services in detached mode.

**How to Access and Test:**

-   **Prometheus:** Accessible at `http://localhost:9090`.
-   **Grafana:** Accessible at `http://localhost:3000`.

**Grafana Initial Setup:**

1.  **Login:** Open `http://localhost:3000` in your browser. The default username is `admin` and the password is `admin`. You will be prompted to change the password on first login.
2.  **Add Prometheus Data Source:**
    *   Click on the gear icon (Configuration) on the left sidebar.
    *   Select "Data sources".
    *   Click "Add data source".
    *   Select "Prometheus".
    *   Set the URL to `http://prometheus:9090` (this is the internal Docker network name for the Prometheus service).
    *   Click "Save & Test". You should see "Data source is working" message.
3.  **Import Dashboard:**
    *   Click on the "+" icon on the left sidebar and select "Import".
    *   Click on "Upload JSON file" and select the `plc_dashboard.json` file from `grafana/dashboards/`.
    *   Select the Prometheus data source you just configured.
    *   Click "Import".

Now, as the PLC simulator runs and Node-RED processes data, you should see metrics appearing in your Grafana dashboard.




### 4.7. Predictive Maintenance Module Setup

The predictive maintenance module, implemented in Python, analyzes historical data from MongoDB to detect anomalies and simulate failure predictions.

**Jupyter Notebook (`analytics/predictive_maintenance.ipynb`):**

This Jupyter Notebook contains the Python code for:

-   Connecting to MongoDB and fetching PLC data.
-   Performing anomaly detection using `IsolationForest` on selected features (e.g., pressure, flow rate).
-   Simulating basic predictive maintenance alerts based on thresholds and detected anomalies.

**Dependencies:**

The Python script requires the following libraries. These are listed in `simulators/requirements.txt` and should have been installed when setting up the simulators.

-   `pandas`
-   `numpy`
-   `pymongo`
-   `scikit-learn`
-   `matplotlib`
-   `seaborn`

**How to Run:**

1.  **Ensure Services are Running:** Make sure your Mosquitto, MongoDB, Node-RED, Prometheus, and Grafana Docker containers are running (`docker compose up -d`). Also, ensure the `plc_simulator.py` is running to populate data into MongoDB.
2.  **Navigate to Analytics Directory:** Open a new terminal and navigate to the `analytics` directory:
    ```bash
    cd /home/ubuntu/smart-factory/analytics
    ```
3.  **Start Jupyter Notebook:**
    ```bash
    jupyter notebook predictive_maintenance.ipynb
    ```
    If `jupyter` is not installed, you might need to install it first:
    ```bash
    pip install jupyter
    ```
4.  **Execute Cells:** Jupyter will open in your web browser (usually `http://localhost:8888`). Open `predictive_maintenance.ipynb` and run all cells. The notebook will connect to MongoDB, fetch data, perform anomaly detection, and print any generated alerts to the console output within the notebook.

**How to Test:**

Observe the output in the Jupyter Notebook. You should see fetched data, details about detected anomalies, and any generated predictive maintenance alerts. You can modify the `plc_simulator.py` to introduce more extreme values or specific error codes to test the anomaly detection and alerting mechanisms.




## 5. System Architecture Diagram

Below is a visual representation of the system architecture, illustrating how each component interacts within the Smart Manufacturing Telemetry + Monitoring System.

![System Architecture Diagram](./architecture_diagram.png)

## 6. Troubleshooting Guide

This section provides solutions to common issues you might encounter during the setup and operation of the Smart Manufacturing Telemetry + Monitoring System.

### 6.1. Docker/Docker Compose Issues

**Problem:** `docker: command not found` or `docker compose: command not found`
**Solution:** Docker and Docker Compose are not installed or not correctly added to your system's PATH. Refer to Section 4.1 for installation instructions and ensure you have restarted your terminal or system after installation.

**Problem:** `Error response from daemon: ... address already in use`
**Solution:** This typically means a port required by one of the Docker containers is already in use by another application on your host machine. Identify the conflicting port (e.g., 1883 for Mosquitto, 27017 for MongoDB, 1880 for Node-RED, 9090 for Prometheus, 3000 for Grafana) and either:
*   Stop the conflicting application.
*   Change the port mapping in `docker-compose.yml` (e.g., `8883:1883` to map host port 8883 to container port 1883).

**Problem:** Containers fail to start or exit immediately.
**Solution:** Check the logs of the failing container. Use `docker logs <container_name>` (e.g., `docker logs mosquitto`). The logs will often provide specific error messages that can help diagnose the problem, such as configuration errors, missing files, or network issues.

### 6.2. MQTT (Mosquitto) Issues

**Problem:** PLC Simulator cannot connect to Mosquitto broker.
**Solution:**
*   Ensure the Mosquitto container is running: `docker ps | grep mosquitto`.
*   Verify the `MQTT_BROKER` and `MQTT_PORT` in `plc_simulator.py` match the Mosquitto service name and port in `docker-compose.yml` (e.g., `localhost:1883` if running simulators on host, or `mosquitto:1883` if running simulators in a Docker network).
*   Check Mosquitto logs for connection errors: `docker logs mosquitto`.

### 6.3. MongoDB Issues

**Problem:** Node-RED or Predictive Maintenance module cannot connect to MongoDB.
**Solution:**
*   Ensure the MongoDB container is running: `docker ps | grep mongodb`.
*   Verify the MongoDB connection string in Node-RED (in the MongoDB node configuration) and in `predictive_maintenance.ipynb` (e.g., `mongodb://admin:password@mongodb:27017/smart_factory`). Ensure the hostname matches the service name in `docker-compose.yml` (`mongodb`).
*   Check MongoDB logs for errors: `docker logs mongodb`.

### 6.4. Node-RED Issues

**Problem:** Node-RED flows are not loading or not processing data.
**Solution:**
*   Ensure the `node-red` container is running: `docker ps | grep node-red`.
*   Check Node-RED logs: `docker logs node-red`.
*   In the Node-RED editor (`http://localhost:1880`), check the status of the MQTT input and MongoDB output nodes. They should show "Connected". If not, re-check Mosquitto and MongoDB setups.
*   Verify that the `flows.json` file is correctly mounted into the container (check `volumes` in `docker-compose.yml`).

### 6.5. Prometheus and Grafana Issues

**Problem:** Grafana dashboards show no data or errors.
**Solution:**
*   Ensure Prometheus and Grafana containers are running: `docker ps | grep prometheus` and `docker ps | grep grafana`.
*   In Grafana (`http://localhost:3000`), verify that the Prometheus data source is correctly configured and tested successfully (URL should be `http://prometheus:9090`).
*   In Prometheus (`http://localhost:9090`), go to "Status" -> "Targets" and ensure that the `node-red` target is `UP`.
*   Check Prometheus logs: `docker logs prometheus`.

### 6.6. Predictive Maintenance Issues

**Problem:** Jupyter Notebook cannot find data in MongoDB or shows errors during analysis.
**Solution:**
*   Ensure MongoDB is running and contains data. Run the `plc_simulator.py` for some time to populate data.
*   Verify the MongoDB connection string in `predictive_maintenance.ipynb`.
*   Ensure all required Python libraries are installed in your environment where you are running Jupyter (`pip install -r simulators/requirements.txt`).
*   Check the console output in the Jupyter Notebook for specific error messages.



