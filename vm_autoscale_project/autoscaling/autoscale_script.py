import requests
import json
import subprocess

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
INSTANCE_NAME = "autoscaled-instance"
MACHINE_TYPE = "e2-medium"
ZONE = "us-central1-a"
IMAGE_PROJECT = "ubuntu-os-cloud"
IMAGE_FAMILY = "ubuntu-2204-lts"

def get_cpu_usage():
    query = '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    result = response.json()
    if result['status'] == 'success' and result['data']['result']:
        return float(result['data']['result'][0]['value'][1])
    return 0.0

def launch_gcp_instance():
    command = f"gcloud compute instances create {INSTANCE_NAME} --machine-type={MACHINE_TYPE}               --image-family={IMAGE_FAMILY} --image-project={IMAGE_PROJECT} --zone={ZONE}"
    subprocess.run(command, shell=True)
    print("GCP Instance Launched")

if get_cpu_usage() > 75:
    launch_gcp_instance()
