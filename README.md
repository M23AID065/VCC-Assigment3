# VCC-Assigment3
# VM Auto-Scaling Project

## Overview
This project sets up a local Virtual Machine (VM), implements resource monitoring, and configures auto-scaling to Google Cloud Platform (GCP) when resource usage exceeds 75%.

## Features
- Local VM setup using VirtualBox or VMware
- Resource monitoring using Prometheus and Node Exporter
- Auto-scaling mechanism to launch a GCP instance when CPU usage surpasses the threshold
- Sample Flask application deployment
- Visualization using Grafana

## Prerequisites
- VirtualBox or VMware installed on your local machine
- GCP account with `gcloud` CLI configured
- Basic knowledge of Docker and Python

## Setup Guide

### 1. Local VM Setup
1. Install VirtualBox/VMware.
2. Create a new VM with Ubuntu 22.04.
3. Allocate at least **4GB RAM** and **20GB storage**.
4. Install required packages:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install docker.io docker-compose -y
   ```

### 2. Monitoring Setup
1. **Install Prometheus:**
   ```bash
   wget https://github.com/prometheus/prometheus/releases/download/v2.41.0/prometheus-2.41.0.linux-amd64.tar.gz
   tar -xvf prometheus-2.41.0.linux-amd64.tar.gz
   sudo mv prometheus-2.41.0.linux-amd64 /usr/local/prometheus
   ```
2. **Install Node Exporter:**
   ```bash
   wget https://github.com/prometheus/node_exporter/releases/download/v1.5.0/node_exporter-1.5.0.linux-amd64.tar.gz
   tar -xvf node_exporter-1.5.0.linux-amd64.tar.gz
   sudo mv node_exporter-1.5.0.linux-amd64 /usr/local/node_exporter
   cd /usr/local/node_exporter
   ./node_exporter
   ```

### 3. Auto-Scaling Implementation
1. **Install GCP CLI:**
   ```bash
   sudo apt install google-cloud-sdk -y
   gcloud auth login
   gcloud config set project [PROJECT_ID]
   ```
2. **Create the auto-scaling script (`autoscale_script.py`):**
   ```python
   import requests
   import subprocess
   
   PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
   INSTANCE_NAME = "autoscaled-instance"
   ZONE = "us-central1-a"
   
   def get_cpu_usage():
       response = requests.get(PROMETHEUS_URL, params={'query': '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'})
       result = response.json()
       return float(result['data']['result'][0]['value'][1]) if result['data']['result'] else 0.0
   
   def launch_gcp_instance():
       subprocess.run(f"gcloud compute instances create {INSTANCE_NAME} --zone={ZONE}", shell=True)
       print("GCP Instance Launched")
   
   if get_cpu_usage() > 75:
       launch_gcp_instance()
   ```
3. **Automate execution via Cron Job:**
   ```bash
   crontab -e
   ```
   Add:
   ```
   * * * * * /usr/bin/python3 /path/to/autoscale_script.py
   ```

### 4. Deploy Sample Application
1. **Create a Flask app (`app.py`):**
   ```python
   from flask import Flask
   app = Flask(__name__)
   
   @app.route("/")
   def home():
       return "Hello, Cloud Scaling!"
   
   if __name__ == "__main__":
       app.run(host="0.0.0.0", port=5000)
   ```
2. **Create a Dockerfile:**
   ```Dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY app.py .
   RUN pip install flask
   CMD ["python", "app.py"]
   ```
3. **Build and run the container:**
   ```bash
   docker build -t flask-app .
   docker run -d -p 5000:5000 flask-app
   ```

### 5. Access and Monitor the Setup
- **Prometheus:** `http://localhost:9090`
- **Grafana:** `http://localhost:3000` (Default login: `admin/admin`)
- **Flask App:** `http://localhost:5000`

## Conclusion
This project demonstrates an effective mechanism for monitoring local VM resources and auto-scaling to GCP when necessary. The integration of Prometheus, Grafana, and Python scripting ensures an automated cloud scaling solution.

### Directory Structure
```
vm-auto-scaling
│──  README.md
│──  autoscale_script.py
│──  app.py
│──  Dockerfile
│──  configs
│   ├──  prometheus.yml
│──  monitoring
│   ├──  node_exporter
```

## Contributing
Feel free to fork this repository and submit pull requests.

## License
This project is licensed under the MIT License.

