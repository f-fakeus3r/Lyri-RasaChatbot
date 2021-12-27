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

        #Conexão com a API
        api_adress='https://api.lyrics.ovh/v1/'

        #Slot de Artista
        artist = str(tracker.get_slot("artist_name"))
        #Substituindo espaço por %20 para que fique no modelo do link da API
        nartist = str(artist.replace(" ", "%20"))
        #Substituindo o símbolo (-), necessário
        nartist = str(nartist.replace("-", ""))

        #Slot de Artista
        song = str(tracker.get_slot("song_name"))
        #Substituindo espaço por %20 para que fique no modelo do link da API
        nsong = str(song.replace(" ", "%20"))
        #Substituindo o símbolo (-), necessário
        nsong = str(nsong.replace("+", ""))

        #URL final
        url = api_adress + nartist + '/' + nsong

        #Saída para console
        print(artist)
        print(song)

        #Retorno do JSON
        json_data = requests.get(url).json()
        
        #Tratamento do JSON
        for i in json_data:
            if i == 'lyrics':   #Se houver resultado
                Lyrics = json_data['lyrics']
                Lyrics = Lyrics.replace("Paroles de la chanson", "")    #Remove essa frase padrão da API
                Lyrics = Lyrics.replace("par", " - ")   #Remove essa frase padrão da API
                dispatcher.utter_message(text="Espero que essa seja a letra que você estava procurando:")   #Envia a mensagem para o usuário do bot
                dispatcher.utter_message(text=f"{Lyrics}")  #Envia a a letra da musica para o usuário do bot
            else:
                Lyrics = json_data['error'] #Se não houver resultado
                dispatcher.utter_message(text=f"Essa música não foi encontrada no nosso banco de dados :(") #Envia a mensagem para o usuário do bot
                dispatcher.utter_message(text="Tem certeza que você digitou corretamente?") #Envia a mensagem para o usuário do bot

        #Conexão com o MongoDB
        client = MongoClient("mongodb+srv://fake:db123_@mycluster.uw16e.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client["teste"]
        collection = db["SearchResults"]
        insertSearch = {'Lyric': Lyrics}
        collection.insert_one(insertSearch)

        #Retorno das funções, resetando também os slots para possibilitar novas pesquisas
        return [AllSlotsReset()]

