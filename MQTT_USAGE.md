# MQTT Smart Farm Implementation Guide

## Overview
This Django application implements a complete MQTT-based Smart Farm AIoT system with ESP32 device integration, real-time telemetry logging, and automated alerting through n8n webhooks.

## Components Implemented

### 1. Django Models ([myapp/models.py](myapp/models.py))

#### Device Model
- Tracks ESP32 board information (board_id, status, IP, firmware)
- Auto-updates `last_seen` timestamp
- Primary key: `board_id`

#### TelemetryLog Model
- Stores sensor readings (water_temp, air_temp, humidity, overflow, dry status)
- Stores relay states (pump, fan, heater)
- Links to Device via ForeignKey
- Indexed for fast queries

### 2. MQTT Handler ([myapp/mqtt_handler.py](myapp/mqtt_handler.py))

#### MQTTHandler Class
- Subscribes to topics: `smartfarm/+/telemetry` and `smartfarm/+/status`
- Processes incoming messages and updates database
- Triggers n8n webhook on water overflow detection
- Handles connection/reconnection automatically

#### publish_control_command()
- Sends relay control commands to devices
- Topic: `smartfarm/<board_id>/control`

### 3. Management Command ([myapp/management/commands/run_mqtt_worker.py](myapp/management/commands/run_mqtt_worker.py))
- Starts MQTT worker as a persistent service
- Graceful shutdown on SIGINT/SIGTERM
- Usage: `python manage.py run_mqtt_worker`

### 4. API Endpoint ([myapp/views.py](myapp/views.py))
- **POST** `/api/control/` - Send control commands to devices
- Accepts JSON payload with board_id and relay states
- Returns success/failure status

### 5. Admin Interface ([myapp/admin.py](myapp/admin.py))
- Device management with filtering and search
- Telemetry log viewing with sensor value extraction
- Read-only timestamps for data integrity

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure MQTT Settings
Edit [myproject/settings.py](myproject/settings.py):

```python
MQTT_BROKER = 'broker.example.com'  # Your MQTT broker address
MQTT_PORT = 1883                     # Default: 1883 (non-SSL) or 8883 (SSL)
MQTT_USER = 'your_username'          # Set to None if no authentication
MQTT_PASSWORD = 'your_password'      # Set to None if no authentication
N8N_WEBHOOK_URL = 'https://your-n8n.com/webhook/alert'  # Your n8n webhook
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Register Your Devices
**IMPORTANT**: Devices must be registered via Django Admin before they can send data.

1. Start Django server: `python manage.py runserver`
2. Open admin panel: `http://localhost:8000/admin/`
3. Login with superuser credentials
4. Click **"Devices"** → **"Add Device"**
5. Fill in device information:
   - **Board ID**: `ESP32-FARM-001-NATTAPHOL-PALM` (match your ESP32 board_id)
   - **Status**: `offline` (will auto-update when device connects)
   - **IP Address**: Leave empty (auto-filled from MQTT status)
   - **Firmware Version**: Leave empty (auto-filled from MQTT status)
6. Click **"Save"**

**Note**: The MQTT handler will now only accept messages from registered devices. Unregistered devices will log a warning message and be ignored.

### 6. Start Django Server (MQTT Worker Auto-Starts)
```bash
python manage.py runserver
```

**✨ The MQTT worker now starts automatically when Django starts!** You'll see:
```
✅ MQTT Worker thread started successfully
🚀 Starting MQTT Worker automatically...
Connected to MQTT broker successfully
Subscribed to smartfarm topics
```

**No need to run a separate terminal for `run_mqtt_worker`** - it's now integrated into the Django startup process.

**Note**: The `run_mqtt_worker` management command is still available if you need to run it separately (e.g., in production with supervisord).

## MQTT Topic Architecture

### Device → Django (Publish)

#### Telemetry Topic: `smartfarm/<board_id>/telemetry`
```json
{
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "timestamp": 1234567890,
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
```

#### Status Topic: `smartfarm/<board_id>/status` (Retained)
```json
{
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "status": "online",
  "ip": "192.168.1.50",
  "firmware": "1.0.0",
  "uptime": 3600
}
```

### Django → Device (Publish)

#### Control Topic: `smartfarm/<board_id>/control`
```json
{
  "command": "relay_control",
  "relays": {
    "relay1_pump": true,
    "relay2_fan": false,
    "relay3_heater": false
  }
}
```

## API Usage

### Send Control Command

**Endpoint:** `POST /api/control/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/control/ \
  -H "Content-Type: application/json" \
  -d '{
    "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
    "relays": {
      "relay1_pump": true,
      "relay2_fan": false,
      "relay3_heater": false
    }
  }'
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Control command sent to ESP32-FARM-001-NATTAPHOL-PALM",
  "relays": {
    "relay1_pump": true,
    "relay2_fan": false,
    "relay3_heater": false
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "board_id is required"
}
```

## n8n Integration

When `sensor_data.water_overflow` is `true`, the system automatically sends a POST request to the configured n8n webhook:

**Payload:**
```json
{
  "alert_type": "water_overflow",
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "timestamp": "2026-04-05T10:30:00",
  "payload": {
    // Full telemetry payload
  }
}
```

### Example n8n Workflow
1. Receive webhook trigger
2. Parse alert data
3. Send Line Notify message
4. Log to Google Sheets
5. Send email notification

## Django Admin

Access the admin panel at: `http://localhost:8000/admin/`

### Features:

#### Devices Management
- **Add Device**: Register new ESP32 boards before they can send data
- **View Devices**: See all registered devices with their status and last seen time
- **Search**: Find devices by board ID or IP address  
- **Filters**: Filter by status (online/offline) or firmware version
- **Auto-Update**: IP address, firmware version, and last_seen are auto-updated from MQTT messages

**Important**: Only registered devices can send telemetry data. Unregistered devices will be ignored with a warning in logs.

#### Telemetry Logs
- **Full Data Display**: View all sensor values (water temp, air temp, humidity, overflow, dry status) and relay states (pump, fan, heater)
- **No Filters**: Clean interface showing all data in one view for easy monitoring
- **Search**: Find logs by device board ID
- **Automatic Logging**: New entries created automatically when registered devices publish telemetry

## Logging

Logs are written to:
- **Console**: Real-time output
- **File**: `mqtt_worker.log` in project root

Log entries include:
- MQTT connection status
- Message processing
- Database updates
- n8n webhook calls
- Errors and exceptions

## Testing

### Test MQTT Connection
```bash
# Subscribe to test messages
mosquitto_sub -h broker.example.com -t "smartfarm/#" -u username -P password

# Publish test telemetry
mosquitto_pub -h broker.example.com \
  -t "smartfarm/ESP32-TEST/telemetry" \
  -u username -P password \
  -m '{"board_id":"ESP32-TEST","rssi":-60,"sensors":{"water_temp":25.5},"relays":{"relay1_pump":false}}'
```

### Test API Endpoint
```python
import requests

response = requests.post('http://localhost:8000/api/control/', json={
    'board_id': 'ESP32-FARM-001-NATTAPHOL-PALM',
    'relays': {
        'relay1_pump': True,
        'relay2_fan': False,
        'relay3_heater': False
    }
})

print(response.json())
```

## Troubleshooting

### MQTT Worker Not Connecting
1. Check MQTT broker address and port in [settings.py](myproject/settings.py)
2. Verify network connectivity: `ping broker.example.com`
3. Check authentication credentials
4. Review logs in `mqtt_worker.log`

### No Data in Database
1. Ensure MQTT worker is running: `python manage.py run_mqtt_worker`
2. Check topic format matches: `smartfarm/<board_id>/telemetry`
3. Verify payload JSON format
4. Check Django logs for errors

### n8n Webhook Not Triggered
1. Verify `N8N_WEBHOOK_URL` in [settings.py](myproject/settings.py)
2. Test webhook manually: `curl -X POST <webhook_url> -d '{"test":"data"}'`
3. Check for `water_overflow: true` in telemetry payload
4. Review logs for HTTP errors

## Production Deployment

### Security Considerations
1. Change `SECRET_KEY` in [settings.py](myproject/settings.py)
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Enable MQTT SSL/TLS (port 8883)
6. Implement proper authentication

### Process Management
Use systemd or supervisor to manage processes:

**MQTT Worker Service:**
```ini
[Unit]
Description=Smart Farm MQTT Worker
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/python manage.py run_mqtt_worker
Restart=always

[Install]
WantedBy=multi-user.target
```

## File Structure
```
myAPP-Django-AIOTs/
├── myapp/
│   ├── management/
│   │   └── commands/
│   │       └── run_mqtt_worker.py  # MQTT worker command
│   ├── admin.py                    # Admin interface config
│   ├── models.py                   # Device & TelemetryLog models
│   ├── mqtt_handler.py             # MQTT service logic
│   └── views.py                    # API endpoints
├── myproject/
│   ├── settings.py                 # MQTT & n8n configuration
│   └── urls.py                     # URL routing
├── requirements.txt                # Python dependencies
└── MQTT_USAGE.md                   # This file
```

## Next Steps

1. **Frontend Dashboard**: Create a real-time monitoring interface
2. **Historical Charts**: Visualize sensor data trends
3. **Alert Rules**: Configure custom alert thresholds
4. **Device Management UI**: Add/remove devices through web interface
5. **Automated Control**: Implement rule-based relay automation

## Support

For issues or questions:
- Check logs: `mqtt_worker.log`
- Review Django admin for data verification
- Test MQTT connectivity with mosquitto_sub/pub tools
- Verify n8n webhook configuration