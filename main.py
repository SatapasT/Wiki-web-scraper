import requests
from bs4 import BeautifulSoup
import re

URL = "https://jujutsu-kaisen.fandom.com/wiki/Jujutsu_Kaisen_Wiki"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

span_finder = soup.find_all("span")

key_word_store = []
key_word_counter = []
for span_finder in span_finder:
    word = span_finder.get_text()
    position_counter = 0
    word_seperator_arr = []

    for i in range(len(word)):
        if word[i] == " ":
            word_seperator_arr.append(word[position_counter:i])
            position_counter = i+1
    for i in range(len(word_seperator_arr)):
        if word not in key_word_store:
            key_word_store.append(word_seperator_arr[0])
            word_seperator_arr.pop(0)
        else:
            word_seperator_arr.pop(0)
print(key_word_store)


print(span_finder)
#print(soup)