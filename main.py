import os
import asyncio
import configparser
import urllib
import webbrowser
import subprocess
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import sys
from colorama import init
init(strip=not sys.stdout.isatty())
from colorama import Fore, Back, Style
from telethon import *
import telethon
from termcolor import cprint
from pyfiglet import figlet_format
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import geckodriver_autoinstaller
from urlextract import URLExtract
import re
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


threedsswitch = '2'  #1 For YAP #2 For Hype


print(figlet_format('LDLC Fucker!', font='slant'))
print("A very good LDLC Bot by @R3ychards --> in only 3 days!")

#Verify and install gekodriver, disabled on macos
#geckodriver_autoinstaller.install()


#DEFINE MAIN BOT ACTIONS
def LDLC_Fucker(uri):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path='./chromedriver_98', options=options)
    driver.get("https://secure2.ldlc.com/it-it/Login/Login?returnUrl=%2Fit-it%2FAccount")

    # Insert login_data
    email_form = driver.find_element_by_id("Email")
    email_form.clear()

    emailParts = 'HERE'.split('@') #Insert your email here
    emailElement = driver.find_element_by_id("Email")

    emailElement.send_keys(emailParts[0])
    action = ActionChains(driver)
    action.key_down(Keys.ALT).send_keys('ò').key_up(Keys.ALT).perform()
    emailElement.send_keys(emailParts[1])

    time.sleep(0.05)

    pwd_form = driver.find_element_by_id("Password")
    pwd_form.clear()
    pwd_form.send_keys("") # Insert your password here

    make_login = driver.find_element_by_xpath("/html/body/div[3]/div/form/button").click()

    # END LOGIN SECTION

    # LOAD PAGE
    driver.get(uri)

    # INIT_CHECKOUT
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[3]/button").click()
    time.sleep(0.2)
    driver.save_screenshot('element.png')
    proc = subprocess.Popen("python3 ./Send_Screenshot.py", stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)
    proc.communicate()[0]
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="product-page-price"]/div[2]/button[2]').click()

    # Scroll to needed section

    actionscroll = ActionChains(driver)
    time.sleep(2.3)
    actionscroll.key_down(Keys.PAGE_DOWN).key_down(Keys.PAGE_DOWN).key_down(Keys.PAGE_DOWN).perform()

    # CHECKOUT DATA, split the numbers into 4 sectors
    cardnr1 = "1111"
    caardnr2 = "2222 "
    cardnr3 = "3333 "
    cardnr4 = "4444"
    validthru = "0523" # Expiry date
    cvv = "123" #CVV here
    cardhldr = "R3ychards!" #Card Holder
    cardver="050802" #Password of the APP, YAP does request this.
    time.sleep(5)

    # CHECKOUT[CODE]

    driver.switch_to.frame('cardNumber')

    cardins = driver.find_element_by_id("checkout-frames-card-number")
    cardins.clear()
    cardins.send_keys(cardnr1)
    cardins.send_keys(caardnr2)
    cardins.send_keys(cardnr3)
    cardins.send_keys(cardnr4)

    print("Wrote Card Nr")

    driver.switch_to.parent_frame()
    print("Switching back from iframe to main window...")
    print("Switching now to expirydate's iframe...")
    driver.switch_to.frame('expiryDate')

    cardins = driver.find_element_by_id("checkout-frames-expiry-date")
    cardins.clear()
    cardins.send_keys(validthru)
    print("Wrote expiry date")

    driver.switch_to.parent_frame()
    print("Switching back from iframe to main window...")
    print("Switching now to cvv's iframe...")
    driver.switch_to.frame('checkout-frames-cvv')

    cardins = driver.find_element_by_id("checkout-frames-cvv")
    cardins.clear()
    cardins.send_keys(cvv)
    print("Wrote CVV")

    driver.switch_to.parent_frame()
    print("Switching back from cvv iframe to main window...")

    cardins = driver.find_element_by_id("CardHolder")
    cardins.clear()
    cardins.send_keys(cardhldr)
    print("Wrote Card Holder")

    print("Sending order...")
    driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[2]/div[1]/div/div/form/div[8]/div/button').click()
    time.sleep(10)
    cururl = driver.current_url
    print (cururl)
    if 'api.checkout.com' in cururl:
        if threedsswitch == '0':
            print("NO 3DS automation used.")
        if threedsswitch == '1':
            yap3ds(driver, cardver)
        if threedsswitch == '2':
            hype3ds(driver)


    print("Order Successful!")
    time.sleep(17)
    driver.save_screenshot('ordercomplete.png')
    time.sleep(1)
    proc = subprocess.Popen("python3 ./Send_Screenshot_Ordercomplete.py", stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)
    proc.communicate()[0]
    time.sleep (100)

#Define yap 3ds bypass
def yap3ds(driver, cardver):
    print("Oh nooo, 3DS verification is required, sending req for the code on telegram")
    driver.switch_to.frame('cko-3ds2-iframe')
    print("Switched to 3DS verification frame")
    proc = subprocess.Popen("python3 ./Get3dsVerification.py", stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)
    output = proc.communicate()[0]
    dec = output.decode("utf-8")
    print(dec)
    if len(dec) < 6:
        dec = str(dec).zfill(6)
        print(dec)
    print("OTP->" + str(dec))
    print("Acc_PWD ->" + str(cardver))
    count = 0
    c3ds = [int(d) for d in str(dec)]
    print(c3ds)
    vercode = [int(float(d)) for d in str(cardver)]

    driver.find_element_by_id('challenge_1').send_keys(c3ds[0])
    driver.find_element_by_id('challenge_2').send_keys(c3ds[1])
    driver.find_element_by_id('challenge_3').send_keys(c3ds[2])
    driver.find_element_by_id('challenge_4').send_keys(c3ds[3])
    driver.find_element_by_id('challenge_5').send_keys(c3ds[4])
    driver.find_element_by_id('challenge_6').send_keys(c3ds[5])
    driver.find_element_by_id('btnConferma').click()

    time.sleep(1)

    # second verification:

    driver.find_element_by_id('key6_1').send_keys(vercode[0])
    driver.find_element_by_id('key6_2').send_keys(vercode[1])
    driver.find_element_by_id('key6_3').send_keys(vercode[2])
    driver.find_element_by_id('key6_4').send_keys(vercode[3])
    driver.find_element_by_id('key6_5').send_keys(vercode[4])
    driver.find_element_by_id('key6_6').send_keys(vercode[5])

    driver.find_element_by_id('btnConferma').click()

    print("YAP 3DS Completato!")

#Define Hype 3ds bypass
def hype3ds(driver):
    print("Initializing Hype 3ds Bypass..")

    print("Switching to 3ds env frame")
    driver.switch_to.frame('cko-3ds2-iframe')
    print("Asking for the client to confirm the transaction..")
    proc = subprocess.Popen("python3 ./Get3dsVerification_Hype.py", stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)
    output = proc.communicate()[0]
    output.decode("utf-8")
    print(output)
    if "confirmed" in output:
        print("User confirmation recieved, pressing button in 3 secs")
        time.sleep(3)
        driver.find_element_by_id('confirm').click()
    print("Hype 3ds Completato!")

#DEFINE Uri Extractor
def UrlExtract(url):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\
    -]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))" \
            r"*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>" \
            r"?«»“”‘’]))"
    urls = re.findall(regex, str(url))
    print(str(urls))
    urls = str(urls)
    extractor = URLExtract()
    uri = extractor.find_urls(urls)
    print(uri[0])
    return uri[0]


#read ini files
config=configparser.ConfigParser()
config.read("config.ini")

#Setting Config_Values
api_id=config.get('telegram', 'api_id')
api_hash=config.get('telegram', 'api_hash')

api_hash = str(api_hash)

phone=config.get('telegram', 'phone')
username=config.get('telegram', 'username')

#Creating Telegram Client Enviroment
client=TelegramClient(username, api_id, api_hash)
client.start()
a=client.is_connected()
print("")
print(username, " / Logged:", a)
print("")

print(Fore.GREEN)
print("Client init successfully.")
print(Style.RESET_ALL)
print("")
time.sleep(1)


#End of Login
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (PeerChannel)

#Main Function #🔥 FE PartAlert

print ("Listening to the channel, waiting for the drop!")
@client.on(events.NewMessage(chats="🔥 FE PartAlert"))
async def MainEvent(event):
    print(event.raw_text)
    dialog = event.raw_text
    if "Nvidia Italy" in dialog:  # PLEASE CHANGE IT TO THE DESIRED DROP WEBSITE!!!!!!!!
        print("LDLC DROP! OMG It's HAPPENING!!!!!")
        if "FE Nvidia GeForce RTX 3060 Ti (IT)" in dialog:
            print(figlet_format('3060 Ti DETECTED!!',font = 'slant' ))
            uri = UrlExtract(dialog)
            print("Uri = " + uri)
            LDLC_Fucker(uri)


client.run_until_disconnected()
# do things
