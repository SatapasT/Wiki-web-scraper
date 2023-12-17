# Wiki Web Scraper

Wiki Web Scraper is a Python program designed for extracting and analyzing textual data from Wiki Fandom pages, specifically those related to TV shows or other topics. It utilizes the BeautifulSoup library for HTML parsing, the requests library for making HTTP requests, and the Googlesearch library for finding relevant Wikipedia pages.

## Features
1. **Data Collection:** The program retrieves textual data from the provided Wikipedia page and its linked pages.
2. **Keyword Analysis:** It identifies and counts the occurrences of individual words (excluding non-alphabetic characters) within the collected data.
3. **More to Come:** Stay tuned for additional features as the project continues to evolve!

## Dependencies
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Alive Progress](https://pypi.org/project/alive-progress/)
- [Googlesearch](https://pypi.org/project/google/)

## Installation and Usage
```bash
pip install requests beautifulsoup4 alive-progress google
```

Run the script in a Python environment:
```bash
python main.py
```

## Notes
The program's execution time may vary depending on the size and structure of the Wikipedia page and its linked pages.
Author
This program was created by SatapasT.

Happy Scrapping!

