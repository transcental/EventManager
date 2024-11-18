from typing import Any, Callable
from slack_sdk import WebClient
from datetime import datetime, timezone

from utils.env import env


def handle_create_event_view(ack: Callable, body: dict[str, Any], client: WebClient):
    ack()
    view = body["view"]
    values = view["state"]["values"]
    title = (values["title"]["title"]["value"],)
    description = (values["description"]["description"]["value"],)
    start_time = (values["start_time"]["start_time"]["selected_date_time"],)
    end_time = (values["end_time"]["end_time"]["selected_date_time"],)
    host_id = values["host"]["host"]["selected_user"]

    user = client.users_info(user=host_id)
    host_name = user["user"]["real_name"]
    host_pfp = user["user"]["profile"]["image_192"]

    event = env.airtable.create_event(
        title[0], description[0], start_time[0], end_time[0], host_id, host_name, host_pfp
    )
    if not event:
        client.chat_postEphemeral(
            user=body["user"]["id"],
            channel=body["user"]["id"],
            text=f'An error occurred whilst creating the event "{title[0]}".',
        )

    fallback_start_time = datetime.fromtimestamp(
        start_time[0], timezone.utc
    ).isoformat()
    fallback_end_time = datetime.fromtimestamp(end_time[0], timezone.utc).isoformat()

    user_id = body.get("user", {}).get("id", "")
    host_mention = f"for <@{host_id}>" if host_id != user_id else ""
    host_str = f"<@{user_id}> {host_mention}"

    client.chat_postMessage(
        channel=env.slack_approval_channel,
        text=f"New event request by <@{body['user']['id']}>!\nTitle: {title[0]}\nDescription: {description[0]}\nStart Time: {start_time[0]}\nEnd Time: {end_time[0]}",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"New event request by {host_str}!\n*Title:* {title[0]}\n*Description:* {description[0]}\n*Start Time (local time):* <!date^{start_time[0]}^{{date_num}} at {{time_secs}}|{fallback_start_time}>\n*End Time (local time):* <!date^{end_time[0]}^{{date_num}} at {{time_secs}}|{fallback_end_time}>",
                },
            }
        ]
    )