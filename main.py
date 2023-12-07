import requests
from bs4 import BeautifulSoup
import re

class scraper:
    def __init__(self, URL):
        self.page = requests.get(URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.key_word_store = []
        self.key_word_counter = []
        self.visited = []
        self.visited.append(URL)
        self.URL_holder = []
        self.word_count = 0
        
        string_URL = str(URL)
        starting_index = string_URL.find("https://")
        ending_index = string_URL.find("/wiki/") + 6
        self.main_webaddress = string_URL[starting_index:ending_index]
    
    def update_soup(self,URL):
        self.page = requests.get(URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
    
    def keyword_printer(self):
        for i in range(len(scraper.key_word_store)):
            print(f"{scraper.key_word_store[i]} : {scraper.key_word_counter[i]}")

    def keyword_finder(self):
        span_finder = self.soup.find_all("span")
        for span_finder in span_finder:
            word = span_finder.get_text()
            position_counter = 0
            word_seperator_arr = []
            for i in range(len(word)):
                if word[i] == " ":
                    word_seperator_arr.append(word[position_counter:i].lower())
                    position_counter = i+1
            while len(word_seperator_arr) != 0:
                if word_seperator_arr[0] not in self.key_word_store:
                    if word_seperator_arr[0].isalpha():
                        self.key_word_store.append(word_seperator_arr[0])
                        self.key_word_counter.append(1)
                        self.word_count += 1
                    word_seperator_arr.pop(0)
                else:
                    if word_seperator_arr[0].isalpha():
                        self.key_word_counter[self.key_word_store.index(word_seperator_arr[0])] += 1
                        self.word_count += 1
                    word_seperator_arr.pop(0)
                    
    def web_surf(self):
        web_finder = self.soup.find_all("a")
        for web_finder in web_finder:
            link_tag_string = str(web_finder)
            if self.main_webaddress in link_tag_string:
                index_href = link_tag_string.find('href="') + 6
                closing_mark = index_href
                while link_tag_string[closing_mark] != '"':
                    closing_mark += 1
                if link_tag_string[index_href:closing_mark:] not in self.visited:
                    self.URL_holder.append(link_tag_string[index_href:closing_mark:])
                    self.visited.append(link_tag_string[index_href:closing_mark:])
    
    def word_amount_finder(self, word):
        for i in range(scraper.word_count - 1):
            if scraper.key_word_store[i] == word:
                return (f"{scraper.key_word_store[i]} : {scraper.key_word_counter[i]}")

    


scraper = scraper("https://genshin-impact.fandom.com/wiki/Genshin_Impact_Wiki")
scraper.keyword_finder()
scraper.web_surf()

print(scraper.main_webaddress)
counter = 0
print("Starting the loop!")
while len(scraper.URL_holder) != 0:
    if counter%10 == 0:
        print(f"I am running and not dead! : {len(scraper.URL_holder)}")
    counter += 1
    scraper.update_soup(scraper.URL_holder[0])
    scraper.URL_holder.pop(0)
    scraper.keyword_finder()
    scraper.web_surf()

return scraper.keyword_printer()
#print(soup)