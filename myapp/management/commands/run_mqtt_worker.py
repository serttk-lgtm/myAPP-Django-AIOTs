"""
Django management command to run MQTT worker.
Usage: python manage.py run_mqtt_worker
"""
import logging
import signal
import sys
from django.core.management.base import BaseCommand
from myapp.mqtt_handler import MQTTHandler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Runs the MQTT worker to listen for messages from ESP32 devices'
    
    def __init__(self):
        super().__init__()
        self.mqtt_handler = None
    
    def handle(self, *args, **options):
        """
        Main entry point for the management command.
        """
        self.stdout.write(self.style.SUCCESS('Starting MQTT Worker...'))
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Initialize and start MQTT handler
            self.mqtt_handler = MQTTHandler()
            self.mqtt_handler.connect()
            
            self.stdout.write(self.style.SUCCESS('✓ MQTT Worker connected and listening'))
            self.stdout.write(self.style.WARNING('Press Ctrl+C to stop'))
            
            # Start the MQTT loop (blocking)
            self.mqtt_handler.start()
        
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nReceived keyboard interrupt'))
            self.shutdown()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            logger.error(f"MQTT Worker error: {e}", exc_info=True)
            sys.exit(1)
    
    def signal_handler(self, sig, frame):
        """
        Handles shutdown signals for graceful termination.
        """
        self.stdout.write(self.style.WARNING(f'\nReceived signal {sig}'))
        self.shutdown()
    
    def shutdown(self):
        """
        Performs graceful shutdown of MQTT worker.
        """
        self.stdout.write(self.style.WARNING('Shutting down MQTT Worker...'))
        
        if self.mqtt_handler:
            try:
                self.mqtt_handler.stop()
                self.stdout.write(self.style.SUCCESS('✓ MQTT Worker stopped gracefully'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error during shutdown: {e}'))
        
        sys.exit(0)
