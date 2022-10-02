import json
import re
from difflib import SequenceMatcher

def print(*arg):
  pass

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def isChinese(s):
  if re.search(u'[\u4e00-\u9fff]', s):
      return True
  return False

def stripe_char(s):
  s="".join(re.findall(r"[\u4e00-\u9fff]+",s))
  return s

'''
save a utf8 
'''

def save_json(file_name,obj):

  j=json.dumps(obj,ensure_ascii=False).encode()

  with open(file_name or "out", 'w',encoding="utf-8") as f:
    f.write(j.decode())  

def read_json(filename):
    file = open(filename,encoding="utf-8")
    config = json.load(file)
    print(config)
    return config

def update_books():
  pass

