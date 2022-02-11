from datetime import date
import time

import get_captcha

from xml.dom.minidom import getDOMImplementation
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(browser, name="", password=""):

    failed = False

    # Click "Anmelden"
    browser.find_element_by_xpath("//*[@action='admin.php']//*[@value=' Anmelden ']").click()
    browser.save_screenshot("screen.png")

    # Get captcha
    captcha = get_captcha.get_captcha()
    
    # Send keys
    name_field = browser.find_element_by_xpath("//input[@id='NewUserName']")
    password_field = browser.find_element_by_xpath("//input[@id='NewUserPassword']")
    captcha_field = browser.find_element_by_xpath("//input[@id='Captcha_INPUT']")

    name_field.send_keys(name)
    password_field.send_keys(password)
    captcha_field.send_keys(captcha)
    browser.find_element_by_xpath("//input[@id='EULA_INPUT']").click()

    # Click
    time.sleep(3)
    browser.find_element_by_xpath("//input[@class='submit']").click()


    print(browser.find_element_by_xpath("//body").getText())
    
    while browser.find_element_by_xpath("//body").getText() == "Sie müssen den Captcha-Text korrekt übergeben!":
        #time.sleep(2)
        browser.refresh()

        try:
            WebDriverWait(browser, 3).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')
            alert = browser.switch_to.alert
            alert.accept()

            captcha = get_captcha.get_captcha()

            name_field.send_keys(name)
            password_field.send_keys(password)
            captcha_field.send_keys(captcha)
            browser.find_element_by_xpath("//input[@id='EULA_INPUT']").click()
            
        except:
            pass
        

def main(name="", password="", favorites=[]):
    today = date.today()
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%Y")
    print(day, month, year)
    
    browser.get(f"https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/day.php?year={year}&month={month}&day={12}&area=20&room=826")

    ### login

    try:
        browser.find_element_by_xpath("//*[@action='admin.php']//*[@value=' Anmelden ']")
        login(browser, name=name, password=password)
        ### call login func


    except: 
        pass
    

if __name__ == "__main__":
    main(name="@2111682", password="riKIT33ik()")