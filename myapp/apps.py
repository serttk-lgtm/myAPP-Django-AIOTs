import os
import threading
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class MyappConfig(AppConfig):
    name = 'myapp'
    mqtt_worker_started = False  # Class variable to track worker status
    mqtt_lock = threading.Lock()  # Thread lock for safety
    
    def ready(self):
        """
        Runs when Django starts. 
        Automatically starts MQTT worker in background thread.
        """
        # Prevent running twice during development (Django's auto-reloader runs code twice)
        if os.environ.get('RUN_MAIN') != 'true':
            return
        
        # Check if worker already started (singleton pattern)
        with MyappConfig.mqtt_lock:
            if MyappConfig.mqtt_worker_started:
                logger.warning("[MQTT] Worker already started - skipping duplicate initialization")
                return
            MyappConfig.mqtt_worker_started = True
        
        # Start MQTT worker in background thread
        from myapp.mqtt_handler import MQTTHandler
        from django.conf import settings
        
        def start_mqtt_worker():
            """Background thread function to run MQTT worker"""
            try:
                logger.info("[MQTT] Starting MQTT Worker automatically...")
                handler = MQTTHandler()
                
                # Connect to broker (settings are read inside connect method)
                handler.connect()
                handler.start()  # This will block in loop_forever()
            except Exception as e:
                logger.error(f"[MQTT] Worker failed to start: {e}", exc_info=True)
                # Reset flag on failure so it can be retried
                with MyappConfig.mqtt_lock:
                    MyappConfig.mqtt_worker_started = False
        
        # Start MQTT worker in daemon thread (will stop when Django stops)
        mqtt_thread = threading.Thread(target=start_mqtt_worker, daemon=True, name="MQTT-Worker")
        mqtt_thread.start()
        logger.info("[MQTT] Worker thread started successfully")
