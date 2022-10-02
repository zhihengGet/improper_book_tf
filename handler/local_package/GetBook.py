from difflib import SequenceMatcher
import requests
from bs4 import BeautifulSoup
from . import BookUtils

link="https://www.cool18.com/bbs4/index.php?app=forum&act=gold&p={0}"
prefix="https://www.cool18.com/bbs4/"
count=0
books=[]

def print(*arg):
  pass
class GetBookFromSource():
  def __init__(self) -> None:
      self.pageCount=1 # page to scrape
      self.soups=[] # all soups scraped
      self.hasNext=True # do we have next page to scrape ?
      self.found=False # found the same book in old_list that we got from last execution
  def getNextSoup(self):
    # get next page and turn it into soup
    if self.hasNext==False:
      return None
    page=f"https://www.cool18.com/bbs4/index.php?app=forum&act=gold&p={self.pageCount}"
    x = requests.get(page)
    soup = BeautifulSoup(x.text, 'html5lib')
    data=soup.body.find("ul",id="thread_list")
    children=data.contents
    if BookUtils.stripe_char(children[0]).strip()=="":
      children.pop()
    if children == []:
      self.hasNext=True
      return None
    self.pageCount+=1
    self.soups.append(data)
    return data
  def get_book_list_from_soup(self,soup,old):
    books=[]
    links=soup.find_all("a")
    for x in links:
      book={}
      href=x.get("href")
      # invalid 
      if "index.php?app=forum&act=threadview&tid" not in href:
        continue
      font=x.find("font")
      types="unknown"
      if font and font.get_text():
          types=font.get_text()
      book["link"]=prefix+href
      book["type"]=types
      book["name"]=x.get_text("")
      left=book["name"].find("【")
      right=book["name"].find("】")
      #〖超級官迷〗１－２１６章　作者：升平
      book["name"]=BookUtils.stripe_char(book["name"][left+1:right]) or BookUtils.stripe_char(x.text)
      if old and book["name"] in old:
        print("already have this book,  stop update")
        self.found=True
        break
      print(book["name"])
      books.append(book)
    return books
  def fetch_all_soup(self):
    self.pageCount=1
    while self.getNextSoup():
      pass
    return self.soup
  def fetch_all_books(self):
    self.fetch_all_soup()
    books=[]
    for soup in self.soups:
      # get all books
      books_from_this_page=self.get_book_list_from_soup(soup,[])
      books.extend(books_from_this_page)
    return books
  def fetch_new_books(self,keys):
    # return updated list
    #cool_books=BookUtils.read_json("/content/cool_books.json")
    new_books=[]
    #keys=map(lambda x:x["name"],cool_books)
    old=set(keys)
    self.found=False
    if self.soups:
      # already fetched soups
      for soup in self.soups:
        booksFromSoup=self.get_book_list_from_soup(soup,old)
        new_books.extend(booksFromSoup)
        if self.found:  
          break
    else:
      # starting fetching 
      self.pageCount=1
      soup=self.getNextSoup()
      
      while soup and self.found ==False:
        booksFromSoup=self.get_book_list_from_soup(soup,old)
        new_books.extend(booksFromSoup)
        
        if self.found ==False:
          soup=self.getNextSoup()
    return new_books


