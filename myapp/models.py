from django.db import models


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
 