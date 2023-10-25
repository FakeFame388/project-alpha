from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import json
import operator

class ActionGetProfName(Action):

     def name(self) -> Text:
         return "action_get_prof_name"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         file = open('departmentToProf.json')
         deptToProf = json.load(file)
         departmentName = tracker.get_slot('department')
         if (departmentName == None):
             dispatcher.utter_message(text="Sorry, but I could not find that department. May be you could retry.")
             return []
         list_of_profs = []
         for item in deptToProf:
             for key in item.keys():
                 if operator.contains(key, departmentName):
                     list_of_profs.append(item[key])
        
         if (len(list_of_profs) != 0):
             dispatcher.utter_message(text=f"The professors of the department {departmentName} are")
             for x in list_of_profs:
                 dispatcher.utter_message(x)

         list_of_profs.clear()
         return [SlotSet("department", None)]

class ActionGetContactDetails(Action):
     def name(self) -> Text:
         return "action_get_contact_details"
     def run(self,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
     ) -> List[Dict[Text, Any]]:
             file = open('contactDetails.json')
             contactDetails = json.load(file)
             profName = tracker.get_slot('profName')
             if (profName == None):
                 return []
             for item in contactDetails:
                 for key in item.keys():
                     if operator.contains(key, profName):
                         dispatcher.utter_message(text=f"The contact detail of the professor {profName} is {item[key]}")
             return [SlotSet(profName, None)]

class ActionGetEventDetails(Action):         def name(self) -> Text:                     return "action_get_event_details"                                           def run(self,                                   dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
     ) -> List[Dict[Text, Any]]:
             file = open('eventDetails.json')
             eventDetails = json.load(file)
             eventName = tracker.get_slot('eventName')
             if (len(eventName) == None):
                 return []
             for item in eventDetails:
                 for key in item.keys():
                     if operator.contains(key, eventName):
                         dispatcher.utter_message(item[key])
             return [SlotSet("eventName", None)]

class ActionGetDeptName(Action):
     def name(self) -> Text:                     return "action_get_dept_name"  
     def run(self,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
     ) -> List[Dict[Text, Any]]:
             file = open('profToDepartment.json')
             profToDept = json.load(file)
             profName = tracker.get_slot('profName')
             isNotProf = True
             if (profName != None):
                 for item in profToDept:
                     for key in item.keys():
                         if operator.contains(key, profName):
                             dispatcher.utter_message(text=f"The department of the professor {profName} is {item[key]}")
                             isNotProf = False
                             break
                 if isNotProf:
                     dispatcher.utter_message(text=f"Sorry, but as per my knowledge, professor {profName} is not a professor at IIT Bombay")
             else:
                 dispatcher.utter_message(text="Sorry, but I could not recognize the professor. May be you could retry.")
             return [SlotSet("profName", None)]

