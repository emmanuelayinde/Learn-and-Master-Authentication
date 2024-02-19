import requests
from ..main import login


token = login("abcd@abcd.com", "password")
 
def ping(token: str):
   headers = {
       'authorization': token
   }
   response = requests.post(url="http://127.0.0.1:9001/ping", headers=headers)
   return(response.text)
 
print(ping(token))