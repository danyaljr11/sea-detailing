import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_admin_notification(event_type, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "admin_notifications",
        {
            "type": event_type,
            "message": json.dumps(data),
        },
    )
