# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from elasticsearch import Elasticsearch, exceptions as es_exceptions


class ActionSearchRole(Action):
    def name(self) -> Text:
        return "action_search_role"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        es = Elasticsearch([{ 'scheme':'http', 'host': 'localhost', 'port': 9200}])

        description= next(tracker.get_latest_entity_values("description"), None)
        if not description:
            dispatcher.utter_message(text="Sorry, I could not identify a description.")
            return []

        try:
            res = es.search(
                index="new3",
                body={
                    "query": {
                        "match": {
                            "Description": description
                        }
                    }
                }
            )

            if res["hits"]["total"]["value"] == 0:
                dispatcher.utter_message(text="Sorry, no records found for this name.")
                return []

            role = res["hits"]["hits"][0]["_source"]["Role"]
            score = res["hits"]["hits"][0]["_score"]

            dispatcher.utter_message(text=f"The role of {description} is {role} (score: {score})")

        except es_exceptions.ConnectionError:
            dispatcher.utter_message(text="Could not connect to ElasticSearch.")
            return []

        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while searching for the Description: {str(e)}")
            return []

        return []

