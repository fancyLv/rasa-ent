# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class EntForm(FormAction):

    def name(self) -> Text:
        return "ent_form"

    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["company", "type"]

    async def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> List[EventType]:
        company = tracker.get_slot('company')
        type = tracker.get_slot('type')
        print(type)
        dispatcher.utter_message(f"{company} {type}")
        return []
