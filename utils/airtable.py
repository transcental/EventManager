from pyairtable import Api
from datetime import datetime, timezone


class AirtableManager:
    def __init__(self, api_key: str, base_id: str):
        api = Api(api_key)
        self.events_table = api.table(base_id, "Events")
        print("Connected to Airtable")

    def create_event(
        self,
        title: str,
        description: str,
        start_time: str,
        end_time: str,
        host_name: str,
        host_pfp: str,
    ):
        event = self.events_table.create(
            {
                "Title": title,
                "Description": description,
                "Start Time": datetime.fromtimestamp(
                    start_time, timezone.utc
                ).isoformat(),
                "End Time": datetime.fromtimestamp(end_time, timezone.utc).isoformat(),
                "Leader": host_name,
                "Avatar": [{"url": host_pfp}],
                "Approved": False,
            }
        )
        return event

    def get_event(self, id: str):
        user = self.events_table.first(formula=f'{{id}} = "{id}"')
        return user

    def update_event(
        self,
        id: str | None = None,
        **updates: dict,
    ):
        event = self.events_table.update(id, updates)
        return event
