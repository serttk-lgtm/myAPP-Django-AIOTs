from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from myapp.mqtt_handler import publish_control_command

logger = logging.getLogger(__name__)


def landing_page(request):
    return render(request, 'myapp/landing.html')


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
