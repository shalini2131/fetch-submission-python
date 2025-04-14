import yaml
import requests
import time
import json
from collections import defaultdict
from urllib.parse import urlparse
# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method','GET')
    headers = endpoint.get('headers')
    body = endpoint.get('body')
    if body:
        try:
            json_body = json.loads(body)
        except json.JSONDecodeError:
            print(f"Invalid JSON body for {url}")
            json_body = None
    else:
        json_body = None

    if method == "GET":
        json_body = None

    start_time = time.time()
    try:
        response = requests.request(method, url, headers=headers, json=json_body, timeout=5)
        elapsed_ms = (time.time() - start_time) * 1000
        status_code = response.status_code
    # except Exception as e:
    #     print(f"Error checking {url}: {e}")
    except requests.RequestException:
        return "DOWN"
    if 200 <= response.status_code < 300 and elapsed_ms<=500:
        return "UP"
    else:
        return "DOWN"
    

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        cycle_start = time.time()
        for endpoint in config:
            domain = urlparse(endpoint["url"]).hostname
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = int(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")
        elapsed = time.time() - cycle_start
        print("---")
        time.sleep(15-elapsed)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")