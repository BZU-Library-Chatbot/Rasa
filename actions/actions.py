import pandas as pd;
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

# actions.py
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from langdetect import detect
import json
from typing import Any, Text, Dict, List

class ActionDefaultFallback(Action):

    def name(self) -> str:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_message = tracker.latest_message.get('text', '')

        try:
            language = detect(user_message)
        except:
            language = 'en'  # Default to English if detection fails

        if language == 'ar':
            dispatcher.utter_message(text="عذراً، لم أفهم ذلك. هل يمكنك إعادة صياغتها؟")
        else:
            dispatcher.utter_message(text="I'm sorry, I didn't quite understand that. Can you please rephrase?")
        
        return []

class ActionProvideBookRecommendation(Action):
    def name(self) -> str:
        return "action_provide_book_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        # Extract entities from user query
        entities = tracker.latest_message.get("entities", [])
        author = next((entity.get("value") for entity in entities if entity["entity"] == "author"), None)
        subject = next((entity.get("value") for entity in entities if entity["entity"] == "subject"), None)
        language = next((entity.get("value") for entity in entities if entity["entity"] == "language"), None)
        print(f"Author: {author}, Subject: {subject}, Language: {language}")
        
        # Detect user language
        user_message = tracker.latest_message.get('text')
        detected_language = detect(user_message)

        # Load books data into a pandas DataFrame
        with open('./data/books.json', 'r', encoding='utf-8') as f:
            books = json.load(f)
        
        df = pd.DataFrame(books)

        # Filter books based on the combination of criteria provided
        if author:
            df = df[df['Author'].str.contains(author, case=False, na=False)]
        if subject:
            df = df[df['Subjects'].apply(lambda x: any(subject.lower() in s.lower() for s in x) or subject.lower() in df['Title'].str.lower().values)]
        if language:
            if "عربي" in language:
                language = "ar"
            elif "انجليزي" in language:
                language = "en"
            df = df[df['language'].str.lower() == language[:2].lower()]

        # Get up to 10 book recommendations
        recommendations = df.head(10).to_dict(orient='records')

        # Generate response
        if detected_language == 'ar' and len(recommendations) > 0:
            response = "إليك بعض توصيات الكتب:\n\n"
        elif detected_language == 'en' and len(recommendations) > 0:
            response = "Here are some book recommendations:\n\n"
        else:
            if detected_language == 'ar':
                response = "آسف، لم أتمكن من العثور على توصيات لكتب تناسب طلبك."
            else:
                response = "Sorry, I couldn't find any book recommendations that match your request."

        if len(recommendations) > 0:    
            counter = 1
            for book in recommendations:
                if detected_language == 'ar':
                    response += f"{counter}. {book['Title']} للكاتب: {book['Author']}\n\n"
                else:
                    response += f"{counter}. {book['Title']} author: {book['Author']}\n\n"
                counter += 1

        dispatcher.utter_message(text=response)
        return []