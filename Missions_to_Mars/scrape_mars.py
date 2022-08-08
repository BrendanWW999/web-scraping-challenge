from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import pymongo
from time import sleep

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    # NASA Mars News

    url = 'https://redplanetscience.com'
    browser.visit(url)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    slide_elem.find('div', class_='content_title')
    slide_elem.find('div', class_='article_teaser_body')
    news_title = slide_elem.find('div', class_='content_title')
    news_p = slide_elem.find('div', class_='article_teaser_body')

    mars_data = {
    "news_title": news_title,
    "news_p": news_p
    }

    # JPL Mars Space Images - Featured Image

    sleep(1)

    url2 = 'https://spaceimages-mars.com'
    browser.visit(url2)
    html2 = browser.html
    pic_soup = soup(html2, 'html.parser')
    img1 = pic_soup.find_all('img')[1]["src"]
    featured_image_url = url2 + "/" + img1
    mars_data.update( {'featured_image_url' : featured_image_url,
                        'featured_image_source' : url2} )
    # Mars Facts

    sleep(1)

    url3 = 'https://galaxyfacts-mars.com'
    browser.visit(url3)
    facts_table = pd.read_html(url3)
    mars_df = facts_table[1]
    html_mars_table = mars_df.to_html(classes = 'table table-striped')
    mars_data.update( {'html_table' :  html_mars_table,
                        'facts_source':  url3} )
    # Mars Hemispheres

    sleep(1)

    url4 = 'https://marshemispheres.com'
    browser.visit(url4)
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item img')
    for x in range(len(links)):
        hemisphere = {}
        browser.find_by_css('a.product-item img')[x].click()
        element = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = element['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    mars_data.update( {'hemi_img_urls': hemisphere_image_urls} )
    browser.quit()
    return mars_data