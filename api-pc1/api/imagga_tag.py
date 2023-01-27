import requests
import json

def extraer_tags(min_confidence, image_url):
   with open('credentials.json', 'r') as f:
       config = json.load(f)
       api_key= config["imagga"]["api_key"]
       api_secret= config["imagga"]["api_secret"]

   response = requests.get(f"https://api.imagga.com/v2/tags?image_url={image_url}", auth=(api_key, api_secret))

   tags = [
   t["tag"]["en"]
   for t in response.json()["result"]["tags"]
   if t["confidence"] > min_confidence]

   return tags

