from django.contrib import admin
from django.utils import timezone
from .models import Device, TelemetryLog


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Admin interface for Device model.
    """
    list_display = ('board_id', 'status', 'ip_address', 'firmware_version', 'format_last_seen')
    list_filter = ('status', 'firmware_version')
    search_fields = ('board_id', 'ip_address')
    readonly_fields = ('format_last_seen',)
    ordering = ('-last_seen',)
    
    def format_last_seen(self, obj):
        """Display last_seen in 24-hour format with seconds"""
        if obj.last_seen:
            local_time = timezone.localtime(obj.last_seen)
            return local_time.strftime('%Y-%m-%d %H:%M:%S')
        return '-'
    format_last_seen.short_description = 'Last Seen'
    format_last_seen.admin_order_field = 'last_seen'


@admin.register(TelemetryLog)
class TelemetryLogAdmin(admin.ModelAdmin):
    """
    Admin interface for TelemetryLog model.
    """
    list_display = (
        'device', 
        'rssi', 
        'format_created_at', 
        'get_water_temp', 
        'get_air_temp', 
        'get_air_humidity',
        'get_water_overflow',
        'get_water_dry',
        'get_relay1_pump',
        'get_relay2_fan',
        'get_relay3_heater'
    )
    search_fields = ('device__board_id',)
    readonly_fields = ('device', 'rssi', 'sensor_data', 'relay_status', 'format_created_at')
    ordering = ('-created_at',)
    list_per_page = 50  # Show more records per page
    
    def format_created_at(self, obj):
        """Display created_at in 24-hour format with seconds"""
        if obj.created_at:
            local_time = timezone.localtime(obj.created_at)
            return local_time.strftime('%Y-%m-%d %H:%M:%S')
        return '-'
    format_created_at.short_description = 'Created At'
    format_created_at.admin_order_field = 'created_at'
    
    def get_water_temp(self, obj):
        """Display water temperature from sensor data"""
        return obj.sensor_data.get('water_temp', 'N/A')
    get_water_temp.short_description = 'Water Temp (°C)'
    
    def get_air_temp(self, obj):
        """Display air temperature from sensor data"""
        return obj.sensor_data.get('air_temp', 'N/A')
    get_air_temp.short_description = 'Air Temp (°C)'
    
    def get_air_humidity(self, obj):
        """Display air humidity from sensor data"""
        return obj.sensor_data.get('air_humidity', 'N/A')
    get_air_humidity.short_description = 'Humidity (%)'
    
    def get_water_overflow(self, obj):
        """Display water overflow status"""
        overflow = obj.sensor_data.get('water_overflow', None)
        return '✓' if overflow else '✗' if overflow is False else 'N/A'
    get_water_overflow.short_description = 'Overflow'
    
    def get_water_dry(self, obj):
        """Display water dry status"""
        dry = obj.sensor_data.get('water_dry', None)
        return '✓' if dry else '✗' if dry is False else 'N/A'
    get_water_dry.short_description = 'Dry'
    
    def get_relay1_pump(self, obj):
        """Display relay1 pump status"""
        status = obj.relay_status.get('relay1_pump', None)
        return '🟢 ON' if status else '🔴 OFF' if status is False else 'N/A'
    get_relay1_pump.short_description = 'Pump'
    
    def get_relay2_fan(self, obj):
        """Display relay2 fan status"""
        status = obj.relay_status.get('relay2_fan', None)
        return '🟢 ON' if status else '🔴 OFF' if status is False else 'N/A'
    get_relay2_fan.short_description = 'Fan'
    
    def get_relay3_heater(self, obj):
        """Display relay3 heater status"""
        status = obj.relay_status.get('relay3_heater', None)
        return '🟢 ON' if status else '🔴 OFF' if status is False else 'N/A'
    get_relay3_heater.short_description = 'Heater'
