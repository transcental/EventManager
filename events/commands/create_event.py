from slack_sdk import WebClient

from views.create_event import get_create_event_modal
from utils.env import env

from typing import Any, Callable

def handle_create_event_cmd(ack: Callable, body: dict[str, Any], client: WebClient):
    ack()
    print(f'Called by {body["user_id"]}')
    sad_members = client.conversations_members(channel=env.slack_sad_channel)["members"]

    if body["user_id"] not in sad_members:
        client.chat_postEphemeral(
            channel=body["channel_id"],
            user=body["user_id"],
            text="You are not authorised to create events."
        )
        return

    client.views_open(
        view=get_create_event_modal(),
        trigger_id=body["trigger_id"]
    )
