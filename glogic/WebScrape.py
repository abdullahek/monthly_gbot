# import numpy as np
# import requests
# from bs4 import BeautifulSoup as bs
# from .gresponses import Dictionary
#
#
# def news_scrape(url, n, tab_no):
#     number_of_articles = n  # how many we want scraped
#     tab = tab_no
#     # creates empty lists
#     articles = []
#     links = []
#     titles = []
#     out_dict = {}
#
#     # connects to page and saves articles in a soup
#     r1 = requests.get(url)
#     cont = r1.content
#     soup = bs(cont, "lxml")
#     articles = soup.find(class_='tab_content', id=tab)
#     if articles is not None:
#         articles = articles.find_all(class_='panel panel-default')
#     else:
#         articles = soup.find_all(class_='panel panel-default')
#
#     # # loops through top articles, adds title and link to dictionary
#     for n in np.arange(0, number_of_articles):
#         # getting titles
#         title = articles[n].find('h1').get_text()
#         titles.append(title)
#
#         # getting links
#         link = articles[n].find('a')['href']
#         links.append(link)
#
#         out_dict[titles[n]] = links[n]
#     return out_dict
#
#
# def news_out(msg, url, n, tab):
#     out = Dictionary[msg]
#     news = news_scrape(url, n, tab)
#     emoji = "\U0001F6A9"
#     for x, y in news.items():
#         headline = "*" + x + "*\n"
#         ref = "Read more at: " + y + "\n\n"
#         out = out + emoji + headline + ref
#
#     return out
#
#
# def rep_out(msg, url, n, tab):
#     out = Dictionary[msg]
#     news = news_scrape(url, n, tab)
#     emoji = "\U0001F6A9"
#     for x, y in news.items():
#         headline = "*" + x + "*\n"
#         ref = "Read more at: https://www.genesis-analytics.com/" + y + "\n\n"
#         out = out + emoji + headline + ref
#
#     return out
#
#
# def value():
#     url = "https://www.genesis-analytics.com/value-unlocked-intro"
#     r1 = requests.get(url)
#     cont = r1.content
#     soup = bs(cont, "lxml")
#     articles = soup.find_all(class_='panel-title')
#
#     out = Dictionary["value1"] + str(articles[0].get_text()) + "* and *" \
#           + str(articles[1].get_text()) + Dictionary['value2']
#
#     return out
#
#
# headlines = news_out('headlines', 'https://www.genesis-analytics.com/news', 3, 'tab1')
# bulletins = news_out('bulletins', 'https://www.genesis-analytics.com/news', 3, 'tab2')
# reports = rep_out('reports', 'https://www.genesis-analytics.com/news', 3, 'tab3')
# covnews = news_out('covidnews', 'https://www.genesis-analytics.com/covid19', 3, None)
# value = value()
