from django.db import models
from django.core.exceptions import ValidationError


class Device(models.Model):
    """
    Represents an ESP32 device in the Smart Farm system.
    """
    board_id = models.CharField(max_length=255, unique=True, primary_key=True)
    status = models.CharField(
        max_length=20,
        choices=[('online', 'Online'), ('offline', 'Offline')],
        default='offline'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    firmware_version = models.CharField(max_length=50, null=True, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_seen']
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
    
    def __str__(self):
        return f"{self.board_id} ({self.status})"


class TelemetryLog(models.Model):
    """
    Logs telemetry data from devices including sensor readings and relay status.
    """
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='telemetry_logs'
    )
    rssi = models.IntegerField(help_text="WiFi signal strength")
    sensor_data = models.JSONField(
        help_text="JSON object containing sensor readings (water_temp, air_temp, air_humidity, water_overflow, water_dry)"
    )
    relay_status = models.JSONField(
        help_text="JSON object containing relay states (relay1_pump, relay2_fan, relay3_heater)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Telemetry Log'
        verbose_name_plural = 'Telemetry Logs'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['device', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.device.board_id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class RelayTestPanel(Device):
    """
    Proxy model for Relay Control Panel menu item.
    This is used to create a dedicated menu entry in Django Admin.
    """
    class Meta:
        proxy = True
        verbose_name = 'Relay Test Panel'
        verbose_name_plural = 'Relay Test Panel'


class MQTTSettings(models.Model):
    """
    MQTT Broker and Topic configuration settings.
    Only one settings record is allowed (Singleton pattern).
    """
    # Broker Settings
    broker = models.CharField(
        max_length=255,
        default='broker.hivemq.com',
        help_text='MQTT Broker hostname or IP address'
    )
    port = models.IntegerField(
        default=1883,
        help_text='MQTT Broker port (default: 1883 for TCP, 8883 for SSL)'
    )
    username = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='MQTT username (leave empty if not required)'
    )
    password = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='MQTT password (leave empty if not required)'
    )
    
    # Topic Settings
    telemetry_topic = models.CharField(
        max_length=255,
        default='smartfarm/+/telemetry',
        help_text='Topic pattern for receiving telemetry data (use + as wildcard)'
    )
    status_topic = models.CharField(
        max_length=255,
        default='smartfarm/+/status',
        help_text='Topic pattern for receiving device status (use + as wildcard)'
    )
    control_topic_pattern = models.CharField(
        max_length=255,
        default='smartfarm/{board_id}/control',
        help_text='Topic pattern for sending control commands (use {board_id} as placeholder)'
    )
    
    # Advanced Settings
    keepalive = models.IntegerField(
        default=60,
        help_text='Keepalive interval in seconds'
    )
    qos = models.IntegerField(
        default=0,
        choices=[
            (0, 'QoS 0 - At most once'),
            (1, 'QoS 1 - At least once'),
            (2, 'QoS 2 - Exactly once')
        ],
        help_text='Quality of Service level for subscriptions'
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'MQTT Setting'
        verbose_name_plural = 'MQTT Settings'
    
    def save(self, *args, **kwargs):
        """
        Singleton pattern - Allow only one settings record.
        """
        if not self.pk and MQTTSettings.objects.exists():
            raise ValidationError('Only one MQTT Settings record is allowed. Please edit the existing settings.')
        # Always use pk=1 for singleton
        self.pk = 1
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """
        Get or create the singleton MQTT settings instance.
        """
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
    
    def __str__(self):
        return f"MQTT Settings - {self.broker}:{self.port}"
 