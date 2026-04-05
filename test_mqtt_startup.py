"""
Quick test script to verify MQTT Worker auto-start
Run this to see if AppConfig.ready() is triggered
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
os.environ['RUN_MAIN'] = 'true'  # Simulate Django auto-reloader

# Initialize Django
django.setup()

print("\n" + "="*60)
print("Django initialized successfully!")
print("="*60)

# Check if app is loaded
from django.apps import apps
myapp_config = apps.get_app_config('myapp')
print(f"✅ App loaded: {myapp_config.name}")
print(f"✅ AppConfig class: {myapp_config.__class__.__name__}")

# Give some time for MQTT thread to start
import time
print("\n⏳ Waiting 3 seconds for MQTT Worker to start...")
time.sleep(3)

print("\n✅ If you see '🚀 Starting MQTT Worker automatically...' above,")
print("   then auto-start is working!")
print("\n❌ If you DON'T see it, there might be an issue.")
print("\n💡 Check mqtt_worker.log file for details.")
print("="*60 + "\n")
