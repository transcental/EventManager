from slack_bolt import App
from slack_sdk import WebClient

from .env import env
from events.commands.create_event import handle_create_event_cmd
from events.views.create_event import handle_create_event_view
from events.buttons.approve_event import handle_approve_event_btn

from typing import Any, Callable

app = App(
    token=env.slack_bot_token,
    signing_secret=env.slack_signing_secret
)

# create a command
@app.command("/create-event")
def create_event(ack: Callable, body: dict[str, Any], client: WebClient):
    handle_create_event_cmd(ack, body, client)

# handle view callback
@app.view("create_event")
def create_event_view(ack: Callable, body: dict[str, Any], client: WebClient):
    handle_create_event_view(ack, body, client)

@app.action("approve-event")
def approve_event(ack: Callable, body: dict[str, Any], client: WebClient):
    handle_approve_event_btn(ack, body, client)