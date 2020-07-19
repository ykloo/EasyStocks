from getNews import find_news_dates, find_news_headlines, find_news_providers

dates = find_news_dates()
providers = find_news_providers()
headlines_links = find_news_headlines()
headlines = headlines_links[0]
links = headlines_links[1]


class News:
    def __init__(self, provider, date, headline, link):
        self.provider = provider
        self.date = date
        self.headline = headline
        self.link = link

list_news = []
for i in range(len(dates)):
    date = dates[i]
    provider = providers[i]
    headline = headlines[i]
    link = links[i]
    article = News(provider, date, headline, link)

    list_news.append(article)

print(list_news[0].link)

