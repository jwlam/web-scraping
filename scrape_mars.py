from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scraper():
    browser = init_browser
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    html = browser.html
    soup = soup(html, 'html.parser')

    article = soup.find('div', class_='list_text')
    news_title = article.find('a').text
    news_p = article.find('div', class_='article_teaser_body').text

    feat_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_split = feat_img_url.split('/spaceimages', 1)
    browser.visit(feat_img_url)
    img_details = soup.find('div', id='secondary_column').find_all('div', class_='download_tiff')
    hires_url = img_details[1].find('a')['href']
    featured_image_url = 'https:' + hires_url

    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)
    mars_df = table[0]
    mars_df.columns = ['Description', 'Values']
    mars_df.set_index('Description', inplace=True)
    