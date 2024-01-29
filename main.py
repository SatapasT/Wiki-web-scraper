import requests
from bs4 import BeautifulSoup
from alive_progress import alive_bar
import os
import sys
from googlesearch import search
import urllib.request 
from PIL import Image 

class Scraper:

    def __init__(self, URL):
        self.page = requests.get(URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.key_word_store = []
        self.key_word_counter = []
        self.visited = []
        self.visited.append(URL)
        self.URL_holder = []
        self.main_title = []
        self.image_holder = []
        self.word_count = 0
        string_URL = str(URL)
        self.main_web_address = string_URL[string_URL.find("https://"):string_URL.find("/wiki/") + len("/wiki/")]

    def setup(self):
        self.web_surf()
        self.data_collector()
        self.sort_counter()
        self.word_count = len(self.key_word_counter)

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

        delete_above_print()
        print(f"Surfed through {counter} total webs! \n",end="\r")
        print(f"Analyzing the web!")

        with alive_bar(len(self.visited)+1) as bar:
            bar(0, skipped=True)
            for i in range(0, len(self.visited)):
                self.get_title(self.visited[i])
                self.get_image(self.visited[i])
                self.update_soup(self.visited[i])
                self.keyword_finder()
                bar()

    def get_image(self,URL):
        image_finder = self.soup.find_all('img')

        for image_embedding in image_finder:
            image_embedding_string = str(image_embedding)
            index_image_name = image_embedding_string.find('img alt="') + len('img alt="')
            closing_image_name = index_image_name

            while image_embedding_string[closing_image_name] != '"':
                closing_image_name += 1
    
            image_name = image_embedding_string[index_image_name:closing_image_name]
            index_image_src = image_embedding_string.find('src="') + len('src="')
            closing_image_src = index_image_src

            while image_embedding_string[closing_image_src] != '"':
                closing_image_src += 1

            image_URL = image_embedding_string[index_image_src:closing_image_src]
            if image_URL not in self.image_holder and image_URL != []:
                self.image_holder.append([image_name,image_URL,URL])

    def get_title(self,URL):
        title_finder = self.soup.find_all('span', class_='mw-page-title-main')

        if title_finder != []:
            title_finder_string = str(title_finder)
            index_span = title_finder_string.find('class="mw-page-title-main">') + len('class="mw-page-title-main">')
            closing_span = title_finder_string.find("</span>")
            self.main_title.append([title_finder_string[index_span:closing_span],URL])

    def update_soup(self,URL):
        self.page = requests.get(URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

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
                    word_separator_arr.pop(0)

                else:
                    if word_separator_arr[0].isalpha():
                        self.key_word_counter[self.key_word_store.index(word_separator_arr[0])] += 1
                    word_separator_arr.pop(0)
                    
    def web_surf(self):
        web_finder = self.soup.find_all("a")

        for web_finder in web_finder:
            link_tag_string = str(web_finder)
            if self.main_web_address in link_tag_string:
                index_href = link_tag_string.find('href="') + len('href="')
                closing_mark = index_href
                while link_tag_string[closing_mark] != '"':
                    closing_mark += 1

                if link_tag_string[index_href:closing_mark:] not in self.visited:
                    self.URL_holder.append(link_tag_string[index_href:closing_mark:])
                    self.visited.append(link_tag_string[index_href:closing_mark:])
                
                
    def keyword_printer(self,start=None,end=None):
        if start < 0:
            start = self.word_count - 10
            end = self.word_count

        if end > self.word_count:
            start = 0
            end = 10

        for i in range(start,end):
            print(f"{i + 1}) {self.key_word_store[i].capitalize()} : {self.key_word_counter[i]}")

        return  start,end

    def word_amount_finder(self, word):
        for i in range(len(self.key_word_store)):
            if str(self.key_word_store[i]) == word:
                return (f"{self.key_word_store[i].capitalize()} : {self.key_word_counter[i]}")
        print(f"{word} wasn't found within the database!")
            
    def sort_counter(self):
        self.key_word_counter,self.key_word_store = merge_sort(self.key_word_counter,self.key_word_store)

    def main_title_printer(self,start,end,mode):
        if start < 0:
            start = len(self.main_title) - 10
            end = len(self.main_title)

        if end > len(self.main_title):
            start = 0
            end = 10

        for i in range(start,end):
            print(f"{i + 1}) {self.main_title[i][mode].capitalize()}")

        return start, end

    def image_print(self,start,end,mode):
        if start < 0:
            start = len(self.image_holder) - 10
            end = len(self.image_holder)

        if end > len(self.main_title):
            start = 0
            end = 10

        for i in range(start,end):
            print(f"{i + 1}) {self.image_holder[i][mode]}")

        return start, end

def delete_above_print():
    cursor_up_one = "\x1b[1A" 
    erase_print = "\x1b[2K"
    sys.stdout.write(cursor_up_one) 
    sys.stdout.write(erase_print)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def merge_sort(arr,arr2):
    if len(arr) <= 1:
        return arr,arr2
    
    middle = len(arr)//2
    left = arr[0:middle]
    right = arr[middle:len(arr)+1]

    left2 = arr2[0:middle]
    right2 = arr2[middle:len(arr)+1]

    left_sorted,left_sorted2 = merge_sort(left,left2)
    right_sorted,right_sorted2 = merge_sort(right,right2)

    return merge(left_sorted,left_sorted2,right_sorted,right_sorted2)

def merge(left,left2,right,right2):
    sorted = []
    sorted2 = []

    while len(left) > 0 or len(right) > 0:
        if len(left) > 0 and len(right) > 0:
            if left[0] >= right[0]:
                sorted.append(left[0])
                left.pop(0)
                sorted2.append(left2[0])
                left2.pop(0)

            elif left[0] <= right[0]:
                sorted.append(right[0])
                right.pop(0)
                sorted2.append(right2[0])
                right2.pop(0)

        elif len(left) > 0:
            while len(left) > 0:
                sorted.append(left[0])
                left.pop(0)
                sorted2.append(left2[0])
                left2.pop(0)

        else:
            while len(right) > 0:
                sorted.append(right[0])
                right.pop(0)
                sorted2.append(right2[0])
                right2.pop(0)

    return (sorted, sorted2)

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
            print("Invalid input!\n")  
            input("Press enter reload!")
            clear_terminal()
            URL = google_search()


def main():
    clear_terminal()

    try:
        user_input = int(input("Please input a command \n1 : Title Data \n2 : Words data \n"))
        if user_input == 1:
            interface_title()

        elif user_input == 2:
            interface_word()

        else:
            print("Invalid input \n")

    except:
        print("Invalid input")

    input("Press enter to reload!")
    main()

def interface_title():
    clear_terminal()

    try:
        user_input = int(input("Please input a command \n1 : Web Title\n2 : Images\n3 : Exit"))
        if user_input == 1:
            clear_terminal()
            start = 0
            end = 10
            mode = 0

            while user_input != 5:
                try:
                    start, end = scraper_instance.main_title_printer(start,end,mode)
                    user_input = int(input("\nPlease input a command \n1 : next 10 word \n2 : last 10 word \n3 : skip to \n4 : change content mode \n5 : exit \n"))
                    if user_input == 1:
                        start += 10
                        end += 10

                    elif user_input == 2:
                        start -= 10
                        end -=10
                        
                    elif user_input == 3:
                        clear_terminal()
                        try:
                            start = int(input("Input where you want to skip to\n")) - 1
                            end = start + 10
                            if start > len(scraper_instance.main_title) or start < 0:
                                print("Input out of bound!")
                                input("\nPress enter to reload!")
                        except:
                            print("Invalid input")
                            input("\nPress enter to reload!")
                    elif user_input == 4:
                        if mode == 0:
                            mode = 1
                        else:
                            mode = 0
                    elif user_input == 5:
                        pass
                    else:
                        print("Invalid input")
                        input("\nPress enter to reload!")
                except:
                    print("Invalid input")
                    input("\nPress enter to reload!")
                clear_terminal()
        elif user_input == 2:
            clear_terminal()
            start = 0
            end = 10
            mode = 0
            while user_input != 5:
                try:
                    start, end = scraper_instance.image_print(start,end,mode)
                    user_input = int(input("\nPlease input a command \n1 : next 10 image \n2 : last 10 image \n3 : skip to \n4 : change content mode \n5 : exit \n"))
                    if user_input == 1:
                        start += 10
                        end += 10
                    elif user_input == 2:
                        start -= 10
                        end -=10
                    elif user_input == 3:
                        clear_terminal()
                        try:
                            start = int(input("Input where you want to skip to\n")) - 1
                            end = start + 10
                            if start > len(scraper_instance.main_title) or start < 0:
                                print("Input out of bound!")
                                input("\nPress enter to reload!")
                        except:
                            print("Invalid input")
                            input("\nPress enter to reload!")
                    elif user_input == 4:
                        if mode == 0:
                            mode = 1
                        else:
                            mode = 0
                    elif user_input == 5:
                        pass
                    else:
                        print("Invalid input")
                        input("\nPress enter to reload!")
                except:
                    print("Invalid input")
                    input("\nPress enter to reload!")
                clear_terminal()    
            scraper_instance.image_print()
        elif user_input == 3:
            main()
        else:
            print("Invalid input!")
    except:
        print("Invalid input!")
    input("\nPress enter to reload!")
    interface_title()

def interface_word():
    clear_terminal()
    try:
        user_input = int(input("Please input a command \n1 : Words Count \n2 : Specific Word Count \n3 : Back\n"))
        if user_input == 1:
            clear_terminal()
            start = 0
            end = 10
            while user_input != 4:
                start, end = scraper_instance.keyword_printer(start,end)
                user_input = int(input("\nPlease input a command \n1 : next 10 word \n2 : last 10 word \n3 : skip to \n4 : exit \n"))
                try:
                    if user_input == 1:
                        start += 10
                        end += 10
                    elif user_input == 2:
                        start -= 10
                        end -= 10
                    elif user_input == 3:
                        clear_terminal()
                        try:
                            start = int(input("Input where you want to skip to\n")) - 1
                            end = start + 10
                            if start > scraper_instance.word_count or start < 0:
                                print("Input out of bound!")
                                input("\nPress enter to reload!")
                        except:
                            print("Invalid input")
                            input("\nPress enter to reload!")
                    elif user_input == 4:
                        interface_word()
                    else:
                        print("Invalid input")
                        input("\nPress enter to reload!")
                except:
                    input("\nPress enter to reload!")
                    print("Invalid input")
                clear_terminal()
        if user_input == 2:
            clear_terminal()
            word_input = input("Input the keyword\n")
            clear_terminal()
            print(scraper_instance.word_amount_finder(word_input))
        elif user_input == 3:
            main()
        else:
            print("Invalid input")
    except:
        print("Invalid input \n")
    input("\nPress enter to reload!")
    interface_word()


clear_terminal()
scraper_instance = setup_scraper()
main()

#data = requests.get(image_URL).content
#with open(f'{image_name}.jpg', 'wb') as file:
#file.write(data)