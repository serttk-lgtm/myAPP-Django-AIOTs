"""
N8N integration service utilities.
Provides outbound event notifications from Dashboard/Admin to n8n.
"""
import logging
from django.utils import timezone
import requests
from myapp.models import N8NSettings

logger = logging.getLogger(__name__)


def _post_n8n_event(enabled, webhook_url, payload, disabled_message, missing_url_message):
    """Common outbound webhook sender for n8n integration events."""
    settings = N8NSettings.get_settings()

    if not enabled:
        return False, disabled_message

    if not webhook_url:
        return False, missing_url_message

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=settings.request_timeout_seconds,
        )

        if 200 <= response.status_code < 300:
            return True, f'Outbound webhook sent ({response.status_code})'

        logger.warning(
            'n8n outbound webhook failed: status=%s body=%s',
            response.status_code,
            response.text[:500],
        )
        return False, f'Outbound webhook failed with status {response.status_code}'
    except Exception as exc:
        logger.error('Failed to notify n8n webhook: %s', exc, exc_info=True)
        return False, f'Outbound webhook error: {exc}'


def notify_n8n_relay_command(source, board_id, relays, action, success, metadata=None):
    """
    Send relay command event to n8n outbound webhook.

    Returns:
        (sent: bool, message: str)
    """
    settings = N8NSettings.get_settings()

    payload = {
        'event_type': 'relay_command',
        'source': source,
        'board_id': board_id,
        'action': action,
        'success': success,
        'relays': relays,
        'timestamp': timezone.now().isoformat(),
        'metadata': metadata or {},
    }

    return _post_n8n_event(
        enabled=settings.enable_outbound_webhook,
        webhook_url=settings.outbound_webhook_url,
        payload=payload,
        disabled_message='Outbound relay webhook is disabled',
        missing_url_message='Outbound relay webhook URL is not configured',
    )


def notify_n8n_telemetry(board_id, rssi, sensor_data, relay_status, metadata=None):
    """Send telemetry event to n8n outbound webhook."""
    settings = N8NSettings.get_settings()

    payload = {
        'event_type': 'telemetry',
        'board_id': board_id,
        'rssi': rssi,
        'sensor_data': sensor_data,
        'relay_status': relay_status,
        'timestamp': timezone.now().isoformat(),
        'metadata': metadata or {},
    }

    return _post_n8n_event(
        enabled=settings.enable_telemetry_webhook,
        webhook_url=settings.telemetry_webhook_url,
        payload=payload,
        disabled_message='Telemetry webhook is disabled',
        missing_url_message='Telemetry webhook URL is not configured',
    )


def notify_n8n_device_status(board_id, status, ip_address, firmware_version, last_seen, metadata=None):
    """Send device status event to n8n outbound webhook."""
    settings = N8NSettings.get_settings()

    payload = {
        'event_type': 'device_status',
        'board_id': board_id,
        'status': status,
        'ip_address': ip_address,
        'firmware_version': firmware_version,
        'last_seen': last_seen.isoformat() if last_seen else None,
        'timestamp': timezone.now().isoformat(),
        'metadata': metadata or {},
    }

    return _post_n8n_event(
        enabled=settings.enable_device_status_webhook,
        webhook_url=settings.device_status_webhook_url,
        payload=payload,
        disabled_message='Device status webhook is disabled',
        missing_url_message='Device status webhook URL is not configured',
    )
