from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
import logging
from myapp.mqtt_handler import publish_control_command
from myapp.models import Device, TelemetryLog, N8NSettings
from myapp.n8n_service import notify_n8n_relay_command

logger = logging.getLogger(__name__)


def _relay_action_map():
    return {
        'all_on': {'relay1_pump': True, 'relay2_fan': True, 'relay3_heater': True},
        'all_off': {'relay1_pump': False, 'relay2_fan': False, 'relay3_heater': False},
        'pump_on': {'relay1_pump': True},
        'pump_off': {'relay1_pump': False},
        'fan_on': {'relay2_fan': True},
        'fan_off': {'relay2_fan': False},
        'heater_on': {'relay3_heater': True},
        'heater_off': {'relay3_heater': False},
    }


def landing_page(request):
    return render(request, 'myapp/landing.html')


@require_http_methods(["GET"])
def dashboard_data(request):
    """Provide dashboard snapshot (devices + latest telemetry)."""
    devices_payload = []

    for device in Device.objects.order_by('board_id'):
        latest_telemetry = (
            TelemetryLog.objects
            .filter(device=device)
            .order_by('-created_at')
            .first()
        )

        sensor_data = latest_telemetry.sensor_data if latest_telemetry else {}
        relay_status = latest_telemetry.relay_status if latest_telemetry else {}

        devices_payload.append({
            'board_id': device.board_id,
            'status': device.status,
            'ip_address': device.ip_address,
            'firmware_version': device.firmware_version,
            'last_seen': device.last_seen.isoformat() if device.last_seen else None,
            'latest_telemetry': {
                'created_at': latest_telemetry.created_at.isoformat() if latest_telemetry else None,
                'rssi': latest_telemetry.rssi if latest_telemetry else None,
                'sensor_data': sensor_data,
                'relay_status': relay_status,
            }
        })

    online_count = sum(1 for d in devices_payload if d['status'] == 'online')

    return JsonResponse({
        'success': True,
        'server_time': timezone.now().isoformat(),
        'summary': {
            'device_count': len(devices_payload),
            'online_count': online_count,
            'offline_count': len(devices_payload) - online_count,
        },
        'devices': devices_payload,
    })


@csrf_exempt
@require_http_methods(["POST"])
def send_control_command(request):
    """
    API endpoint to send control commands to ESP32 devices.
    
    Expected POST body:
    {
        "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
        "relays": {
            "relay1_pump": true,
            "relay2_fan": false,
            "relay3_heater": false
        }
    }
    
    Returns:
        JsonResponse with success status and message
    """
    try:
        # Parse request body
        data = json.loads(request.body)
        
        # Validate required fields
        board_id = data.get('board_id')
        relay_data = data.get('relays')
        
        if not board_id:
            return JsonResponse({
                'success': False,
                'error': 'board_id is required'
            }, status=400)
        
        if not relay_data or not isinstance(relay_data, dict):
            return JsonResponse({
                'success': False,
                'error': 'relays must be a valid dictionary'
            }, status=400)
        
        # Publish control command via MQTT
        success = publish_control_command(board_id, relay_data)

        notify_n8n_relay_command(
            source='dashboard_api',
            board_id=board_id,
            relays=relay_data,
            action='direct_relays',
            success=success,
            metadata={'endpoint': '/api/control/'},
        )
        
        if success:
            return JsonResponse({
                'success': True,
                'message': f'Control command sent to {board_id}',
                'relays': relay_data
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Failed to publish MQTT message'
            }, status=500)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON in request body'
        }, status=400)
    
    except Exception as e:
        logger.error(f"Error in send_control_command: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def n8n_relay_control(request):
    """
    Inbound webhook: n8n -> Dashboard -> MQTT Relay Control.

    Header auth (recommended):
      X-N8N-Token: <token>

    Expected payload (one of two modes):
    1) action mode:
    {
      "board_id": "ESP32-FARM-001",
      "action": "pump_on"
    }

    2) direct relays mode:
    {
      "board_id": "ESP32-FARM-001",
      "relays": {"relay1_pump": true, "relay2_fan": false, "relay3_heater": true}
    }
    """
    try:
        n8n_settings = N8NSettings.get_settings()

        if not n8n_settings.enable_inbound_webhook:
            return JsonResponse(
                {'success': False, 'error': 'Inbound webhook is disabled'},
                status=403,
            )

        configured_token = n8n_settings.inbound_auth_token or ''
        provided_token = (
            request.headers.get('X-N8N-Token')
            or request.POST.get('token')
            or request.GET.get('token')
            or ''
        )

        if configured_token and provided_token != configured_token:
            return JsonResponse({'success': False, 'error': 'Invalid token'}, status=401)

        data = json.loads(request.body)
        board_id = data.get('board_id')
        relays = data.get('relays')
        action = data.get('action')

        if not board_id:
            return JsonResponse({'success': False, 'error': 'board_id is required'}, status=400)

        if relays is None and not action:
            return JsonResponse(
                {'success': False, 'error': 'Provide either relays object or action'},
                status=400,
            )

        relay_payload = relays
        action_name = action or 'direct_relays'

        if relay_payload is None:
            relay_payload = _relay_action_map().get(action)
            if relay_payload is None:
                return JsonResponse(
                    {'success': False, 'error': f'Unsupported action: {action}'},
                    status=400,
                )

        if not isinstance(relay_payload, dict):
            return JsonResponse({'success': False, 'error': 'relays must be an object'}, status=400)

        success = publish_control_command(board_id, relay_payload)

        notify_n8n_relay_command(
            source='n8n_inbound_webhook',
            board_id=board_id,
            relays=relay_payload,
            action=action_name,
            success=success,
            metadata={'endpoint': '/api/n8n/relay-control/'},
        )

        if success:
            return JsonResponse(
                {
                    'success': True,
                    'message': f'Command sent to {board_id}',
                    'board_id': board_id,
                    'action': action_name,
                    'relays': relay_payload,
                }
            )

        return JsonResponse(
            {'success': False, 'error': 'Failed to publish MQTT message'},
            status=500,
        )
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON in request body'}, status=400)
    except Exception as exc:
        logger.error('Error in n8n_relay_control: %s', exc, exc_info=True)
        return JsonResponse({'success': False, 'error': str(exc)}, status=500)


@require_http_methods(["GET"])
def telemetry_history(request):
    """Return last N telemetry records for a device (oldest first for charting)."""
    board_id = request.GET.get('board_id', '').strip()
    if not board_id:
        return JsonResponse({'success': False, 'error': 'board_id is required'}, status=400)

    try:
        limit = min(int(request.GET.get('limit', 20)), 100)
    except (ValueError, TypeError):
        limit = 20

    logs = list(
        TelemetryLog.objects
        .filter(device_id=board_id)
        .order_by('-created_at')[:limit]
    )
    logs.reverse()  # oldest first so chart renders left-to-right

    history = [
        {
            'created_at': log.created_at.isoformat(),
            'rssi': log.rssi,
            'water_temp': log.sensor_data.get('water_temp'),
            'air_temp': log.sensor_data.get('air_temp'),
            'air_humidity': log.sensor_data.get('air_humidity'),
            'water_overflow': log.sensor_data.get('water_overflow'),
            'water_dry': log.sensor_data.get('water_dry'),
            'relay1_pump': log.relay_status.get('relay1_pump'),
            'relay2_fan': log.relay_status.get('relay2_fan'),
            'relay3_heater': log.relay_status.get('relay3_heater'),
        }
        for log in logs
    ]

    return JsonResponse({'success': True, 'history': history})
