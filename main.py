import requests
from bs4 import BeautifulSoup
import re

class scraper:
    def __init__(self, URL, key_store_input=None, key_counter_input=None, URL_holder=None, visited=None):
        self.page = requests.get(URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.key_word_store = []
        self.key_word_counter = []
        self.visited = [URL]
        self.URL_holder = []
    
    def update_soup(self,URL):
        self.page = requests.get(URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

    def keyword_finder(self):
        span_finder = self.soup.find_all("span")
        
        for span_finder in span_finder:
            word = span_finder.get_text()
            position_counter = 0
            word_seperator_arr = []

            for i in range(len(word)):
                if word[i] == " ":
                    word_seperator_arr.append(word[position_counter:i])
                    position_counter = i+1
            while len(word_seperator_arr) != 0:
                if word_seperator_arr[0] not in self.key_word_store:
                    self.key_word_store.append(word_seperator_arr[0])
                    self.key_word_counter.append(1)
                    word_seperator_arr.pop(0)
                else:
                    self.key_word_counter[self.key_word_store.index(word_seperator_arr[0])] += 1
                    word_seperator_arr.pop(0)
        for i in range(len(self.key_word_store)):
            if self.key_word_store[i].isalpha():
                print(f"{self.key_word_store[i]} : {self.key_word_counter[i]}")
        
    def web_surf(self):
        web_finder = self.soup.find_all("a")
        for web_finder in web_finder:
            link_tag_string = str(web_finder)
            if "https://jujutsu-kaisen.fandom.com/wiki" in link_tag_string:
                print(link_tag_string)
            #index_href = link_tag_string.find('href="') + 6
            #print(link_tag_string[index_href::])


scraper = scraper("https://jujutsu-kaisen.fandom.com/wiki/Jujutsu_Kaisen_Wiki")
print(scraper.web_surf())
#print(soup)