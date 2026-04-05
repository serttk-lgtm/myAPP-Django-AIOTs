"""
MQTT Handler for Smart Farm AIoT System
Handles incoming MQTT messages from ESP32 devices and updates database.
"""
import json
import logging
from datetime import datetime
import requests
import paho.mqtt.client as mqtt
from django.conf import settings
from django.utils import timezone
from myapp.models import Device, TelemetryLog, MQTTSettings

logger = logging.getLogger(__name__)


class MQTTHandler:
    """
    Manages MQTT connection and message processing for Smart Farm devices.
    """
    
    def __init__(self):
        # Get MQTT settings from database
        self.mqtt_settings = MQTTSettings.get_settings()
        
        # Use unique client_id and clean_session to prevent duplicate subscriptions
        import uuid
        client_id = f"django_smartfarm_{uuid.uuid4().hex[:8]}"
        self.client = mqtt.Client(client_id=client_id, clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # Set username and password if provided
        if self.mqtt_settings.username and self.mqtt_settings.password:
            self.client.username_pw_set(self.mqtt_settings.username, self.mqtt_settings.password)
    
    def on_connect(self, client, userdata, flags, rc):
        """
        Callback when client connects to MQTT broker.
        """
        if rc == 0:
            logger.info(f"Connected to MQTT broker successfully (Client ID: {client._client_id.decode() if hasattr(client._client_id, 'decode') else client._client_id})")
            
            # Subscribe to topics from settings with configured QoS
            client.subscribe(self.mqtt_settings.telemetry_topic, qos=self.mqtt_settings.qos)
            client.subscribe(self.mqtt_settings.status_topic, qos=self.mqtt_settings.qos)
            
            logger.info(f"Subscribed to topics: {self.mqtt_settings.telemetry_topic}, {self.mqtt_settings.status_topic} (QoS {self.mqtt_settings.qos})")
        else:
            logger.error(f"Failed to connect to MQTT broker with code: {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        """
        Callback when client disconnects from MQTT broker.
        """
        if rc != 0:
            logger.warning(f"Unexpected disconnection from MQTT broker. Code: {rc}")
        else:
            logger.info("Disconnected from MQTT broker")
    
    def on_message(self, client, userdata, msg):
        """
        Callback when a message is received from MQTT broker.
        Processes telemetry and status messages.
        """
        try:
            topic = msg.topic
            payload_str = msg.payload.decode('utf-8')
            payload = json.loads(payload_str)
            
            logger.debug(f"Received message on topic: {topic}")
            logger.debug(f"Payload: {payload}")
            
            # Extract board_id from payload or topic
            board_id = payload.get('board_id')
            if not board_id:
                # Try to extract from topic: smartfarm/<board_id>/...
                topic_parts = topic.split('/')
                if len(topic_parts) >= 2:
                    board_id = topic_parts[1]
            
            if not board_id:
                logger.error("Could not determine board_id from message")
                return
            
            # Route message based on topic type
            if topic.endswith('/status'):
                self.handle_status_message(board_id, payload)
            elif topic.endswith('/telemetry'):
                self.handle_telemetry_message(board_id, payload)
            else:
                logger.warning(f"Unknown topic type: {topic}")
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON payload: {e}")
        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}", exc_info=True)
    
    def handle_status_message(self, board_id, payload):
        """
        Processes status messages and updates Device model.
        Only updates devices that are already registered in the system.
        """
        try:
            # Check if device exists (don't auto-create)
            try:
                device = Device.objects.get(board_id=board_id)
            except Device.DoesNotExist:
                logger.warning(f"Received status from unregistered device: {board_id}. Please add device via Admin first.")
                return
            
            # Update existing device
            device.status = payload.get('status', 'offline')
            device.ip_address = payload.get('ip')
            device.firmware_version = payload.get('firmware')
            device.save()
            
            logger.debug(f"Updated device: {board_id} with status {device.status}")
        
        except Exception as e:
            logger.error(f"Error updating device status: {e}", exc_info=True)
    
    def handle_telemetry_message(self, board_id, payload):
        """
        Processes telemetry messages and creates TelemetryLog entries.
        Also triggers n8n webhook for water overflow alerts.
        Only processes messages from devices that are already registered.
        """
        try:
            # Check if device exists (don't auto-create)
            try:
                device = Device.objects.get(board_id=board_id)
            except Device.DoesNotExist:
                logger.warning(f"Received telemetry from unregistered device: {board_id}. Please add device via Admin first.")
                return
            
            # Update last_seen timestamp
            device.save(update_fields=['last_seen'])
            
            # Extract sensor and relay data with safe defaults
            sensors = payload.get('sensors', {})
            relays = payload.get('relays', {})
            rssi = payload.get('rssi', 0)
            
            # Create telemetry log entry
            telemetry_log = TelemetryLog.objects.create(
                device=device,
                rssi=rssi,
                sensor_data=sensors,
                relay_status=relays
            )
            
            logger.debug(f"Created telemetry log for {board_id}")
            
            # Check for water overflow and trigger n8n webhook
            if sensors.get('water_overflow') is True:
                self.trigger_n8n_alert(board_id, payload)
        
        except Exception as e:
            logger.error(f"Error processing telemetry: {e}", exc_info=True)
    
    def trigger_n8n_alert(self, board_id, payload):
        """
        Sends HTTP POST request to n8n webhook when water overflow is detected.
        """
        try:
            webhook_url = getattr(settings, 'N8N_WEBHOOK_URL', None)
            
            if not webhook_url:
                logger.warning("N8N_WEBHOOK_URL not configured in settings")
                return
            
            # Prepare alert payload
            alert_data = {
                'alert_type': 'water_overflow',
                'board_id': board_id,
                'timestamp': datetime.now().isoformat(),
                'payload': payload
            }
            
            # Send POST request to n8n
            response = requests.post(
                webhook_url,
                json=alert_data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully sent water overflow alert for {board_id} to n8n")
            else:
                logger.warning(f"n8n webhook returned status {response.status_code}")
        
        except requests.RequestException as e:
            logger.error(f"Failed to send n8n alert: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending n8n alert: {e}", exc_info=True)
    
    def connect(self):
        """
        Connects to MQTT broker.
        """
        try:
            # Get broker settings from database
            mqtt_settings = MQTTSettings.get_settings()
            
            logger.info(f"Connecting to MQTT broker at {mqtt_settings.broker}:{mqtt_settings.port}")
            self.client.connect(mqtt_settings.broker, mqtt_settings.port, mqtt_settings.keepalive)
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}", exc_info=True)
            raise
    
    def start(self):
        """
        Starts the MQTT client loop.
        """
        logger.info("Starting MQTT client loop")
        self.client.loop_forever()
    
    def stop(self):
        """
        Stops the MQTT client loop and disconnects.
        """
        logger.info("Stopping MQTT client")
        # Unsubscribe from topics using settings
        try:
            mqtt_settings = MQTTSettings.get_settings()
            self.client.unsubscribe(mqtt_settings.telemetry_topic)
            self.client.unsubscribe(mqtt_settings.status_topic)
        except Exception as e:
            logger.warning(f"Error unsubscribing: {e}")
        self.client.loop_stop()
        self.client.disconnect()


# Module-level function to publish control commands
def publish_control_command(board_id, relay_data):
    """
    Publishes a control command to a specific device.
    
    Args:
        board_id: The target device board ID
        relay_data: Dictionary containing relay states
    
    Returns:
        Boolean indicating success or failure
    """
    try:
        import time
        
        # Get MQTT settings from database
        mqtt_settings = MQTTSettings.get_settings()
        
        client = mqtt.Client()
        
        # Set credentials if available
        if mqtt_settings.username and mqtt_settings.password:
            client.username_pw_set(mqtt_settings.username, mqtt_settings.password)
        
        # Connect to broker using settings
        client.connect(mqtt_settings.broker, mqtt_settings.port, mqtt_settings.keepalive)
        
        # Start network loop to handle message sending
        client.loop_start()
        
        # Prepare control payload
        control_payload = {
            'command': 'relay_control',
            'relays': relay_data
        }
        
        # Build topic from pattern (replace {board_id} with actual board_id)
        topic = mqtt_settings.control_topic_pattern.replace('{board_id}', board_id)
        logger.info(f"Publishing to {topic}: {control_payload}")
        
        # Publish with QoS 1 for guaranteed delivery
        msg_info = client.publish(topic, json.dumps(control_payload), qos=1)
        
        # Wait for message to be published (max 2 seconds)
        msg_info.wait_for_publish(timeout=2.0)
        
        # Give time for message to be sent
        time.sleep(0.5)
        
        # Stop loop and disconnect
        client.loop_stop()
        client.disconnect()
        
        if msg_info.is_published():
            logger.info(f"✅ Successfully published control command to {board_id}")
            return True
        else:
            logger.error(f"❌ Failed to publish control command to {board_id}")
            return False
    
    except Exception as e:
        logger.error(f"Error publishing control command: {e}", exc_info=True)
        return False
