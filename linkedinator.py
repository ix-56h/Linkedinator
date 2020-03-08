#!/usr/bin/env python
import sys
import os 
import time
import requests
import py_imgcat
import gender_guesser.detector as gender
import argparse
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
        self.driver_path    = f"{os.getcwd()}/drivers/chromedriver"
        self.LOGIN_URL      = "https://www.linkedin.com/"
        
        parser = argparse.ArgumentParser()
        parser.add_argument("-g", "--gender", help="Get profile by gender. 1 = girl, 2 = male", type=int, choices=[1, 2])
        parser.add_argument("-r", "--range", help="Set \"mutual connection\" search argument. 4 = All, Default = Don't care", type=int, choices=[1, 2, 3, 4])
        parser.add_argument("-m", "--max", help="Set maximum connections requests.\tDefault = 50", type=int, default=50)
        parser.add_argument("-l", "--location", help="Set the chrome binary location", type=str)
        parser.add_argument("-L", "--live", help="Run the bot in live mod", action="store_true")
        parser.add_argument("--auto", help="Connect automatically with everyone.", action="store_true")
        self.args = parser.parse_args()
        
        self.options        = webdriver.chrome.options.Options()
        self.options.add_argument('--profile-directory=Default')
        self.options.add_argument("--disable-plugins-discovery");
        self.options.add_argument('window-size=1200x900')
        if self.args.location:
            self.options.binary_location = self.args.location
        if not self.args.live:
            self.options.add_argument('headless');
        
        print_header()
        self.tags           = input("Enter your tags : ")
        self.user           = input("Enter your phone : ")
        self.password       = getpass("Enter your password : ")

        self.driver         = webdriver.Chrome(executable_path=self.driver_path, chrome_options=self.options)

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except:
            return False
        return True

    def login(self):
        i               = 1
        requests_count  = 0
        answer          = 'y'
        if self.args.range == 1:
            self.tags       = 'https://www.linkedin.com/search/results/people/?facetNetwork=["F"]&keywords='+ self.tags +'&origin=FACETED_SEARCH&page='
        elif self.args.range == 2:
            self.tags       = 'https://www.linkedin.com/search/results/people/?facetNetwork=["S"]&keywords='+ self.tags +'&origin=FACETED_SEARCH&page='
        elif self.args.range == 3:
            self.tags       = 'https://www.linkedin.com/search/results/people/?facetNetwork=["O"]&keywords='+ self.tags +'&origin=FACETED_SEARCH&page='
        elif self.args.range == 4:
            self.tags       = 'https://www.linkedin.com/search/results/people/?facetNetwork=["O"%2C"F"%2C"S"]&keywords='+ self.tags +'&origin=FACETED_SEARCH&page='
        else :
            self.tags       = 'https://www.linkedin.com/search/results/people/?keywords='+ self.tags +'&origin=FACETED_SEARCH&page='
        
        print("\nLet's connect\n")
        
        self.driver.get(self.LOGIN_URL)
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.NAME, 'session_key')))

        input_field     = self.driver.find_element_by_name('session_key')
        input_field.send_keys(self.user)
        input_field     = self.driver.find_element_by_name('session_password')
        input_field.send_keys(self.password)
        input_field.send_keys(Keys.RETURN)
        
        try:
            WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.CLASS_NAME, 'nav-item__profile-member-photo')))
        except:
            print("[" + Fore.RED + "FAILED" + Fore.RESET + "] Connexion Failed...")
            sys.exit(1)
        if self.driver.find_element_by_class_name('nav-item__profile-member-photo') is not False :
            print("[" + Fore.GREEN + "SUCCESS" + Fore.RESET + "] Connexion succeed !")
            self.driver.get(self.tags + str(i))
            while self.check_exists_by_xpath("//div[@class='search-no-results__container']") is False :
                # Get all profiles
                time.sleep(1);
                profiles = self.driver.find_elements_by_class_name('search-result__occluded-item')
                for profile in profiles:
                    if requests_count == self.args.max:
                        print("[" + Fore.RED + "MAX" + Fore.RESET + "] Limit of connection.")
                        sys.exit(0)
                    try :
                        connect = profile.find_element_by_class_name('search-result__action-button')
                        if connect.text[0] == 'S':
                            name        = profile.find_element_by_class_name('actor-name').text
                            synopsis    = profile.find_element_by_class_name('subline-level-1').text
                            img         = profile.find_element_by_class_name('ivm-view-attr__img--centered').get_attribute('src')
                            g           = gender.Detector()
                            g = g.get_gender(name.split(' ')[0])
                            gender_condition = 0
                            if not self.args.gender :
                                gender_condition = 1
                            elif self.args.gender == 1 and "female" in g :
                                gender_condition = 1
                            elif self.args.gender == 2 and "female" not in g :
                                gender_condition = 1
                            if not self.args.auto and gender_condition == 1 :
                                py_imgcat.imgcat(requests.get(img).content)
                                answer = input("[" + Fore.YELLOW + "?" + Fore.RESET + "] " + name + " | " + synopsis + " ? y/N : ").strip('\n\t\r ')
                            if answer is 'y' and gender_condition == 1 :
                                try :
                                    connect.click()
                                except :
                                    traceback.print_exc()
                                WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.ID, 'send-invite-modal')))
                                elem = self.driver.find_element_by_id('send-invite-modal')
                                button = self.driver.find_element_by_xpath("//div[@class='artdeco-modal__actionbar text-align-right ember-view']/button[@class='ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
                                button.click()
                                if self.args.auto :
                                    py_imgcat.imgcat(requests.get(img).content)
                                else :
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
