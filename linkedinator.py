#!/usr/bin/env python
import sys
import requests
from colorama import Fore
from art import *
""" https://www.linkedin.com/search/results/people/?keywords=test&origin=FACETED_SEARCH&page=1 """
""" not found keyword : search-no-results__container """
""" else work click on all button with class : search-result__action-button """


import os 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def print_header():
        ascii_header = text2art("LINKEDINATOR", "rand")
        print(ascii_header)
        print("\t\t\tNeed a job\n")

def make_request(domain, redirect):
    try:
        response = requests.get("https://"+domain, allow_redirects=redirect, verify=False, timeout=5)
        if not response:
            response = requests.get("http://"+domain, allow_redirects=redirect, verify=False, timeout=5)
        return response
    except:
        return None 

class   Linkedinator:
    def __init__(self):
        print_header()
        tags = input("Enter your tags :")
        self.LOGIN_URL      = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
        self.driver_path    = f"{os.getcwd()}/drivers/geckodriver"
        self.driver = webdriver.Firefox(executable_path=self.driver_path)

    def login(self):
        print("\nLet's connect\n")
        self.driver.get(self.BASE_URL)
        input_field = self.driver.find_element_by_xpath('//*[@id="id"]')
        input_field.send_keys(self.domain)
        input_field.send_keys(Keys.RETURN)
        time.sleep(3)

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
    instance.start()
    instance.destroy()

if __name__ == '__main__':
    linkedinator_launch()
