import requests
from bs4 import BeautifulSoup
from alive_progress import alive_bar
import os
import sys
from googlesearch import search

class Scraper:

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
        self.main_web_address = string_URL[string_URL.find("https://"):string_URL.find("/wiki/") + len("/wiki/")]

    def setup(self):
        self.web_surf()
        self.data_collector()

    def data_collector(self):
        clear_terminal()
        print(f"Scraping all data from {self.main_web_address}!")
        counter = 1
        print("Starting the loop!","\n","\n")
        while len(self.URL_holder) != 0:
            progress_bar = "-" * (counter % 10)
            print(f"{progress_bar:<10}", end="\r")
            if counter % 10 == 0:
                delete_above_print()
                print(f"Surfed through {counter} webs!", end="\r")
                print()
            counter += 1
            self.update_soup(self.URL_holder[0])
            self.URL_holder.pop(0)
            self.web_surf()
        print(f"Surfed through {counter} total webs! \n",end="\r")
        delete_above_print()
        print(f"Analyzing the web!")
        with alive_bar(len(self.visited)+1) as bar:
            bar(0, skipped=True)
            for i in range(0, len(self.visited)):
                self.update_soup(self.visited[i])
                self.keyword_finder()
                bar()

    def update_soup(self,URL):
        self.page = requests.get(URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
    
    def keyword_printer(self,n=None):
        if n == None:
            n = len(self.key_word_store)
        for i in range(n):
            print(f"{self.key_word_store[i]} : {self.key_word_counter[i]}")

    def keyword_finder(self):
        span_finder = self.soup.find_all("span")
        for span_finder in span_finder:
            word = span_finder.get_text()
            position_counter = 0
            word_separator_arr = []
            for i in range(len(word)):
                if word[i] == " ":
                    word_separator_arr.append(word[position_counter:i].lower())
                    position_counter = i+1
            while len(word_separator_arr) != 0:
                if word_separator_arr[0] not in self.key_word_store:
                    if word_separator_arr[0].isalpha():
                        self.key_word_store.append(word_separator_arr[0])
                        self.key_word_counter.append(1)
                        self.word_count += 1
                    word_separator_arr.pop(0)
                else:
                    if word_separator_arr[0].isalpha():
                        self.key_word_counter[self.key_word_store.index(word_separator_arr[0])] += 1
                        self.word_count += 1
                    word_separator_arr.pop(0)
                    
    def web_surf(self):
        web_finder = self.soup.find_all("a")
        for web_finder in web_finder:
            link_tag_string = str(web_finder)
            if self.main_web_address in link_tag_string:
                index_href = link_tag_string.find('href="') + 6
                closing_mark = index_href
                while link_tag_string[closing_mark] != '"':
                    closing_mark += 1
                if link_tag_string[index_href:closing_mark:] not in self.visited:
                    self.URL_holder.append(link_tag_string[index_href:closing_mark:])
                    self.visited.append(link_tag_string[index_href:closing_mark:])
    
    def word_amount_finder(self, word):
        for i in range(len(self.key_word_store)):
            if str(self.key_word_store[i]) == word:
                return (f"{self.key_word_store[i]} : {self.key_word_counter[i]}")

def delete_above_print():
    cursor_up_one = "\x1b[1A" 
    erase_print = "\x1b[2K"
    sys.stdout.write(cursor_up_one) 
    sys.stdout.write(erase_print)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    middle = len(arr)//2
    left = arr[0:middle]
    right = arr[middle:len(arr)+1]
    
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)

    return merge(left_sorted,right_sorted)

def merge(left,right):
    sorted = []
    while len(left) > 0 or len(right) > 0:
        print(left,right)
        if len(left) > 0 and len(right) > 0:
            if left[0] >= right[0]:
                sorted.append(left[0])
                left.pop(0)
            elif left[0] <= right[0]:
                sorted.append(right[0])
                right.pop(0)
        elif len(left) > 0:
            while len(left) > 0:
                sorted.append(left[0])
                left.pop(0)
        else:
            while len(right) > 0:
                sorted.append(right[0])
                right.pop(0)
    return sorted


def google_search():
    user_input = input("Type the name of the show you want to scrap! \n")
    query = user_input + "wiki fandom"
    for web in search(query, tld="co.in", num=5, stop=5, pause=2):
        if "fandom" in web and "com":
            return str(web)
        else:
            clear_terminal()
            print("Couldn't find the wiki fandom for it! Have you spelt it correctly? \n")
            google_search()

def setup_scraper():
    my_scraper = None
    URL = google_search()
    while my_scraper == None:
        clear_terminal()
        try:
            user_input = int(input(f"Is this the correct URL? \n{URL} \nYes : 1 \nNo : 2 \n"))
            if user_input == 1:
                my_scraper = Scraper(URL)
                my_scraper.setup()
                return my_scraper
            elif user_input == 2:
                clear_terminal()
                URL = google_search()
            else:
                print("Invalid input! \n Yes : 1 \n No : 2 \n")
        except:
            clear_terminal()
            print("Invalid input! \n")
            input("Press enter reload!")
            clear_terminal()
            URL = google_search()


arr = [5, 2, 8, 1, 7, 4, 6, 3]
print(merge_sort(arr))
input()

#clear_terminal()
scraper_instance = setup_scraper()

while True:
    clear_terminal()
    try:
        user_input = int(input("Please input a command \n 1 : specific word count \n 2 : words count \n"))
    except ValueError:
        print("Invalid input \n")
    if user_input == 1:
        clear_terminal()
        word_input = input("Input the keyword\n")
        clear_terminal()
        print(scraper_instance.word_amount_finder(word_input))
    elif user_input == 2:
        clear_terminal()
        scraper_instance.keyword_printer()
    else:
        print("Invalid input")
    input("Press enter to reload!")
