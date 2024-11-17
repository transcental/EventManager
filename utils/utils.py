from .env import env

from slack_sdk import WebClient

client = WebClient(token=env.slack_bot_token)


def user_in_safehouse(user_id: str):
    sad_members = client.conversations_members(channel=env.slack_sad_channel)["members"]
    return user_id in sad_members