from datetime import datetime, timezone

from utils.env import env
from utils.utils import user_in_safehouse

def get_home(user_id: str):
    sad_member = user_in_safehouse(user_id)
    admin = True if user_id in env.authorised_users else False
    events = env.airtable.get_all_events(unapproved=True if admin or sad_member else False)
    upcoming_events = [event for event in events if datetime.fromisoformat(event['fields']["Start Time"]) > datetime.now(timezone.utc)]
    upcoming_events_blocks = []
    for event in upcoming_events:
        upcoming_events_blocks.append({
        	"type": "divider"
	})
        fallback_time = datetime.fromisoformat(event['fields']["Start Time"]).strftime("%A, %B %d at %I:%M %p")
        formatted_time = f"<!date^{int(datetime.fromisoformat(event['fields']['Start Time']).timestamp())}^{{date_long_pretty}} at {{time}}|{fallback_time}>"
        upcoming_events_blocks.append({
        	"type": "section",
        	"text": {
				"type": "mrkdwn",
				"text": f"{'*[UNAPPROVED]:* ' if not event['fields'].get('Approved', False) else ''}*{event['fields']['Title']}* - <@{event['fields']['Leader Slack ID']}>\n{event['fields']['Description']}\n*{formatted_time}*"
			},
			"accessory": {
				"type": "image",
				"image_url": event['fields']['Avatar'][0]['url'],
				"alt_text": f"{event['fields']['Leader']} profile picture",
			}
		})
        buttons = []
        if admin and not event['fields'].get('Approved', False):
              buttons.append(
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Approve",
						"emoji": True
					},
                    "style": "primary",
					"value": event['id'],
					"action_id": "approve-event"
				})
        if user_id == event['fields']['Leader Slack ID'] or admin:
            buttons.append(
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Edit",
						"emoji": True
					},
					"value": "edit-event",
					"action_id": "edit-event"
				})
        if not user_id == event['fields']['Leader Slack ID']:
            buttons.append(
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "RSVP",
						"emoji": True
					},
					"value": "rsvp",
					"action_id": "rsvp"
				})
        if event['fields'].get('Approved', False):
            buttons.append({
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "More Info",
						"emoji": True
					},
					"value": "more-info",
					"action_id": "more-info"
				})
        upcoming_events_blocks.append({
			"type": "actions",
			"elements": [
				*buttons
			]
		})

    return {
		"type": "home",
		"blocks": [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": "Events",
					"emoji": True
				}
			},
			{
				"type": "actions",
				"elements": [{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Create Event" if sad_member else "Propose Event",
						"emoji": True
					},
					"value": "host-event",
					"action_id": "create-event" if sad_member else "propose-event"
				}
				],
			},
			*upcoming_events_blocks,
			{
				"type": "divider"
			}
		]
	}