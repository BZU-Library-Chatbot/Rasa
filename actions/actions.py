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

        # Load books data
        with open('./data/books.json', 'r', encoding='utf-8') as f:
            books = json.load(f)

        # Initial filtered books is all books
        all_books = books
        filtered_books = []
        # Filter books based on the combination of criteria provided
        if author and subject and language:
            filtered_books = [book for book in books if 
                              'Author' in book and author.lower() in book['Author'].lower() and
                              (any(subject.lower() in s.lower() for s in book['Subjects']) or subject.lower() in book['Title'].lower()) and
                              book['language'].lower() == language[:2].lower()]
        elif author and subject:
            filtered_books = [book for book in books if 
                              'Author' in book and author.lower() in book['Author'].lower() and
                              (any(subject.lower() in s.lower() for s in book['Subjects']) or subject.lower() in book['Title'].lower())]
        elif author and language:
            filtered_books = [book for book in books if 
                              'Author' in book and author.lower() in book['Author'].lower() and
                              book['language'].lower() == language[:2].lower()]
        elif subject and language:
            filtered_books = [book for book in books if 
                              (any(subject.lower() in s.lower() for s in book['Subjects']) or subject.lower() in book['Title'].lower()) and
                              book['language'].lower() == language[:2].lower()]
        elif author:
            filtered_books = [book for book in books if 'Author' in book and author.lower() in book['Author'].lower()]
        elif subject:
            for book in books:
                if book['language'] == "ar":
                    print(f"book: {book['Title']}")
            filtered_books = [book for book in books if any(subject.lower() in s.lower() for s in book['Subjects']) or subject.lower() in book['Title'].lower()]
        elif language:
            if("عربي" in language):
                language = "ar"
            elif("انجليزي" in language):
                language = "en"
            filtered_books = [book for book in books if book['language'].lower() == language[:2].lower()]

        # Get up to 10 book recommendations from filtered books
        recommendations = filtered_books[:10]

        # If recommendations are less than 10, tokenize the subject and search for each token
        if len(recommendations) < 10 and subject:
            tokens = subject.split()
            for token in tokens:
                additional_books = [book for book in all_books if token.lower() in book['Title'].lower() or any(token.lower() in s.lower() for s in book['Subjects'])]
                # Add books to recommendations without duplicating
                for book in additional_books:
                    if book not in recommendations:
                        recommendations.append(book)
                        if len(recommendations) >= 10:
                            break
                if len(recommendations) >= 10:
                    break

        # If recommendations are still less than 10, tokenize the author and search for each token
        if len(recommendations) < 10 and author:
            tokens = author.split()
            for token in tokens:
                additional_books = [book for book in all_books if token.lower() in book['Author'].lower()]
                # Add books to recommendations without duplicating
                for book in additional_books:
                    if book not in recommendations:
                        recommendations.append(book)
                        if len(recommendations) >= 10:
                            break
                if len(recommendations) >= 10:
                    break

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