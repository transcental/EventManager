from slack_sdk import WebClient

from views.propose_event import get_propose_event_modal

from typing import Any, Callable


def handle_propose_event_btn(ack: Callable, body: dict[str, Any], client: WebClient):
    ack()
    client.views_open(view=get_propose_event_modal(), trigger_id=body["trigger_id"])
