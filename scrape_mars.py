from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time

def init_browser():
    #mac chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

    #windows chromedriver
    #executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scraper():
    browser = init_browser()
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    html = browser.html
    soup_new = soup(html, 'html.parser')

    article = soup_new.find('li', class_='slide')
    news_title = article.find('div', class_='content_title').text
    news_p = article.find('div', class_='article_teaser_body').text

    feat_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_split = feat_img_url.split('/spaceimages', 1)
    browser.visit(feat_img_url)
    img_details = soup_new.find('div', id='secondary_column').find_all('div', class_='download_tiff')
    hires_url = img_details[1].find('a')['href']
    featured_image_url = 'https:' + hires_url

    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)
    mars_df = table[0]
    mars_df.columns = ['Description', 'Values']
    mars_df.set_index('Description', inplace=True)
    mars_html_table = mars_df.to_html()
    mars_html_table = mars_html_table.replace('\n', '')

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_split = hemi_url.split('/search',1)
    browser.visit(hemi_url)
    hemi_soup = soup_new.find('div', class_='collapsible results')
    hemi_pages = hemi_soup.find_all('div', class_='item')
    
    hemisphere_image_urls = []

    for page in hemi_pages:
        hemi_dict = {}
        title = page.find('div', class_='description').find('a').text
        hemi_dict['title'] = title
        hemi_link = page.find('div', class_='description').find('a')['href']
        browser.visit(hemi_split[0] + hemi_link)
        hemi_html = browser.html
        hemisphere_soup = soup_new(hemi_html, 'html.parser')
        hemi_img = hemisphere_soup.find('div', class_='content').find('a')['href]']
        hemi_dict['img_url'] = hemi_img
        hemisphere_image_urls.append(hemi_dict)
        browser.back()
    browser.quit

    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_html_table': mars_html_table,
        'hemisphere_image_urls': hemisphere_image_urls
    }
    return mars_data
if __name__ == '__main__':
    print(scraper())
