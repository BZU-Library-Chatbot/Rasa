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
        book_title = next((entity.get("value") for entity in entities if entity["entity"] == "book_title"), None)
        author = next((entity.get("value") for entity in entities if entity["entity"] == "author"), None)
        subject = next((entity.get("value") for entity in entities if entity["entity"] == "subject"), None)
        language = next((entity.get("value") for entity in entities if entity["entity"] == "language"), None)

        # Detect user language
        user_message = tracker.latest_message.get('text')
        detected_language = detect(user_message)
        
        # Load books data
        with open('./data/books.json') as f:
            books = json.load(f)

        # Filter books based on user query
        filtered_books = books
        if book_title:
            filtered_books = [book for book in filtered_books if book_title.lower() in book['Title'].lower()]
        if author:
            filtered_books = [book for book in filtered_books if any(author.lower() in a.lower() for a in book['Author'])]
        if subject:
            filtered_books = [book for book in filtered_books if any(subject.lower() in s.lower() for s in book['Subjects'])]
        if language:
            filtered_books = [book for book in filtered_books if book['Language'].lower() == language.lower()]

        # Get up to 10 random book recommendations from filtered books
        recommendations = filtered_books[:10]
        
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

        if len(recommendations) >= 0:    
            counter = 1
            for book in recommendations:
                print("book", book)
                if detected_language == 'ar':
                    response += f"{counter}. {book['Title']} للكاتب: {', '.join(book['Author'])}\n\n"
                else:
                    response += f"{counter}. {book['Title']} author: {', '.join(book['Author'])}\n\n"
                counter += 1


        dispatcher.utter_message(text=response)
        return []