#!/usr/bin/env python
import sys
import os 
import time
import requests
import py_imgcat
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from colorama import Fore
from art import *
import warnings
import traceback
warnings.filterwarnings('ignore')

def print_header():
        ascii_header = text2art("LINKEDINATOR", "rand")
        print(ascii_header)
        print("\t\t\tNeed a job\n")

class   Linkedinator:
    def __init__(self):
        print_header()
        self.max_requests   = 90
        self.tags           = input("Enter your tags : ")
        self.user           = input("Enter your phone : ")
        self.password       = getpass("Enter your password : ")
        self.LOGIN_URL      = "https://www.linkedin.com/"
        self.driver_path    = f"{os.getcwd()}/drivers/chromedriver"
        self.options        = webdriver.chrome.options.Options()
        self.options.add_argument('--profile-directory=Default')
        self.options.add_argument("--disable-plugins-discovery");
        self.options.binary_location = '/Users/niguinti/goinfre/Google Chrome.app/Contents/MacOS/Google Chrome'
        self.options.add_argument('headless');
        self.options.add_argument('window-size=1200x900')
        self.driver         = webdriver.Chrome(executable_path=self.driver_path, chrome_options=self.options)

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except:
            return False
        return True

    def login(self):
        print("\nLet's connect\n")
        self.driver.get(self.LOGIN_URL)
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.NAME, 'session_key')))

        input_field     = self.driver.find_element_by_name('session_key')
        input_field.send_keys(self.user)
        input_field     = self.driver.find_element_by_name('session_password')
        input_field.send_keys(self.password)
        input_field.send_keys(Keys.RETURN)
        
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, 'nav-item__profile-member-photo')))
        except:
            print("[" + Fore.RED + "FAILED" + Fore.RESET + "] Connexion Failed...")
            sys.exit(1)
        if self.driver.find_element_by_class_name('nav-item__profile-member-photo') is not False :
            print("[" + Fore.GREEN + "SUCCESS" + Fore.RESET + "] Connexion succeed !")
            self.tags = 'https://www.linkedin.com/search/results/people/?keywords='+ self.tags +'&origin=FACETED_SEARCH&page='
            i = 1
            requests_count = 0
            
            self.driver.get(self.tags + str(i))
            while self.check_exists_by_xpath("//div[@class='search-no-results__container']") is False :
                # Get all profiles
                profiles = self.driver.find_elements_by_class_name('search-result__occluded-item')
                for profile in profiles:
                    if requests_count == self.max_requests:
                        print("[" + Fore.RED + "MAX" + Fore.RESET + "] Limit of connection.")
                        sys.exit(0)
                    try :
                        connect = profile.find_element_by_class_name('search-result__action-button')
                        if connect.text[0] == 'S':
                            name        = profile.find_element_by_class_name('actor-name').text
                            synopsis    = profile.find_element_by_class_name('subline-level-1').text
                            img         = profile.find_element_by_class_name('ivm-view-attr__img--centered').get_attribute('src')
                            py_imgcat.imgcat(requests.get(img).content)
                            answer      = input("[" + Fore.YELLOW + "?" + Fore.RESET + "] " + name + " | " + synopsis + " ? y/N : ").strip('\n\t\r ')
                            if answer is 'y' :
                                try :
                                    connect.click()
                                except :
                                    traceback.print_exc()
                                WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.ID, 'send-invite-modal')))
                                elem = self.driver.find_element_by_id('send-invite-modal')
                                button = self.driver.find_element_by_xpath("//div[@class='artdeco-modal__actionbar text-align-right ember-view']/button[@class='ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
                                button.click()
                                print("[" + Fore.GREEN + "+" + Fore.RESET + "] Sended !")
                                requests_count += 1
                    except :
                        pass
                i += 1
                print("[" + Fore.CYAN + "..." + Fore.RESET + "] Loading page " + str(i) + "...")
                self.driver.get(self.tags + str(i))
            print("[" + Fore.RED + "X" + Fore.RESET + "] No more result !")
            sys.exit(1)
        else:
            print("[" + Fore.RED + "FAILED" + Fore.RESET + "] Connexion error.")

    def _close(self):
        self.driver.close()

def     linkedinator_launch():
    instance = Linkedinator()
    instance.login()
    instance.destroy()

if __name__ == '__main__':
    linkedinator_launch()
