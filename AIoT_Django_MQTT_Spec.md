Project Specification: Django MQTT AIoT System (Smart Farm)

1. Project Context

We are developing a Smart Farm management system. The backend is built with Django and uses MQTT to communicate with ESP32 devices. Data is stored in PostgreSQL. The system also integrates with n8n for automation workflows (e.g., Line Notify on overflow).

2. MQTT Topic & Payload Architecture

Topics Structure:

smartfarm/<board_id>/telemetry: Device sends sensor & relay data.

smartfarm/<board_id>/status: Device sends availability (LWT/Online).

smartfarm/<board_id>/control: Django sends commands to Device.

Payload Examples:

Telemetry (/telemetry):

{
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "timestamp": 1234567,
  "rssi": -65,
  "sensors": {
    "water_temp": 25.5,
    "air_temp": 30.2,
    "air_humidity": 65.0,
    "water_overflow": false,
    "water_dry": false
  },
  "relays": {
    "relay1_pump": false,
    "relay2_fan": true,
    "relay3_heater": false
  }
}


Status (/status - Retained):

{
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "status": "online",
  "ip": "192.168.1.50",
  "firmware": "1.0.0",
  "uptime": 3600
}


Control (/control):

{
  "command": "relay_control",
  "relays": { "relay1_pump": true, "relay2_fan": false, "relay3_heater": false }
}


3. Database Schema (Django Models)

Device Model:

board_id (CharField, Unique, Primary Key)

status (CharField: 'online'/'offline')

ip_address (GenericIPAddressField)

firmware_version (CharField)

last_seen (DateTimeField)

TelemetryLog Model:

device (ForeignKey to Device)

rssi (IntegerField)

sensor_data (JSONField) - Store the 'sensors' object here

relay_status (JSONField) - Store the 'relays' object here

created_at (DateTimeField, auto_now_add=True)

4. Tasks for GitHub Copilot (Instructions)

Please implement the following components in the Django project:

Task 1: models.py

Create Device and TelemetryLog models based on the schema above.

Add a __str__ method to both models for easy debugging.

Task 2: MQTT Service (mqtt_handler.py)

Use paho.mqtt.client.

Define MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD (fetch from django.conf.settings).

Logic for on_message:

Parse JSON payload.

Identify board_id from the payload or topic string.

If topic is /status: Update/Create Device instance with status, IP, and firmware.

If topic is /telemetry:

Update Device last_seen.

Create a TelemetryLog entry.

n8n Integration: If sensors.water_overflow is true, send an HTTP POST request to settings.N8N_WEBHOOK_URL with the full payload.

Handle missing keys in sensors or relays objects gracefully.

Task 3: Management Command (mqtt_worker.py)

Create a custom Django management command python manage.py run_mqtt_worker.

This command should initialize the mqtt_handler.py and run client.loop_forever().

Task 4: Control View (views.py)

Create a function send_control_command(board_id, relay_data).

It should publish the JSON control payload to the smartfarm/<board_id>/control topic.

Return a JsonResponse indicating success or failure.

5. Required Settings (Append to settings.py)

MQTT_BROKER = 'your-broker-address'
MQTT_PORT = 1883
MQTT_USER = 'your-user'
MQTT_PASSWORD = 'your-password'
N8N_WEBHOOK_URL = 'https://your-n8n-instance/webhook/...'
