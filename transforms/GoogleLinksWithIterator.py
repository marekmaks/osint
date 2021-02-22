from maltego_trx.entities import Phrase

from maltego_trx.entities import URL

from maltego_trx.maltego import UIM_INFORM

from maltego_trx.transform import DiscoverableTransform

from googlesearch import search

from filelock import Timeout, FileLock

class GoogleLinksWithIterator(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):
        query = request.Value
        iteration = 0

        lock = FileLock("iterator_file.lock")

        with lock:
          with open('iterator_file', 'r') as f:
             iterationSetting = f.read()
             if iterationSetting is not None:
               iteration = int(iterationSetting)
          with open('iterator_file', 'w') as f:
             nextIteration = iteration + 1
             if nextIteration >= 6:
               nextIteration = 0
             f.write(str(nextIteration))

        maltegoLimit = 10
        startPos = maltegoLimit * iteration
        stopPos = maltegoLimit * (iteration + 1)

        for link in search(query, tld="com", lang="pl", num=maltegoLimit, start=startPos, stop=maltegoLimit, pause=2):  
          urlEntity = response.addEntity(URL)
          urlEntity.addProperty('url', 'URL', 'loose', link)
          urlEntity.addProperty('title', 'Title', 'loose', link)
          urlEntity.addProperty('short-title', 'Short Title', 'loose', link)
