from slack_sdk import WebClient

from utils.env import env

from typing import Any, Callable

def handle_approve_event_btn(ack: Callable, body: dict[str, Any], client: WebClient):
    ack()
    user_id = body["user"]["id"]
    ts = body["message"]["ts"]
    if user_id not in env.authorised_users:
        client.chat_postEphemeral(
            user=user_id,
            channel=user_id,
            text="You are not authorised to approve events."
        )
        return
    value = body['actions'][0]['value']

    event = env.airtable.update_event(value, **{'Approved': True})

    if not event:
        client.chat_postEphemeral(
            user=body["user"]["id"],
            channel=body["user"]["id"],
            text=f'An error occurred whilst approving the event with id `{value}`.'
        )
        return
    
    message = client.conversations_history(
        channel=env.slack_approval_channel,
        latest=ts,
        limit=1,
        inclusive=True,
        
    )
    blocks =[ message['messages'][0]['blocks'][0], 
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Approved by <@{user_id}>"
                }
            ]
        }
    
    ]
    client.chat_update(
        channel=env.slack_approval_channel,
        ts=ts,
        blocks=blocks,
        text=body['message']['text']
        )   
