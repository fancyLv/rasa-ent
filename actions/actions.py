# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Text, List

from rasa_sdk import Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.types import DomainDict
from requests import ConnectionError, HTTPError, TooManyRedirects, Timeout

from actions.third_ent import get_basic_info, get_hot_news, get_negative_info


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
        dispatcher.utter_message(generate_message(company, type))
        return [SlotSet('type', None)]


def generate_message(company, type):
    if type in ('热点新闻', '新闻', '热点', '新闻舆情', '舆情'):
        try:
            result = get_hot_news(company)
            if result:
                text_message = f"""热点新闻：{result['title']}  {result['time']}\n{result['link']}"""
            else:
                text_message = "暂无信息"
        except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
            text_message = "{}".format(e)

    elif type in ('信息', '基本信息', '工商信息', '工商基本信息'):
        try:
            result = get_basic_info(company)
            if result:
                text_message = "\n".join(f"{key}：{result[key]}" for key in result if key != 'pid')
            else:
                text_message = "暂无信息"
        except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
            text_message = "{}".format(e)
    elif type in ['企业负面', '负面', '负面信息', '处罚', '失信']:
        try:
            result = get_negative_info(company)
            if result:
                text_message = "\n".join(f"{key}：{result[key]}" for key in result)
            else:
                text_message = "暂无信息"
        except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
            text_message = "{}".format(e)
    else:
        text_message = f"暂不支持查询{type}"
    return text_message
