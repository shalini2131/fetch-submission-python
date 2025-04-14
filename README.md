
# Fetch Take Home – Site Reliability Engineering Exercise

## Overview

This Python program monitors the availability of multiple HTTP endpoints provided via a YAML config file. It checks each endpoint every **15 seconds**, logs the results, and calculates **cumulative availability** for each domain (ignoring ports).

---

## How to Run

### 🧱 Requirements
- Python 3.7+
- `requests`, `pyyaml` libraries

### Install dependencies
```bash
pip install requests pyyaml
```

### Run the Program (with Virtual Environment)

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install requests pyyaml

# Run the script
python3 main.py sample.yaml
```
---

## Functionality

- Accepts YAML config with endpoint definitions
- Checks endpoints every 15 seconds
- Endpoint is **available** only if:
  - Status code is `200–299`
  - Response time is **≤ 500ms**
- Logs cumulative availability per **domain** (port ignored)
- Rounds availability to whole number (**no decimals**)
- Supports `GET`, `POST`, and headers/body handling

---

## Modifications & Fixes (Compared to Starter Code)

### 1. **YAML Parsing and Method Default**
- Set default method to `GET` when missing.
- Used `yaml.safe_load()` to read valid config.

### 2. **Proper Request Body Handling**
- Body from YAML is a JSON string; parsed with `json.loads()` before sending.
- `json=` used with `requests.request()` so headers and body format are correct.

### 3. **Response Time Enforcement**
- Measured exact request time with `time.time()`.
- Marked endpoints unavailable if response took more than 500ms.

### 4. **Accurate Domain Extraction**
- Used `urllib.parse.urlparse()` to extract hostname and ignore port numbers.

### 5. **Fixed Availability Calculation**
- Tracked total and success counts **by domain**.
- Dropped decimals using `int()` for clean logging.

### 6. **Consistent 15-Second Looping**
- Measured each cycle time and used `time.sleep()` to ensure exact 15s intervals.

---

## Sample Output

```bash
(venv) shalinikallepallli@MacBookAir sre-take-home-exercise-python % python3 main.py sample.yaml
[2025-04-14 18:45:08] dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 50% availability percentage
---

[2025-04-14 18:45:22] dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 50% availability percentage
```

---