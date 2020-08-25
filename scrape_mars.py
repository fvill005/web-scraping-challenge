# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests
import pymongo

#set up connection to mongo
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 

# Initialize browser
def init_browser(): 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


# NASA MARS NEWS
def scrape():
    browser = init_browser()
    mars_data_scrape = {}

    #scraping for the title and paragraph 
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('div', class_='list_text')
    news_title = article.find('div', class_='content_title').text()
    news_p = soup.find('div', class_='article_teaser_body').text()
    mars_data_scrape["data1"] = news_title
    mars_data_scrape["data2"] = news_p
    
    # #looking for thr jpl image
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    html_jpl_image = browser.html
    soup = BeautifulSoup(html_jpl_image, 'html.parser') 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + featured_image_url
    mars_data_scrape["image"] = featured_img_url

    #scraping info for the mars facts
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    mars_facts_df = table[0]
    mars_facts_df.columns = ['Mars Planet Profile', ' ']
    mars_facts_hmtl_table = mars_facts_df.to_html()
    mars_facts_df.to_html('mars_facts.html')
    mars_data_scrape["table"] = mars_facts_df.to_html()


    #scraping for hemispheres images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hemi_html = browser.html
    soup = BeautifulSoup(hemi_html, 'html.parser')

    images = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

#loop for scraping the images and appending to list
    for image in images: 
   
        title = item.find('h3').text
        image_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + image_url)
        image_html = browser.html
        soup = BeautifulSoup( image_html, 'html.parser')
        image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"Title" : title, "Image_URL" : image_url})
        mars_data_scrape["hemispheres"] = hem_img_urls


    return mars_data_scrape

