from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from News import News


def initialise_driver(text):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome('C:\Bot\chromedriver.exe',options=options)
    # driver = webdriver.Chrome()
    driver.get(f'https://sg.finance.yahoo.com/quote/{text}')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="quoteNewsStream-0-Stream"]/ul')))

    #returns name
    name = find_name(driver)

    #returns tuple consisting of price and its changes
    price_changes = find_price_and_changes(driver)

    #returns list of authors
    authors = find_news_providers(driver)

    #returns list of dates
    dates = find_news_dates(driver)

    #returns list of headlines
    headlines_links = find_news_headlines(driver)
    driver.quit()

    headlines = headlines_links[0]
    links = headlines_links[1]

    #returns a list of news objects
    list_news = []
    for i in range(len(dates)):
        author = authors[i]
        date = dates[i]
        headline = headlines[i]
        link = links[i]
        article = News(author, date, headline, link)

        list_news.append(article)
    return name, price_changes, list_news

def find_name(driver):
    name = driver.find_elements_by_xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')
    return name[0].text


#finds price and price changes
def find_price_and_changes(driver):
    span_tag_price = driver.find_elements_by_xpath('//*[@id="quote-header-info"]/div[3]/div/div/span[1]')
    span_tag_change = driver.find_elements_by_xpath('//*[@id="quote-header-info"]/div[3]/div/div/span[2]')

    return span_tag_price[0].text, span_tag_change[0].text


#finds news provider

def find_news_providers(driver):
    news_providers = []
    for i in range(1,6):
        path = '//*[@id="quoteNewsStream-0-Stream"]/ul/li[' + str(i) + ']/div/div/div[1]/div/span[1]'
        span_tag_news = driver.find_elements_by_xpath(path)
        #for articles that has no images attached
        if len(span_tag_news) > 0: 
            provider = span_tag_news[0].text
        else:
            #for articles that has images attached
            path = '//*[@id="quoteNewsStream-0-Stream"]/ul/li[' + str(i) + ']/div/div/div[2]/div/span[1]'
            span_tag_news = driver.find_elements_by_xpath(path)
            provider = span_tag_news[0].text
            #for articles that are Editor's Pick
            if provider == "Editor'S Pick":
                path = '//*[@id="quoteNewsStream-0-Stream"]/ul/li[' + str(i) + ']/div/div/div[2]/div[2]/span[1]'
                span_tag_news = driver.find_elements_by_xpath(path)
                provider = span_tag_news[0].text

        news_providers.append(provider)
    return news_providers

def find_news_dates(driver):
    news_dates = []
    for i in range(1,6):
        path = '//*[@id="quoteNewsStream-0-Stream"]/ul/li[' + str(i) + ']/div/div/div[1]/div/span[2]'
        span_tag_date = driver.find_elements_by_xpath(path)
        if len(span_tag_date) > 0 :
            date = span_tag_date[0].text
        else:
            path = '//*[@id="quoteNewsStream-0-Stream"]/ul/li[' + str(i) + ']/div/div/div[2]/div/span[2]'
            span_tag_date = driver.find_elements_by_xpath(path)
            if len(span_tag_date) > 0:
                date = span_tag_date[0].text
            #checks for articles that are editors picks
            else:
                path = '//*[@id="quoteNewsStream-0-Stream"]/ul/li[' + str(i) + ']/div/div/div[2]/div[2]/span[2]'
                span_tag_date = driver.find_elements_by_xpath(path)
                # date = span_tag_date[0].text
                date = 'empty'

        news_dates.append(date)
    return news_dates

def find_news_headlines(driver):
    news_headlines = []
    news_links = []
    for i in range(1,6):
        path = '//*[@id="quoteNewsStream-0-Stream"]/ul/li[' + str(i) + ']/div/div/div[1]/h3/a'
        span_tag_headline = driver.find_elements_by_xpath(path)
        if len(span_tag_headline) > 0:
            headline = span_tag_headline[0].text
            link = span_tag_headline[0].get_attribute('href')
        else:
            path = '//*[@id="quoteNewsStream-0-Stream"]/ul/li[' + str(i) + ']/div/div/div[2]/h3/a'
            span_tag_headline = driver.find_elements_by_xpath(path)
            headline = span_tag_headline[0].text
            link = span_tag_headline[0].get_attribute('href')

        news_headlines.append(headline)
        news_links.append(link)
    return news_headlines, news_links

'''
use this to check for advertisement issues

headline1 = driver.find_elements_by_xpath('//*[@id="quoteNewsStream-0-Stream"]/ul/li[4]/div/div/div[1]/h3/a')
print(len(headline1))
print(headline1[0].text)
print('--------------------')

headline2 = driver.find_elements_by_xpath('//*[@id="quoteNewsStream-0-Stream"]/ul/li[4]/div/div/div[2]/h3/a')
print(len(headline2))
print(headline2[0].text)
print('--------------------')

'''

