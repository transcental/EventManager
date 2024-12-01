# Isabelle

> [!WARNING]
> # This project has moved to [hackclub/isabelle](https://github.com/hackclub/isabelle). This repository will **not** be updated and is now an archive.

Isabelle is a Slack bot for discovering events in the Hack Club Slack. It provides an easy way for SAD members to add events to the Hack Club [events website](https://events.hackclub.com), members to find events and RSVP to event.

## Usage

Run `/create-event` in the Hack Club Slack! If you're an authorised member (in the private SAD channel), you'll be shown a modal to fill out the event details. Once you submit the form, the event will be submitted for approval in a private channel.
Once the event is approved, it will be added to the Hack Club events website.

## Development

To run the bot locally, you'll need to set up a Slack app and will need access to the Airtable base. You'll need to set the following environment variables:

- `SLACK_SIGNING_SECRET` - _the signing secret for the Slack app. Found on the Slack app dashboard_
- `SLACK_BOT_TOKEN` - _the bot token for the Slack app. Found on the Slack app dashboard after authorising the app_
- `SLACK_SAD_CHANNEL` - _the ID of the private SAD channel. Get this from the channel URL_
- `SLACK_APPROVAL_CHANNEL`- _the ID of the channel events are sent to for approval. Get this from the channel URL_
- `AIRTABLE_API_KEY` - _the API key for the Airtable base. Get this from [here](https://airtable.com/create/tokens/new)_
- `AIRTABLE_BASE_ID` - _the ID of the Airtable base. Get this from the URL (begins with `app`)_
- `PORT` - _optional, defaults to 3000_

For the Slack app, here is the manifest you will need. Make sure to change the command and request URLs.

```json
{
    "display_information": {
        "name": "Event Manager"
    },
    "features": {
        "app_home": {
            "home_tab_enabled": true,
            "messages_tab_enabled": false,
            "messages_tab_read_only_enabled": true
        },
        "bot_user": {
            "display_name": "Event Manager",
            "always_online": false
        },
        "slash_commands": [
            {
                "command": "/create-event",
                "url": "https://cassiopeia3000.transcental.dev/slack/events",
                "description": "Create an event for events.hackclub.com",
                "should_escape": false
            }
        ]
    },
    "oauth_config": {
        "scopes": {
            "bot": [
                "chat:write",
                "chat:write.public",
                "commands",
                "groups:read",
                "users:read",
                "groups:history",
                "channels:history"
            ]
        }
    },
    "settings": {
        "event_subscriptions": {
            "request_url": "https://cassiopeia3000.transcental.dev/slack/events",
            "bot_events": [
                "app_home_opened"
            ]
        },
        "interactivity": {
            "is_enabled": true,
            "request_url": "https://cassiopeia3000.transcental.dev/slack/events"
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": false,
        "token_rotation_enabled": false
    }
}
```

To actually run the bot, you can use the following commands:

```bash
git clone https://github.com/DillonB07/EventManager
cd EventManager
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```
