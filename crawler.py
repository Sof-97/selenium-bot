from selenium.webdriver import Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import sleep
import pandas as pd

LINKEDIN = 'https://it.linkedin.com/'
EMAIL = 'testlinkedin2343@gmail.com'
PASSWORD = 'Appius_2022!'

QUERY = 'React Developer'

data = {'name': [],'summary': [],'city': [],}

#TODO ADD TOKEN ANTY CAPTCHA
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
chrome_driver = ChromeDriverManager().install()
driver  = Chrome(service=Service(chrome_driver), options=options)
driver.maximize_window()
driver.get(LINKEDIN)



def submit_login(user_name, user_password):
    #GET INPUT 
    username = driver.find_element(by=By.XPATH, value="//input[@name='session_key']")
    password = driver.find_element(by=By.XPATH, value="//input[@name='session_password']")

    #COMPILE FORM
    username.send_keys(user_name)
    password.send_keys(user_password)

    #SUBMIT LOGIN
    sleep(2)
    submit = driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()
    #TODO increase sleep time to get captcha verified
    sleep(15)

def search_person(query):
    #SELECT SEARCH INPUT   --and submit
    search_input = driver.find_element(by=By.XPATH, value="//input[@aria-label='Cerca']")
    search_input.send_keys(query)
    search_input.send_keys('\uE007')
    sleep(4)
    #SELECT PEOPLES TAB
    peoples_button = driver.find_elements(by=By.CSS_SELECTOR, value="ul.search-reusables__filter-list li button")
    people_btn = [btn for btn in peoples_button if btn.text == 'Persone']
    sleep(1)
    people_btn[0].click()
    sleep(4)

def get_info():
    #SELECT PEOPLE INFO FROM LIST
    #TODO CLEAN RESULTS FROM EMOJI AND CUSTOM UNICODE
    list_elements = driver.find_elements(by=By.CSS_SELECTOR, value="li .entity-result__content.entity-result__divider")
    for element in list_elements:
        title = element.find_elements(by=By.CSS_SELECTOR, value="span.entity-result__title-line a span span:first-child")
        if len(title) > 0:
            summary = element.find_element(by=By.CSS_SELECTOR, value='div.entity-result__primary-subtitle')
            city = element.find_element(by=By.CSS_SELECTOR, value='div.entity-result__secondary-subtitle')
            data['name'].append(title[0].text)
            data['summary'].append(summary.text)
            data['city'].append(city.text)

#SCRIPT START
submit_login(EMAIL, PASSWORD )

search_person(QUERY)

get_info()

#TO THE NEXT PAGE
driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
sleep(4)
next = driver.find_element(by=By.XPATH, value="//button[@aria-label='Avanti']")
print(next.text)
sleep(4)
next.click()
sleep(2)
get_info()
sleep(2)
get_info()

df = pd.DataFrame(data)
df.to_csv('people.csv')

while True: 
    sleep(1)