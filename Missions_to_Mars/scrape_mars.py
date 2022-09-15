# import dependencies


from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import time


# scrape all function

def scrape_all():
    # print("hello")Just to see if the code is working and printing in git bash
    # the main goal of having scrape_all function is to retunr a json dictionary that has all the data from the scraped websites and loaded onto mongo db
    # Setup splinter

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # get the information from the news page
    news_title, news_p = scrape_news(browser)
    # build a dictionary using the information from all the scrapes from the websites
    marsData = {
        "news_Title": news_title,
        "NewsParagraph": news_p,
        "featured_Image": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemisphere_URLS": scrape_hemispheres(browser),
        "Updated_date": dt.datetime.now()
    }

    # stop the webdriver
    browser.quit()

    # display the dictionary output
    return marsData


# scrape the mars news page
def scrape_news(browser):
    # go to the Mars Nasa News Website
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # optional delay fpr laoding the page
    browser.is_element_present_by_css('div.list.text', wait_time=1)

    # convert the browser html to a soup object
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    quotes = news_soup.select_one('div', class_='list_text')


    title = quotes.find('div', class_='content_title').get_text()
    #print(title)
    news_title = title
    #news_title

    paragraph = quotes.find('div', class_ ='article_teaser_body').get_text()
    news_p = paragraph

    # return the title nd the paragraph so that we can put it the idctionary
    return news_title, news_p


# scrape through the featured image page
def scrape_feature_img(browser):
    # URL of page to be scraped
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # find and click the full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    # Then parse out the image page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    DustySpaceCloud = soup.find('div', class_='floating_text_area')

    #link = DustySpaceCloud.a["href"]

    #print(f"https://spaceimages-mars.com/{link}")

    featured_image_url = f"{url + DustySpaceCloud.a['href']}"
    featured_image_url

    # return the image url
    return featured_image_url


# scrape through the facts page
def scrape_facts_page(browser):
    # the pandas code wont work here to we will use :
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # Then parse out the facts table
    html = browser.html
    fact_soup = BeautifulSoup(html, 'html.parser')

    # find the facts location
    factsLocation = fact_soup.find('div', class_='diagram mt-4')
    # this grabs the html code for the facts table
    factTable = factsLocation.find('table')

    # we can create and add this to an empty string
    facts = ""

    # add the text from factTable to the empty string then return
    facts += str(factTable)

    return facts


# scrape through the hemispheres pages

def scrape_hemispheres(browser):
    # base url
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles
    hemisphere_ImageURLS = []

    # Getting a list of all of the hemispheres
    links = browser.find_by_css('a.product-item img')


    # set up the loop
    for link in range(len(links)):
            
        #hemisphere info dictionary
        hemisphereInfo={}

        # we have to find the elements in each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[link].click()
        time.sleep(2)
        
        # We need to find the text "sample" and find the image url for that sample text
        SampleText = browser.links.find_by_text('Sample').first
    #     print(SampleText['href'])
        hemisphereInfo["img_url"] =SampleText['href']
        
        
        # Get Hemisphere title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
        
        #Append hemisphere object to list
        hemisphere_ImageURLS.append(hemisphereInfo)
        
        
        
        # finally we navigate backwards
        browser.back()
    return hemisphere_ImageURLS

# set up as a flask app
if __name__ == "__main__":
    print(scrape_all())
