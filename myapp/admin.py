from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Device, TelemetryLog, RelayTestPanel
from .mqtt_handler import publish_control_command


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Admin interface for Device model with relay control actions.
    """
    list_display = ('board_id', 'status', 'ip_address', 'firmware_version', 'format_last_seen')
    list_filter = ('status', 'firmware_version')
    search_fields = ('board_id', 'ip_address')
    readonly_fields = ('format_last_seen',)
    ordering = ('-last_seen',)
    actions = [
        'relay_all_on',
        'relay_all_off',
        'relay1_pump_on',
        'relay1_pump_off',
        'relay2_fan_on',
        'relay2_fan_off',
        'relay3_heater_on',
        'relay3_heater_off',
        'relay_test_sequence',
    ]
    
    def format_last_seen(self, obj):
        """Display last_seen in 24-hour format with seconds"""
        if obj.last_seen:
            local_time = timezone.localtime(obj.last_seen)
            return local_time.strftime('%Y-%m-%d %H:%M:%S')
        return '-'
    format_last_seen.short_description = 'Last Seen'
    format_last_seen.admin_order_field = 'last_seen'
    
    # ==================== Relay Control Actions ====================
    
    def relay_all_on(self, request, queryset):
        """Turn all relays ON for selected devices"""
        success_count = 0
        fail_count = 0
        
        for device in queryset:
            relay_data = {
                'relay1_pump': True,
                'relay2_fan': True,
                'relay3_heater': True
            }
            if publish_control_command(device.board_id, relay_data):
                success_count += 1
            else:
                fail_count += 1
        
        if success_count > 0:
            self.message_user(request, f'✅ ALL ON command sent to {success_count} device(s)', messages.SUCCESS)
        if fail_count > 0:
            self.message_user(request, f'❌ Failed to send to {fail_count} device(s)', messages.ERROR)
    relay_all_on.short_description = '🟢 Turn ALL Relays ON'
    
    def relay_all_off(self, request, queryset):
        """Turn all relays OFF for selected devices"""
        success_count = 0
        fail_count = 0
        
        for device in queryset:
            relay_data = {
                'relay1_pump': False,
                'relay2_fan': False,
                'relay3_heater': False
            }
            if publish_control_command(device.board_id, relay_data):
                success_count += 1
            else:
                fail_count += 1
        
        if success_count > 0:
            self.message_user(request, f'✅ ALL OFF command sent to {success_count} device(s)', messages.SUCCESS)
        if fail_count > 0:
            self.message_user(request, f'❌ Failed to send to {fail_count} device(s)', messages.ERROR)
    relay_all_off.short_description = '🔴 Turn ALL Relays OFF'
    
    def relay1_pump_on(self, request, queryset):
        """Turn Relay 1 (Pump) ON"""
        success_count = 0
        fail_count = 0
        
        for device in queryset:
            relay_data = {'relay1_pump': True}
            if publish_control_command(device.board_id, relay_data):
                success_count += 1
            else:
                fail_count += 1
        
        if success_count > 0:
            self.message_user(request, f'✅ PUMP ON sent to {success_count} device(s)', messages.SUCCESS)
        if fail_count > 0:
            self.message_user(request, f'❌ Failed to send to {fail_count} device(s)', messages.ERROR)
    relay1_pump_on.short_description = '💧 Relay 1 PUMP ON'
    
    def relay1_pump_off(self, request, queryset):
        """Turn Relay 1 (Pump) OFF"""
        success_count = 0
        fail_count = 0
        
        for device in queryset:
            relay_data = {'relay1_pump': False}
            if publish_control_command(device.board_id, relay_data):
                success_count += 1
            else:
                fail_count += 1
        
        if success_count > 0:
            self.message_user(request, f'✅ PUMP OFF sent to {success_count} device(s)', messages.SUCCESS)
        if fail_count > 0:
            self.message_user(request, f'❌ Failed to send to {fail_count} device(s)', messages.ERROR)
    relay1_pump_off.short_description = '💧 Relay 1 PUMP OFF'
    
    def relay2_fan_on(self, request, queryset):
        """Turn Relay 2 (Fan) ON"""
        success_count = 0
        fail_count = 0
        
        for device in queryset:
            relay_data = {'relay2_fan': True}
            if publish_control_command(device.board_id, relay_data):
                success_count += 1
            else:
                fail_count += 1
        
        if success_count > 0:
            self.message_user(request, f'✅ FAN ON sent to {success_count} device(s)', messages.SUCCESS)
        if fail_count > 0:
            self.message_user(request, f'❌ Failed to send to {fail_count} device(s)', messages.ERROR)
    relay2_fan_on.short_description = '🌀 Relay 2 FAN ON'
    
    def relay2_fan_off(self, request, queryset):
        """Turn Relay 2 (Fan) OFF"""
        success_count = 0
        fail_count = 0
        
        for device in queryset:
            relay_data = {'relay2_fan': False}
            if publish_control_command(device.board_id, relay_data):
                success_count += 1
            else:
                fail_count += 1
        
        if success_count > 0:
            self.message_user(request, f'✅ FAN OFF sent to {success_count} device(s)', messages.SUCCESS)
        if fail_count > 0:
            self.message_user(request, f'❌ Failed to send to {fail_count} device(s)', messages.ERROR)
    relay2_fan_off.short_description = '🌀 Relay 2 FAN OFF'
    
    def relay3_heater_on(self, request, queryset):
        """Turn Relay 3 (Heater) ON"""
        success_count = 0
        fail_count = 0
        
        for device in queryset:
            relay_data = {'relay3_heater': True}
            if publish_control_command(device.board_id, relay_data):
                success_count += 1
            else:
                fail_count += 1
        
        if success_count > 0:
            self.message_user(request, f'✅ HEATER ON sent to {success_count} device(s)', messages.SUCCESS)
        if fail_count > 0:
            self.message_user(request, f'❌ Failed to send to {fail_count} device(s)', messages.ERROR)
    relay3_heater_on.short_description = '🔥 Relay 3 HEATER ON'
    
    def relay3_heater_off(self, request, queryset):
        """Turn Relay 3 (Heater) OFF"""
        success_count = 0
        fail_count = 0
        
        for device in queryset:
            relay_data = {'relay3_heater': False}
            if publish_control_command(device.board_id, relay_data):
                success_count += 1
            else:
                fail_count += 1
        
        if success_count > 0:
            self.message_user(request, f'✅ HEATER OFF sent to {success_count} device(s)', messages.SUCCESS)
        if fail_count > 0:
            self.message_user(request, f'❌ Failed to send to {fail_count} device(s)', messages.ERROR)
    relay3_heater_off.short_description = '🔥 Relay 3 HEATER OFF'
    
    def relay_test_sequence(self, request, queryset):
        """Send test sequence: Turn all ON then all OFF"""
        import time
        success_count = 0
        fail_count = 0
        
        for device in queryset:
            # Turn all ON
            relay_on = {
                'relay1_pump': True,
                'relay2_fan': True,
                'relay3_heater': True
            }
            if publish_control_command(device.board_id, relay_on):
                time.sleep(0.5)  # Small delay between commands
                
                # Turn all OFF
                relay_off = {
                    'relay1_pump': False,
                    'relay2_fan': False,
                    'relay3_heater': False
                }
                if publish_control_command(device.board_id, relay_off):
                    success_count += 1
                else:
                    fail_count += 1
            else:
                fail_count += 1
        
        if success_count > 0:
            self.message_user(request, f'✅ Test sequence sent to {success_count} device(s)', messages.SUCCESS)
        if fail_count > 0:
            self.message_user(request, f'❌ Failed to send to {fail_count} device(s)', messages.ERROR)
    relay_test_sequence.short_description = '🧪 Test Sequence (ALL ON → ALL OFF)'
    
    # ==================== Custom Admin Views ====================
    
    def get_urls(self):
        """Add custom URL for relay control panel"""
        urls = super().get_urls()
        custom_urls = [
            path('relay-control/', self.admin_site.admin_view(self.relay_control_view), name='myapp_device_relay_control'),
        ]
        return custom_urls + urls
    
    def relay_control_view(self, request):
        """Relay Control Panel - Simple interface for testing relays"""
        # Get all online devices
        online_devices = Device.objects.filter(status='online').order_by('board_id')
        
        # Get selected device
        selected_device_id = request.GET.get('device')
        selected_device = None
        relay_status = None
        
        if selected_device_id:
            try:
                selected_device = Device.objects.get(board_id=selected_device_id)
                
                # Get latest telemetry to show current relay status
                latest_telemetry = TelemetryLog.objects.filter(
                    device=selected_device
                ).order_by('-created_at').first()
                
                if latest_telemetry and latest_telemetry.relay_status:
                    relay_status = latest_telemetry.relay_status
                    
            except Device.DoesNotExist:
                messages.error(request, f'Device {selected_device_id} not found')
        
        # Handle relay control actions
        if request.method == 'POST':
            action = request.POST.get('action')
            device_id = request.POST.get('device_id')
            
            if not device_id:
                messages.error(request, 'Please select a device first')
            else:
                relay_commands = {
                    'all_on': {'relay1_pump': True, 'relay2_fan': True, 'relay3_heater': True},
                    'all_off': {'relay1_pump': False, 'relay2_fan': False, 'relay3_heater': False},
                    'pump_on': {'relay1_pump': True},
                    'pump_off': {'relay1_pump': False},
                    'fan_on': {'relay2_fan': True},
                    'fan_off': {'relay2_fan': False},
                    'heater_on': {'relay3_heater': True},
                    'heater_off': {'relay3_heater': False},
                }
                
                if action in relay_commands:
                    if publish_control_command(device_id, relay_commands[action]):
                        messages.success(request, f'✅ Command {action.upper()} sent to {device_id}')
                    else:
                        messages.error(request, f'❌ Failed to send command to {device_id}')
                
                return HttpResponseRedirect(f'/admin/myapp/device/relay-control/?device={device_id}')
        
        context = {
            **self.admin_site.each_context(request),
            'title': 'Relay Control Panel',
            'online_devices': online_devices,
            'selected_device': selected_device,
            'relay_status': relay_status,
            'opts': self.model._meta,
        }
        
        return render(request, 'admin/myapp/relay_control.html', context)


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


@admin.register(RelayTestPanel)
class RelayTestPanelAdmin(admin.ModelAdmin):
    """
    Custom admin for Relay Test Panel menu item.
    Redirects to the relay control panel page.
    """
    
    def has_add_permission(self, request):
        """Disable add functionality"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Allow view access"""
        return True
    
    def has_delete_permission(self, request, obj=None):
        """Disable delete functionality"""
        return False
    
    def has_module_permission(self, request):
        """Show this in the admin index"""
        return True
    
    def changelist_view(self, request, extra_context=None):
        """Redirect to relay control panel"""
        return HttpResponseRedirect('/admin/myapp/device/relay-control/')
