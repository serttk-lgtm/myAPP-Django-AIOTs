Project Specification: Django AIoT Backend with MQTT & n8n

1. Context & Objective

We are building a Smart Farm management system. The backend uses Django to manage ESP32 devices via MQTT. Data is stored in PostgreSQL. We use n8n for external automation (notifications/AI analysis).

2. Hardware: ESP32 Payload Reference

The board_id is unique (e.g., ESP32-FARM-001-NATTAPHOL-PALM).

A. Telemetry (Topic: smartfarm/+/telemetry)

sensors: water_temp, air_temp, air_humidity (all optional floats), water_overflow (bool), water_dry (bool).

relays: relay1_pump, relay2_fan, relay3_heater (all bool).

B. Status (Topic: smartfarm/+/status)

status: online | offline (Last Will and Testament supported).

ip, firmware, uptime, timestamp.

C. Control (Topic: smartfarm/+/control)

Commands: relay_control (with relay object), reboot, ping.

3. Implementation Requirements

Phase 1: Data Models (models.py)

Device Model:

board_id (CharField, unique)

status (CharField: online/offline)

ip_address (GenericIPAddressField, null=True)

firmware_version (CharField)

last_seen (DateTimeField, auto_now=True)

metadata (JSONField for uptime or extra info)

TelemetryLog Model:

device (ForeignKey to Device)

rssi (IntegerField)

sensor_data (JSONField: stores the 'sensors' object)

relay_state (JSONField: stores the 'relays' object)

created_at (DateTimeField, auto_now_add=True)

Phase 2: MQTT Service (mqtt_handler.py)

Use paho-mqtt.

on_connect: Subscribe to smartfarm/+/telemetry and smartfarm/+/status.

on_message:

Parse JSON safely.

If status topic: Update or Create the Device record.

If telemetry topic:

Create TelemetryLog entry.

Constraint: Handle missing keys in sensors (e.g., water_temp) using .get().

n8n Integration: If water_overflow is true, send a POST request to N8N_WEBHOOK_URL (defined in settings).

Phase 3: Background Worker

Create a Django Management Command (management/commands/run_mqtt.py) to initialize the MQTT client and run client.loop_forever().

Phase 4: Device Control API (views.py)

Create a view to publish MQTT messages to the /control topic.

Ensure the payload matches the ESP32 expectations.

4. Prompt for Copilot (How to use this file)

Open this file in your IDE.

Open models.py and ask: "Generate Django models based on AIoT_Django_Specification.md"

Create mqtt_handler.py and ask: "Implement paho-mqtt logic to handle telemetry and status topics as per AIoT_Django_Specification.md. Include n8n webhook trigger for water_overflow."

Create the management command and ask: "Create a Django command to run the mqtt_handler service in the background."