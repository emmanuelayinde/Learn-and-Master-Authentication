import firebase_admin
import pyrebase
import json
 
from firebase_admin import credentials


yotube_summarizer_json = "youtube-summarizer-firebase-adminsdk.json"
firebase_config_json = 'firebase_config.json'


cred = credentials.Certificate(yotube_summarizer_json)
firebase = firebase_admin.initialize_app(cred)

pb = pyrebase.initialize_app(json.load(open(firebase_config_json)))