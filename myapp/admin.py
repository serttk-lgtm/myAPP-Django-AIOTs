from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Device, TelemetryLog, RelayTestPanel, MQTTSettings
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
    
    def format_last_seen(self, obj):
        """Display last_seen in 24-hour format with seconds"""
        if obj.last_seen:
            local_time = timezone.localtime(obj.last_seen)
            return local_time.strftime('%Y-%m-%d %H:%M:%S')
        return '-'
    format_last_seen.short_description = 'Last Seen'
    format_last_seen.admin_order_field = 'last_seen'
    
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


@admin.register(MQTTSettings)
class MQTTSettingsAdmin(admin.ModelAdmin):
    """
    Admin interface for MQTT Settings.
    Allows configuration of broker, topics, and connection parameters.
    """
    fieldsets = (
        ('🌐 ตั้งค่า Broker', {
            'fields': ('broker', 'port', 'username', 'password'),
            'description': (
                'กำหนดค่าการเชื่อมต่อ MQTT Broker<br>'
                '<strong>หมายเหตุ:</strong> หลังบันทึกค่า ต้องรีสตาร์ตเซิร์ฟเวอร์ Django เพื่อให้มีผล'
            )
        }),
        ('📡 ตั้งค่า Topic', {
            'fields': ('telemetry_topic', 'status_topic', 'control_topic_pattern'),
            'description': (
                'กำหนดรูปแบบ Topic สำหรับรับและส่งข้อมูล<br>'
                '<strong>Wildcards:</strong> ใช้ <code>+</code> สำหรับ 1 ระดับ, ใช้ <code>#</code> สำหรับหลายระดับ<br>'
                '<strong>Placeholder:</strong> ใช้ <code>{board_id}</code> ใน <code>control_topic_pattern</code><br>'
                '<strong>ตัวอย่าง Topic แบบเต็ม:</strong><br>'
                '<code>smartfarm/{board_id}/telemetry</code><br>'
                '<code>smartfarm/{board_id}/status</code><br>'
                '<code>smartfarm/{board_id}/control</code>'
            )
        }),
        ('⚙️ ตั้งค่าขั้นสูง', {
            'fields': ('keepalive', 'qos'),
            'description': (
                'ตั้งค่าการเชื่อมต่อและระดับคุณภาพการส่งข้อความ (QoS)<br>'
                '<strong>QoS 0:</strong> ส่งอย่างมาก 1 ครั้ง - เร็วที่สุด แต่อาจมีข้อความหาย<br>'
                '<strong>QoS 1:</strong> ส่งอย่างน้อย 1 ครั้ง - การันตีการส่ง แต่อาจซ้ำ<br>'
                '<strong>QoS 2:</strong> ส่งแบบไม่ซ้ำ - ช้าที่สุดแต่แม่นยำที่สุด'
            )
        }),
        ('📅 ข้อมูล', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('updated_at',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        """Customize labels and help texts for Thai readability."""
        form = super().get_form(request, obj, change=change, **kwargs)

        form.base_fields['broker'].label = 'Broker'
        form.base_fields['broker'].help_text = 'ชื่อโฮสต์หรือ IP ของ MQTT Broker เช่น broker.hivemq.com'

        form.base_fields['port'].label = 'พอร์ต'
        form.base_fields['port'].help_text = 'พอร์ตที่ใช้เชื่อมต่อ เช่น 1883 (TCP) หรือ 8883 (SSL/TLS)'

        form.base_fields['username'].label = 'ชื่อผู้ใช้'
        form.base_fields['username'].help_text = 'กรอกเมื่อ Broker ต้องการยืนยันตัวตน (ถ้าไม่ใช้ให้เว้นว่าง)'

        form.base_fields['password'].label = 'รหัสผ่าน'
        form.base_fields['password'].help_text = 'กรอกเมื่อ Broker ต้องการยืนยันตัวตน (ถ้าไม่ใช้ให้เว้นว่าง)'

        form.base_fields['telemetry_topic'].label = 'Telemetry topic'
        form.base_fields['telemetry_topic'].help_text = (
            'Topic สำหรับรับข้อมูลเซ็นเซอร์ เช่น smartfarm/{board_id}/telemetry '
            'หรือ smartfarm/+/telemetry'
        )

        form.base_fields['status_topic'].label = 'Status topic'
        form.base_fields['status_topic'].help_text = (
            'Topic สำหรับรับสถานะอุปกรณ์ เช่น smartfarm/{board_id}/status '
            'หรือ smartfarm/+/status'
        )

        form.base_fields['control_topic_pattern'].label = 'Control topic pattern'
        form.base_fields['control_topic_pattern'].help_text = (
            'Topic สำหรับส่งคำสั่งควบคุม เช่น smartfarm/{board_id}/control '
            '(ระบบจะแทน {board_id} อัตโนมัติ)'
        )

        form.base_fields['keepalive'].label = 'Keepalive (วินาที)'
        form.base_fields['keepalive'].help_text = 'ช่วงเวลาที่ client ส่งสัญญาณคงการเชื่อมต่อ (วินาที)'

        form.base_fields['qos'].label = 'ระดับ QoS'
        form.base_fields['qos'].help_text = 'เลือกคุณภาพการส่งข้อความสำหรับการ subscribe topic'

        return form
    
    def save_model(self, request, obj, form, change):
        """Save settings and notify user to restart server"""
        from django.contrib import messages
        super().save_model(request, obj, form, change)
        messages.warning(
            request,
            '⚠️ บันทึก MQTT Settings สำเร็จแล้ว กรุณารีสตาร์ต Django server เพื่อให้ค่ามีผล '
            'โดยกด Ctrl+C แล้วรัน: python manage.py run_mqtt_worker'
        )
    
    def has_add_permission(self, request):
        """Only one settings record allowed"""
        return not MQTTSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of settings"""
        return False
    
    def changelist_view(self, request, extra_context=None):
        """Redirect to change form if settings exist"""
        if MQTTSettings.objects.exists():
            obj = MQTTSettings.objects.first()
            return HttpResponseRedirect(f'/admin/myapp/mqttsettings/{obj.pk}/change/')
        return super().changelist_view(request, extra_context=extra_context)
