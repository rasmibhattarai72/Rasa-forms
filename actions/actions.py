from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

account_balances = {
    "aaaaa": ['9811111111', 6000],
    "bbbbb": ['9822222222', 5000],
    "ccccc": ['9833333333', 3000],
    "ddddd": ['9844444444', 2000],
    "eeeee": ['9855555555', 1000]
}

transaction_records = {
    "aaaaa": [
        {"date": "2022-01-01", "description": "Salary Credit", "amount": 20000},
        {"date": "2022-01-10", "description": "Grocery Shopping", "amount": -1500},
        {"date": "2022-01-15", "description": "Rent Payment", "amount": -6000}
    ],
    "bbbbb": [
        {"date": "2022-01-01", "description": "Salary Credit", "amount": 15000},
        {"date": "2022-01-10", "description": "Grocery Shopping", "amount": -2000},
        {"date": "2022-01-15", "description": "Rent Payment", "amount": -5000}
    ],
    "ccccc": [
        {"date": "2022-01-01", "description": "Salary Credit", "amount": 10000},
        {"date": "2022-01-10", "description": "Grocery Shopping", "amount": -1000},
        {"date": "2022-01-15", "description": "Rent Payment", "amount": -4000}
    ],
    "ddddd": [
        {"date": "2022-01-01", "description": "Salary Credit", "amount": 8000},
        {"date": "2022-01-10", "description": "Grocery Shopping", "amount": -500},
        {"date": "2022-01-15", "description": "Rent Payment", "amount": -3000}
    ],
    "eeeee": [
        {"date": "2022-01-01", "description": "Salary Credit", "amount": 5000},
        {"date": "2022-01-10", "description": "Grocery Shopping", "amount": -700},
        {"date": "2022-01-15", "description": "Rent Payment", "amount": -4000}
    ]
}


class ValidateSimpleBankForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_bank_form"

    def validate_account_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:


        latest_intent = tracker.latest_message['intent'].get('name')
        #if (latest_intent == "check_balance"):
            #ab = "balance"
        #else:
            #ab = "transaction history"

        acc = tracker.get_slot("account_number")
        if acc not in account_balances.keys():
            dispatcher.utter_message(
                text=f"please provide your valid account number")
            return {"account_number": None}
        else:

            dispatcher.utter_message(
                text=f'Account number: {acc}')

            return {"account_number": acc}

    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        phone = tracker.get_slot("phone_number")
        acc = tracker.get_slot("account_number")

        latest_intent = tracker.latest_message['intent'].get('name')

        def check_phone_number(account_number, phone_number):
            if account_number in account_balances:
                stored_phone_number = account_balances[account_number][0]
                if stored_phone_number == phone_number:
                    a = True
                else:
                    a = False
                return a

        check = check_phone_number(acc, phone)

        if check == False:
            dispatcher.utter_message(
                text=f"Please provide correct phone number")
            return {"phone_number": None}

        else:
            dispatcher.utter_message(
                text=f'Phone Number: {phone}')
            return ["phone_number", phone]


class ActionGetAccountBalance(Action):
    def name(self) -> Text:
        return "action_get_account_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        acc = tracker.get_slot("account_number")
        phone = tracker.get_slot("phone_number")

        def get_acc_balance(account_number):
            if account_number in account_balances:
                m = account_balances[account_number][1]
            else:
                m = None
            return m

        balance = get_acc_balance(acc)
        print(f'The balance is {balance}')
        dispatcher.utter_message(
            text=f"The account balance of account number {acc} and phone {phone} is {balance}.")
        return []


class ActionCheckTransactionHistory(Action):
    def name(self) -> Text:
        return "action_check_transaction_history"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #latest_intent = tracker.latest_message['intent'].get('name')
        acc = tracker.get_slot("account_number")
        phone = tracker.get_slot("phone_number")

        #if latest_intent == "check_transaction_history":

        def get_trans_history(account_number):
            if account_number in transaction_records:
                m = transaction_records[account_number]
            else:
                m = None
            return m

        records = get_trans_history(acc)

        dispatcher.utter_message(
            text=f"The transaction history of account number {acc} and phone number {phone} are as follows: {records}.")
        
        return []
        
        
        # elif latest_intent == "check_balance":
        #     def get_acc_balance(account_number):
        #         if account_number in account_balances:
        #             m = account_balances[account_number][1]
        #         else:
        #             m = None
        #         return m

        #     balance = get_acc_balance(acc)
        #     print(f'The balance is {balance}')
        #     dispatcher.utter_message(
        #         text=f"The account balance of {acc} is {balance}.")

        
