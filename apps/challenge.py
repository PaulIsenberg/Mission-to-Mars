# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import traceback


executable_path = {'executable_path': 'C:/Users/pauli/Web_Scraping/chromedriver.exe'}
browser = Browser("chrome", **executable_path, headless=True)


def scrape_all():
   # Initiate headless driver for deployment
# Set the executable path and initialize the chrome browser in splinter
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemisphere": hemisphere_images(),
      "last_modified": dt.datetime.now()
    }
    #browser.quit()
    return data

## FIRST SCRAPE
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add Try/Except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')  

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        
    except AttributeError:
        return None, None

    # Adds Return Statement that includes News Title and Paragraph
    return news_title, news_p

# ### Featured Images
## SECOND SCRAPE
# Visit URL
def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

## MARS FACTS
def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    traceback.print_exc()    
    return df.to_html()


## THIRD SCRAPE
# Visit URL
def hemisphere_images():
    #executable_path = {'executable_path': 'chromedriver'}
    #browser = Browser('chrome', **executable_path)
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemi_url = []

    hemi_home = browser.find_by_css("a.product-item h3")
    for hemi in range(len(hemi_home)):
        hemi = {}
        browser.find_by_css("a.product-item h3")[hemi].click()
        sample_elem = browser.find_link_by_text('Sample').first
        hemi['img_url'] = sample_elem['href']
        hemi['title'] = browser.find_by_css("h2.title").text     
        hemi_url.append(hemi)     
        browser.back()
    
    
    
    
    #url = 'https://www.astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #browser.visit(url)
    #hemi_url = []
    #html = browser.html
    #img_soup = BeautifulSoup(html, 'html.parser')
    #hemi_home = browser.find_by_css("a.product-item h3")
    
    #print(hemi_home)
    
    #for hemi in hemi_home:
        #hemi.click()
        #hemi_html = browser.html
        #hemi_title=BeautifulSoup(hemi_html, 'html.parser')
        #hemi_img = hemi_title.find('img', class_='wide-image').find('src')
        #title = hemi_title.find('h2', class_='title')
        #hemi_url.append({'title': title, 'img_url': hemi_img}) 
        #return hemi_url
        






if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
