import requests
from bs4 import BeautifulSoup
import re

class scraper:
    def __init__(self, URL, key_store_input=None, key_counter_input=None):
        page = requests.get(URL)
        self.soup = BeautifulSoup(page.content, "html.parser")
        if key_store_input == None:
            self.key_word_store = []
            self.key_word_counter = []
        else:
            self.key_word_store = key_store_input
            self.key_word_counter = key_counter_input

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


scraper = scraper("https://jujutsu-kaisen.fandom.com/wiki/Jujutsu_Kaisen_Wiki")
scraper.keyword_finder()
#print(soup)