import json
from googletrans import Translator, LANGUAGES
import requests, uuid, json
from asgiref.sync import async_to_sync
from googletrans import Translator, LANGUAGES
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
import spacy

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


class TranslatorConsumer(WebsocketConsumer):
    def connect(self):
        # Called on connection.
        # To accept the connection call:
       
        self.accept()
        print("connet")
    

    def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        ent1,ent2,labels1,labels2=[],[],[],[]
       
        text_data_json = json.loads(text_data)
        print(text_data_json)
        
        slang=text_data_json["fromLanguage"]
        dstlang=text_data_json["toLanguage"]
        language_models = {
        'en': 'en_core_web_sm',
        'es': 'es_core_news_sm',
        'it': 'it_core_news_sm',
        'ar':'xx_ent_wiki_sm'
        }
         
        translator = Translator()
        translation = translator.translate(text_data_json["transcript"], src=slang, dest=dstlang)
        transl=translation.text


        if slang  in language_models :
            nlp = spacy.load(language_models[slang])
            doc = nlp(text_data_json["transcript"])
            for ent in doc.ents:
                ent1.append(ent.text)
                labels1.append(ent.label_)
            
        
        
        if dstlang  in language_models :
            print(language_models[dstlang])
            nlp = spacy.load(language_models[dstlang])
            doc = nlp(transl)
            for ent in doc.ents:
                ent2.append(ent.text)
                labels2.append(ent.label_)

        self.send(text_data=json.dumps({
                        'translation': transl,
                         "speechHighlitedWords":{
                            "label":labels1,
                            "entity":ent1
                         },
                        "highlightedWords":{
                            "label":labels2,
                            "entity":ent2
                        }                    }))


    def disconnect(self, close_code):
        # Called when the socket closes
        self.close()



"""
        if slang  in language_models :
            nlp = spacy.load(language_models[slang])
            doc = nlp(text_data_json["transcript"])
            for ent in doc.ents:
                ent1.append(ent.text)
                labels1.append(ent.label_)
            
        
        
        if dstlang  in language_models :
            print(language_models[dstlang])
            nlp = spacy.load(language_models[dstlang])
            doc = nlp(transl)
            for ent in doc.ents:
                ent2.append(ent.text)
                labels2.append(ent.label_)
"""

class NerConsumer(WebsocketConsumer):
    def connect(self):
        # Called on connection.
        # To accept the connection call:
        self.accept()
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        #self.accept("subprotocol")
        # To reject the connection, call:
        #self.close()

    def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        
        text = text_data_json["text"]
       # entities,labels=ner_en(text)
       # sentObject={}
       # self.send(text_data=json.dumps(sentObject))
        

    def disconnect(self, close_code):
        # Called when the socket closes
        self.close()
    
   # def ner_en( text):
            #tagger = SequenceTagger.load("flair/ner-english")
           # sentence = Sentence(text)
           # pred = tagger.predict(sentence)
            #entities, labels = [], []
           # for entity in sentence.get_spans('ner'):
            #    entities.append(entity.text)
            #    labels.append(entity.labels[0].value)
            #return entities, labels


