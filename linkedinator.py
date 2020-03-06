#!/usr/bin/env python
import sys
import os 
import time
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from colorama import Fore
from art import *
import base64

def print_header():
        ascii_header = text2art("LINKEDINATOR", "rand")
        print(ascii_header)
        print("\t\t\tNeed a job\n")

class   Linkedinator:
    def __init__(self):
        print_header()
        self.max_requests = 3
        self.tags           = input("Enter your tags : ")
        #self.user           = input("Enter your username : ")
        self.user           = '+33768228651'
        #self.password       = getpass("Enter your password : ")
        self.password       = 'P4ssword1024'
        self.LOGIN_URL      = "https://www.linkedin.com/"
        self.driver_path    = f"{os.getcwd()}/drivers/chromedriver"
        self.options        = webdriver.chrome.options.Options()
        self.options.add_argument('--profile-directory=Default')
        self.options.add_argument("--disable-plugins-discovery");
        self.options.binary_location = '/Users/niguinti/goinfre/Google Chrome.app/Contents/MacOS/Google Chrome'
        #self.options.add_argument('headless');
        self.driver         = webdriver.Chrome(executable_path=self.driver_path, chrome_options=self.options)

    def catch_results(self):
        try:
            self.driver.find_element_by_class_name('search-no-results')
            print("[" + Fore.RED + "X" + Fore.RESET + "] No more result !\n")
            sys.exit(1)
        except:
            return False

    def login(self):
        print("\nLet's connect\n")
        self.driver.get(self.LOGIN_URL)
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.NAME, 'session_key')))
        input_field     = self.driver.find_element_by_name('session_key')
        input_field.send_keys(self.user)
        input_field     = self.driver.find_element_by_name('session_password')
        input_field.send_keys(self.password)
        input_field.send_keys(Keys.RETURN)
        if self.driver.find_element_by_class_name('nav-item__profile-member-photo') is not False :
            print("[" + Fore.GREEN + "SUCCESS" + Fore.RESET + "] Connexion succeed !\n")
            self.tags = 'https://www.linkedin.com/search/results/people/?keywords='+ self.tags +'&origin=SWITCH_SEARCH_VERTICAL&page='
            i = 1
            requests_count = 0
            while self.catch_results() is False :
                self.driver.get(self.tags + str(i))
                self.driver.get_screenshot_as_file('main-page.png')
                connects = self.driver.find_elements_by_class_name('search-result__action-button')
                for profile in connects :
                    if requests_count < self.max_requests :
                        profile.click()
                        time.sleep(1)
                        elem = self.driver.find_element_by_id('send-invite-modal')
                        self.driver.get_screenshot_as_file('clic1.png')
                        if elem.is_displayed():
                            button = self.driver.find_element_by_xpath("//div[@class='artdeco-modal__actionbar text-align-right ember-view']/button[@class='ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
                            button.click()
                            print("[" + Fore.GREEN + "+" + Fore.RESET + "] Sended]!\n")
                            self.driver.get_screenshot_as_file('clic2.png')
                            requests_count += 1
                    else:
                        print("[" + Fore.RED + "MAX" + Fore.RESET + "] Limit of connection.\n")
                        sys.exit(0)
                i += 1

        else:
            print("[" + Fore.RED + "FAILED" + Fore.RESET + "] Connexion error.\n")

        self.driver.close()

    def start(self):
        page = 1
        response = make_request(domain+page, False)
        while response is not None and response.status_code == 200 and no_bad_keyword:
            print("[" + Fore.GREEN + "✓" + Fore.RESET + "]\t[%s/%s] succeed" % (domain, test))

    def _close(self):
        self.driver.close()

def     linkedinator_launch():
    instance = Linkedinator()
    instance.login()
    #instance.start()
    #instance.destroy()

if __name__ == '__main__':
    linkedinator_launch()
