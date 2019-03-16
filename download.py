# coding: UTF-8
from multiprocessing import Pool
import json
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import os
import functools

# create folder if need
def createDirSafe(path):
  if not os.path.isdir(path):
    os.makedirs(path)

# read url parse to soup
def url2soup(url):
  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, "html.parser")
  return soup

def getmaxsize(sizeurl):
  soup = url2soup(sizeurl)
  sizejson = json.loads(str(soup))['sizes']
  widths = list(map(lambda x:x['width'], sizejson))
  #print(maxwidth)
  return max(widths)

def xxx(id, path):
  # json:items
  txtbase  = "https://digitalcollections.lib.washington.edu/digital/api/collections/chandless/items/%s/false"
  # json:image width
  sizebase = "https://digitalcollections.lib.washington.edu/digital/iiif/chandless/%s/info.json"
  # full size image
  fullbase = "https://digitalcollections.lib.washington.edu/digital/iiif/chandless/%s/full/%s,/0/default.jpg?highlightTerms="
  id = str(id).replace('\n', '')
  print("id=" + id)

  txturl  = (txtbase % id)
  sizeurl = (sizebase % id)
  imgurl  = (fullbase % (id, getmaxsize(sizeurl)))

  # save json
  with open(path+id+'.json', mode='w') as f:
    json.dump(json.loads(str(url2soup(txturl))), f, indent=2)

  # save img
  urllib.request.urlretrieve(imgurl, path+id+'.jpg')

# -------------
# memo howto create id.txt
#for(var i=0;i<$$('a.SearchResult-container').length;i++)
#    console.log($$('a.SearchResult-container')[i].href)

fn = './id.txt'
path = './data/'
createDirSafe(path)
with open(fn, mode='r') as f:
  ids = f.readlines()

with Pool(5) as p:
  p.map(functools.partial(xxx, path=path), ids)

