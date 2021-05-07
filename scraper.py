from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.binary_location = "/usr/bin/chromium-browser"
#chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works


def waitForLoad(driver, elementId, by=By.ID):
    try:
        element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((by, elementId)))
    finally:
        print("Page loaded")

def login_to_facebook(driver, login_url, credentials):
    driver.get(login_url)
    waitForLoad(driver, 'm_login_email')

    username = driver.find_element_by_id("m_login_email")
    password = driver.find_element_by_id("m_login_password")

    username.send_keys(credentials['mail'])
    password.send_keys(credentials['password'])

    driver.find_element_by_id("signup-button").click()

def saler(story):
    return story.find_element_by_xpath("//strong/a").get_attribute('innerHTML')

def saler_location(details):
    return get_text(details[2])

def article_name(details):
    return get_text(details[1])

def article_description(details):
    return get_text(details[3])

def get_text(html_element):
    return html_element.get_attribute('innerHTML')

def get_article_from_group(story):
    details = story.find_elements_by_xpath(".//child::header//following-sibling::div[2]//span")
    return {'name' : article_name(details),
            'saler_name' : saler(story),
            'price' : 0,
            'description' : article_description(details),
            'saler_number' : '',
            'image_url' : '',
            'location' : saler_location(details)}

def get_articles_from_group(driver, group_url):
    driver.get(group_url)
    waitForLoad(driver, 'm_group_stories_container')
    stories = driver.find_elements_by_css_selector("article")

    return [get_article_from_group(story) for story in stories[:4]]

driver = webdriver.Chrome(options=chrome_options)
login_url = "https://m.facebook.com/login"
group_url = "https://m.facebook.com/groups/816783068805198"
credentials = {"mail" : "glodymbutwile@gmail.com", "password" : "hmpez118"}

login_to_facebook(driver, login_url, credentials)
time.sleep(3)
articles = get_articles_from_group(driver, group_url)

print(articles)



#driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

#print(driver.page_source.encode("utf-8"))
#driver.quit()
