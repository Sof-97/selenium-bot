from sqlite3 import connect
from selenium.webdriver import Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import sleep

LINKEDIN = 'https://it.linkedin.com/'

TEXT_MESSAGE = 'Questo è un messaggio di test automatizzato.'

options = webdriver.ChromeOptions()
options.add_argument("--incognito")

chrome_driver = ChromeDriverManager().install()
driver  = Chrome(service=Service(chrome_driver), options=options)
driver.maximize_window()
driver.get(LINKEDIN)

def basic_connect():
    #ERROR CATCHING EMAIL
    email_error = len(driver.find_elements(by=By.XPATH, value="//input[@name='email']")) > 0

    if email_error == False:    
        #OPEN MESSAGE INPUT
        sleep(3)
        note_button = driver.find_element(by=By.XPATH, value="//button[@aria-label='Aggiungi una nota']")
        sleep(1)
        note_button.click()
        sleep(3)

        # #TYPE MESSAGE
        textarea = driver.find_element(by=By.CSS_SELECTOR, value="textarea#custom-message")
        sleep(1)
        textarea.send_keys(TEXT_MESSAGE)
        sleep(1)

#GET INPUT 
username = driver.find_element(by=By.XPATH, value="//input[@name='session_key']")
password = driver.find_element(by=By.XPATH, value="//input[@name='session_password']")

#COMPILE FORM
username.send_keys('testlinkedin2343@gmail.com')
password.send_keys('Appius_2022!')

#SUBMIT LOGIN
sleep(2)
submit = driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()
#TODO increase sleep time to get captcha verified
sleep(15)

#SELECT SEARCH INPUT   --and submit
search_input = driver.find_element(by=By.XPATH, value="//input[@aria-label='Cerca']")
search_input.send_keys('Francesco Ma \uE007')
sleep(4)

#SELECT PEOPLES TAB
peoples_button = driver.find_elements(by=By.CSS_SELECTOR, value="ul.search-reusables__filter-list li button")
people_btn = [btn for btn in peoples_button if btn.text == 'Persone']
sleep(1)
people_btn[0].click()
sleep(4)

#SELECT N ITERATION OF INTERACTION BUTTONS
interaction_buttons = driver.find_elements(by=By.TAG_NAME, value='button')
connect_buttons = [btn for btn in interaction_buttons if btn.text == 'Collegati']
sleep(1)

#CLICK ON FIRST CONNECT BUTTON
connect_buttons[0].click()

basic_connect()

#KEEP ON
while True:
    sleep(1)
