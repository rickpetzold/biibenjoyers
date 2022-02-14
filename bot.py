import argparse
import sys
from datetime import date
from datetime import datetime
from datetime import timedelta
import time
import pickle
from random import random

import get_captcha

from PIL import Image
from xml.dom.minidom import getDOMImplementation
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def login(browser, name="", password="", mode="new", login_time=8, tries=0): 
    tries += 1
    # Click "Anmelden"
    if mode == "new":
        browser.find_element(By.XPATH, "//*[@action='admin.php']//*[@value=' Anmelden ']").click()
    else:
        pass

    browser.save_screenshot(r"temp/screen.png")

    # Get captcha
    captcha = get_captcha.get_captcha()

    # Send keys
    name_field = browser.find_element(By.XPATH, "//input[@id='NewUserName']")
    password_field = browser.find_element(By.XPATH,"//input[@id='NewUserPassword']")
    captcha_field = browser.find_element(By.XPATH, "//input[@id='Captcha_INPUT']")

    name_field.send_keys(name)
    password_field.send_keys(password)
    captcha_field.send_keys(captcha)
    #time.sleep(1)
    browser.find_element(By.XPATH, "//input[@id='EULA_INPUT']").click()

    # Sleep and send
    rand_sec = random()
    time.sleep(rand_sec+login_time)
    
    try:
        browser.find_element(By.XPATH, "//input[@class='submit']").click()
    except:
        pass
    
    # Wrong captach: recursive call
    time.sleep(2)
    print(f"Login try: {tries}")

    if browser.find_element(By.XPATH, "//body").text == "Sie müssen den Captcha-Text korrekt übergeben!" or browser.find_element(By.XPATH, "//td/div[@id='logon_box']/form[@method='post']/div/input[@type='submit']").get_attribute("value") == " Anmelden ":
        browser.get("https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/admin.php")
        login(browser, name=name, password=password, mode="again", login_time=login_time, tries=tries)

    return tries

    
   
def get_seat(browser, seat_numbers, slot = "", favorites=list(), mode="schedule"):

    reserved = False # Boolean for seat
    marked = False # Boolean for favorite seat
    indices = list()
    counter = 0

    # Fast mode
    if mode=="fast": 
        try:
            seats = browser.find_elements(By.XPATH, f"//tr/td[div/a[text()='{slot}']]/following-sibling::td[@class='new']")
            seats[-1].click()
            browser.find_element(By.XPATH, "//input[@class='submit default_action']").click()
            reserved=True
            return reserved
        except:
            return reserved

    # Schedule mode
    seats = browser.find_elements(By.XPATH, f"//tr/td[div/a[text()='{slot}']]/following-sibling::td[not(@class='row_labels')]")
    for seat in seats:
        if seat.find_element(By.XPATH, ".//div/a").get_attribute("title") != "[X]" and seat.get_attribute("class") != "K writable":
            indices.append(counter)
        counter+=1

    # No seats
    if not indices:
        return reserved
    else: 
        print("Seats available")

    # Free seats
    ## Check favorites
    if favorites: 
        # Set of favorites
        fav_seats_index = set()
        for fav in favorites: 
            try:
                fav_seats_index.add(seat_numbers[fav])
            except:
                pass
        
        ### Check if free seat index in favorites index list
        for ind in indices: 
            if ind in fav_seats_index: 
                seats[ind].click()
                browser.find_element(By.XPATH, "//input[@class='submit default_action']").click()
                marked=True
                reserved=True
                print("Got favorite seat!\n")
                break

    if not marked: 
        seats[indices[-1]].click()
        browser.find_element(By.XPATH, "//input[@class='submit default_action']").click()
        reserved=True
        print("Favorite seat missed, got alternative\n")
    
    return reserved

def main(name="", password="", floor = "Altbau EG KIT-BIB (LBS)", slot = "nachmittags", favorites=[], area=20, start_time=200, booking_time=10, login_time=8, mode="schedule"):

    today = date.today()
    now = datetime.now()
    
    firefox_options=Options()
    firefox_options.add_argument("--log-level=OFF")
    #firefox_options.add_argument("--headless")
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
    print("================================\n")

    day = int(today.strftime("%d"))
    month = today.strftime("%m")
    year = today.strftime("%Y")
    hour = int(now.strftime("%H"))

    """
    Time
    """
    if mode == "schedule":
        if hour >= 8 and hour <=9: 
            slot = "vormittags"
        
        elif hour >=18 and hour <= 19: 
            slot = "abends"
        else: 
            ## Book for midday slot in 3 days
            slot = "nachmittags"
            day+=3

    elif mode == "fast":
        slot=slot

    assert slot in set(["nachmittags", "vormittags", "abends", "nachts"]), "Slot: Falscher Zeitraum"


    print(f"Hour: {hour}")
    print(f"Target day: {day}")
    print(f"Trying to get a slot in: {slot}")
    print(f"Floor: {floor}")
    if favorites:
        print("Preferred seats: ")
        print(favorites)
        print("\n")
    else:
        print("Preferred seats: none\n")


    ### 1. Get page
    loaded = False
    while not loaded:
        try:
            browser.get(f"https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/day.php?year={year}&month={month}&day={day}&area=20&room=826")
            loaded=True
        except:
            pass

    ### 2. Login
    try:
        browser.find_element(By.XPATH, "//*[@action='admin.php']//*[@value=' Anmelden ']")
        login(browser, name=name, password=password, login_time=login_time)
    except: 
       print("Error: Login failed")

    ### Timer between login and specified time
    try:
        start_year = int(start_time[0])
        start_month = int(start_time[1])
        start_day = int(start_time[2])
        start_hour = int(start_time[3])
        start_min = int(start_time[4])
        start_sec = int(start_time[5])

        start_date = datetime(start_year, start_month, start_day, start_hour, start_min, start_sec)
        print(f"-> Planned start date and time: {start_date.strftime('%y-%m-%d %H:%M:%S')}\n")
    except: 
        print("-> Start date format wrong")
        print("Start date and time: now\n")
        start_date = datetime.now()


    print("->Preserving session...")
    counter_sec = 0
    while datetime.now() < start_date: 
        time.sleep(1)
        if datetime.now() >= start_date:
            break
        counter_sec += 1

        if counter_sec == 20:
            print(f"Refresh at: {datetime.now().strftime('%y-%m-%d %H:%M:%S')}")
            browser.find_element(By.XPATH, "//td[@id='company']/div/div/a[text()='Sitzplatzreservierung']").click()
            WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "//td[@id='company']/div/div/a[text()='Sitzplatzreservierung']")))
            counter_sec = 0
    print("Starting booking process...\n")

    
    ### 3. Get seat
    status = False
    browser.get(f"https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/day.php?year={year}&month={month}&day={day}&area={area}")
    start = datetime.now()
    end = start + timedelta(seconds=booking_time)
    print(f" >>> Start time: {start.strftime('%y-%m-%d %H:%M:%S')}")
    print(f" >>> Projected end time: {end.strftime('%y-%m-%d %H:%M:%S')}")

    while not status: 
        browser.refresh()
        print(f"Run at: {datetime.now().strftime('%y-%m-%d %H:%M:%S')}")
        print("---Finding seat...")
        status = get_seat(browser, seat_numbers, slot=slot, favorites=favorites, mode=mode)
        
        if datetime.now() > end: 
            break
    print("Booking time up\n")

    if not status: 
        print("Error: Seat not reserved")
    else:
        print("================")
        print("Success")
        print("================\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Arguments for bibbot")
    parser.add_argument("-u", help="Login username", required=True)
    parser.add_argument("-p", help="Login password", required=True)
    parser.add_argument("-fl", help="Floor number, options: 1 (1.OG neu) 2 (2.OG neu) 3 (3.OG neu) A1 (1.OG Alt) A2 (2.OG Alt) A2E (2.OG Alt Empore) A3 (3.OG Alt) AE (Alt EG)", required=True)
    parser.add_argument("-m", help="Mode: fast or schedule (fast omitts favorites and grabs last seat, very fast and used for today, requires slot; schedule respects favorite seats and sets slot to: (if time bet(8,9): vormittags), (18,19: abends), (else: nachmittags and day+3))", required=True)
    parser.add_argument("-s", help="Timeslot, applicable when in fast mode")
    parser.add_argument("-lt", help="Login: Base waiting time, added to random amount of a second [seconds]")
    parser.add_argument("-bt", help="booking time in which booking is retried [seconds]")
    parser.add_argument("-fa", nargs="*", help="Preferred seat numbers seperated by space, optional")
    parser.add_argument("-st", nargs="*", help="starting date and time for booking [yyyy mm dd HH MM SS], possible for both fast and schedule")
    
    args = parser.parse_args()._get_kwargs()
    
    floor=""
    for tup in args: 
        if tup[0] == 'u': 
            username = tup[1]
        elif tup[0] == 'p': 
            password = tup[1]
        elif tup[0] == 'fl':
            with open("seat_dict/seat_numbers.pickle", "rb") as handle: 
                seat_dic = pickle.load(handle)
                
                seat_numbers = seat_dic[tup[1]][0]
                floor = seat_dic[tup[1]][1]
                area = seat_dic[tup[1]][2]

        elif tup[0] == 'm':
            mode = tup[1]
        
        elif tup[0] == "s": 
            slot = tup[1]
        
        elif tup[0] == 'lt':
            try:
                login_time = int(tup[1])
            except:
                login_time = 0

        elif tup[0] == 'fa':
            try:
                favorites = tup[1]
                for i in range(len(favorites)): 
                    favorites[i] = str(favorites[i])
            except: 
                favorites = list()

        elif tup[0] == 'bt': 
            try:
                booking_time = int(tup[1])
            except:
                booking_time = 0

        elif tup[0] == 'st': 
            start_time = tup[1]
        
    if mode == "fast": 
        assert booking_time, "Specify how long to retry booking with [-bt ...]"
        assert slot, "Specify timeslot for today with [-s ...] "
        assert not start_time, "Fast mode starts after login time for the intervall specified in booking time [bt]"
    elif mode == "schedule": 
        assert booking_time, "Specify how long to retry booking with [-bt ...]"
        assert start_time, "Specify start date and time for booking seat [-st yyyy mm dd HH MM SS]"
        assert not slot, "Slot is automatically calculated: (if time bet(8,9): vormittags), (18,19: abends), (else: nachmittags and day+3)"
        

    

    main(name=username, password=password, floor=floor, slot=slot, mode=mode, favorites=favorites, area=area, login_time=login_time, booking_time=booking_time, start_time=start_time)