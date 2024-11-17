from slack_sdk import WebClient

from views.create_event import get_create_event_modal
from utils.env import env
from utils.utils import user_in_safehouse

from typing import Any, Callable


def handle_create_event_cmd(ack: Callable, body: dict[str, Any], client: WebClient):
    ack()
    sad_member = user_in_safehouse(body["user_id"])

    if not sad_member:
        client.chat_postEphemeral(
            channel=body["channel_id"],
            user=body["user_id"],
            text="You are not authorised to create events.",
        )
        return

    client.views_open(view=get_create_event_modal(), trigger_id=body["trigger_id"])
