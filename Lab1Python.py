from asyncio.windows_events import NULL
from datetime import timedelta
import re
#import httplib2
import sys
from pyparsing import empty
import wikipedia
from ratelimiter import RateLimiter
import collections
import re
#from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import unquote



def bfs(graph:dict, root,w,search,deep:dict,parents:dict)->dict:
    lim=timedelta(seconds=(60/w))
    #print(graph)
    print(lang)
    wikipedia.set_rate_limiting(True,lim)
    visited, queue = set(), collections.deque([root])
    visited.add(root)
    while queue:
        vertex = queue.popleft()
        print("Searching for "+search)
        if vertex!=root:
            deep.update({vertex:deep.get(parents.get(vertex))+1})
        if vertex == search:
            visited.add(vertex)
            print(deep)
            return 1
        print(vertex +" depth: " +str( deep.get(vertex)))
        try:
            page=wikipedia.page(vertex)
            links=[]
            links=page.links
            #print ("vertex: "+vertex)
            graph.update({page.title:links})
        except:
            print(vertex+" Not found")
        #print(empty.get(vertex))
        if graph.get(vertex)!=None:
            for neighbour in graph.get(vertex):
                if neighbour not in visited:
                    visited.add(neighbour)
                    parents.update({neighbour:vertex})
                    #print(neighbour)
                    queue.append(neighbour)
        #deep=+1
        if deep.get(vertex)>6:
            return 0
    print(deep)
def translate( url ):
    tr=unquote(url.split("/wiki/")[1])
    return tr
if __name__ == '__main__':                    
    url =sys.argv[1]
    findurl= sys.argv[2]
    #url ="https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"
    #findurl= "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0:%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5"
    #print(url2)
    lang=""
    ls=re.compile(r"//[a-z][a-z]")
    lang=ls.search(url).group()
    if lang== NULL:
        exit
    if lang!=ls.search(findurl).group():
        print("language dont match")
        sys.exit()
    wikipedia.set_lang(lang.strip("/"))
    find= translate(findurl)
    start=translate(url)
    #http = httplib2.Http()
    #response, content = http.request(url)
    result=wikipedia.search(start)
    page=wikipedia.page(result[0])
    links=[]
    links=page.links
    graph={page.title:links}
    deep={page.title:0}
    parents={page.title:-1}
    #for i in graph.get(page.title):
    #    parents.update({i:page.title})
 
    #result=wikipedia.search(find)
    ##page=wikipedia.page(result[0])
    ##links=[]
    ##links=page.links
    #graph.update({page.title:links})
    #print(graph)
   
    #print(page.title)
    #print(graph.get(page.title))
    #print(bfs(graph,page.title,5,find,deep,parents))
    if bfs(graph,page.title,sys.argv[3],find,deep,parents)!=0:
        path = []
        path.append(find)
        current = parents.get(find)
 

        while current != -1:
            path.append(current)
            current = parents.get(current)
        path.append(start)
        print(path.reverse())
    else:
        print("Search didn't found link")