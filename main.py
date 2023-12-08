import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from alive_progress import alive_bar
import os
import random
import sys

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 

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
        self.main_webaddress = string_URL[string_URL.find("https://"):string_URL.find("/wiki/") + 6]

    def setup(self):
        self.web_surf()
        self.data_collector()

    def partition(word_count_arr,word_store_arr, left, right):
        
        pivot_location = random.randint(left,right)
        pivot = word_count_arr[pivot_location]
        i = left - 1

        for j in range(left,right):
            if word_count_arr[j] <= pivot:
                pass


    def data_collector(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Scraping all data from {scraper.main_webaddress}!")
        counter = 1
        print("Starting the loop!","\n","\n")

        while len(scraper.URL_holder) != 0:
            progress_bar = "-" * (counter % 10)
            print(f"{progress_bar:<10}", end="\r")
            if counter % 10 == 0:
                delete_above_print()
                print(f"Surfed through {counter} webs!", end="\r")
                print()
            counter += 1
            self.update_soup(scraper.URL_holder[0])
            self.URL_holder.pop(0)
            self.web_surf()
        delete_above_print()
        print(f"Surfed through {counter} total webs! \n")
        print(f"Analyzing the web!")
        with alive_bar(len(scraper.visited)+1) as bar:
            bar(0, skipped=True)
            for i in range(0, len(scraper.visited)):
                self.update_soup(scraper.visited[i])
                self.keyword_finder()
                bar()
    
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
        for i in range(len(self.key_word_store)):
            if str(scraper.key_word_store[i]) == word:
                return (f"{scraper.key_word_store[i]} : {scraper.key_word_counter[i]}")

def delete_above_print():
    cursor_up_one = '\x1b[1A' 
    erase_print = '\x1b[2K' 
    sys.stdout.write(cursor_up_one) 
    sys.stdout.write(erase_print)
    
scraper = scraper("https://jujutsu-kaisen.fandom.com/wiki/Jujutsu_Kaisen_Wiki")

scraper.setup()




print(scraper.word_amount_finder("sukuna"))
#print(soup)