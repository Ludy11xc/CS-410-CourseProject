import urllib.error
import re
import logging
from urllib.request import urlopen
from bs4 import BeautifulSoup
import concurrent.futures
import time


MAX_THREADS = 30

def get_soup(url):
    """Returns BeautifulSoup object from url

    :param url: url
    :return: soup
    """
    try:
        page = urlopen(url)
    except urllib.error.URLError as e:
        print(e.reason)
        return None
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_links(soup):
    links = []
    link_tag = soup.find("ul", id="headlines")
    all_links = link_tag.find_all("a")
    for link in all_links:
        links.append(link['href'])
    return links

def get_document(link):
    soup = get_soup(link)
    if soup is None:
        return
    text = []
    text_tag = soup.find_all("p")
    relevant = False
    for paragraph in text_tag:
        txt = paragraph.get_text()
        if ("bush" in txt.lower() or "gore" in txt.lower()):
            relevant = True
        if (len(txt) > 80):
            text.append(txt)
    if relevant:
        time_tag = soup.find("time")
        ftime = open("./data/nyt_filtered_time_stamps", "a+")
        ftime.write(time_tag.get_text() + "\n")
        ftime.close()
        f = open("./data/nyt_filtered_election_docs", "a+")
        f.write(" ".join(text) + "\n")
        f.close()
        print("Wrote relevant document")
    return

# Attempt to speed up process, not WAI
def threaded_scrape(links):
    threads = min(MAX_THREADS, len(links))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_document, links)


if __name__ == "__main__":
    # Links to get all articles from May 2000 through October 2000
    all_links = [
                    "https://spiderbites.nytimes.com/2000/articles_2000_05_00000.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_05_00001.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_05_00002.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_05_00003.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_05_00004.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_06_00000.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_06_00001.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_06_00002.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_06_00003.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_06_00004.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_07_00000.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_07_00001.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_07_00002.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_07_00003.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_07_00004.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_08_00000.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_08_00001.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_08_00002.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_08_00003.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_08_00004.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_09_00000.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_09_00001.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_09_00000.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_09_00001.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_09_00002.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_09_00003.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_09_00004.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_10_00000.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_10_00001.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_10_00002.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_10_00003.html",
                    "https://spiderbites.nytimes.com/2000/articles_2000_10_00004.html"
                ]
    i = 0
    for link in all_links:
        soup = get_soup(link)
        articles = get_links(soup)
    #    f = open("./data/nyt_filtered_election_docs", "a+")
    #    for link in links:
    #        f.write(get_document(get_soup(link)))
    #    f.close()
    #    for article in articles:
    #        get_document(article)
        threaded_scrape(articles)
        i+=1
        print("Done " + str(i) + "/30")
        time.sleep(5)

    print("Completed")
