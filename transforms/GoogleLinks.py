
from maltego_trx.entities import Phrase

from maltego_trx.entities import URL

from maltego_trx.transform import DiscoverableTransform

from googlesearch import search

class GoogleLinks(DiscoverableTransform):
   """
   Returns URL links for asked query from google.com
   """

   @classmethod
   def create_entities(cls, request, response):
       query = request.Value

       maltegoLimit = request.Slider

       weight = 10

       for link in search(query, tld="com", lang="pl", num=maltegoLimit, start=0,  stop=maltegoLimit, pause=2):
         urlEntity = response.addEntity(URL)
         urlEntity.setWeight(weight)
         urlEntity.addProperty('url', 'URL', 'loose', link)
         urlEntity.addProperty('title', 'Title', 'loose', link)
         urlEntity.addProperty('short-title', 'Short Title', 'loose', link)
         weight -= 1