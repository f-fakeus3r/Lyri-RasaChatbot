# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from rasa_sdk.events import AllSlotsReset
from pymongo import MongoClient


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_lyrics"
        

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        api_adress='https://api.lyrics.ovh/v1/'
        artist = str(tracker.get_slot("artist_name"))
        print(artist)
        nartist = str(artist.replace(" ", "%20"))
        nartist = str(nartist.replace("-", ""))

        song = str(tracker.get_slot("song_name"))
        print(song)
        nsong = str(song.replace(" ", "%20"))
        nsong = str(nsong.replace("+", ""))
        url = api_adress + nartist + '/' + nsong


        json_data = requests.get(url).json()
        
        for i in json_data:
            if i == 'lyrics':
                Lyrics = json_data['lyrics']
                Lyrics = Lyrics.replace("Paroles de la chanson", "")
                Lyrics = Lyrics.replace("par", " - ")
                dispatcher.utter_message(text="Espero que essa seja a letra que você estava procurando:")
                dispatcher.utter_message(text=f"{Lyrics}")
            else:
                Lyrics = json_data['error']
                dispatcher.utter_message(text=f"Essa música não foi encontrada no nosso banco de dados :(")
                dispatcher.utter_message(text="Tem certeza que você digitou corretamente?")

        client = MongoClient("mongodb+srv://fake:db123_@mycluster.uw16e.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client["teste"]
        collection = db["SearchResults"]
        insertSearch = {'Lyric': Lyrics}
        collection.insert_one(insertSearch)



        return [AllSlotsReset()]

