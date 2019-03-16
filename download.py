# coding: UTF-8
from multiprocessing import Pool
import json
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import os
import functools
import traceback

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
  return max(widths)

def xxx(id, path):
  id = str(id).replace('\n', '')
  print("id=" + id)
  base ="https://digitalcollections.lib.washington.edu/digital/"
  txtbase  = base + "api/collections/chandless/items/%s/false"		# json:items
  sizebase = base + "iiif/chandless/%s/info.json"					# json:image width
  fullbase = base + "iiif/chandless/%s/full/%s,/0/default.jpg"		# full size image

  # save json
  fjson = path+id+'.json'
  if(not os.path.exists(fjson)):
    txturl  = (txtbase  % id)
    with open(fjson, mode='w') as f:
      try:
        json.dump(json.loads(str(url2soup(txturl))), f, indent=2)
      except:
        traceback.print_exc()

  # save img
  fjpg = path+id+'.jpg'
  if(not os.path.exists(fjpg)):
    sizeurl = (sizebase % id)
    try:
      imgurl  = (fullbase % (id, getmaxsize(sizeurl)))
      urllib.request.urlretrieve(imgurl, fjpg)
    except:
      traceback.print_exc()

# -------------
# memo howto create id.txt
#for(var i=0;i<$$('a.SearchResult-container').length;i++)
#    console.log($$('a.SearchResult-container')[i].href)

fn = './id.txt'
path = './data/'
createDirSafe(path)
with open(fn, mode='r') as f:
  ids = f.readlines()

#with Pool(1) as p:
#  p.map(functools.partial(xxx, path=path), ids)
for i in ids:
  xxx(i, path)
