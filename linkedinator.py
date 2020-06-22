#!/usr/bin/env python3
import sys
import platform
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

op_sys = platform.system()
binary_suffix = ''
if op_sys == "Windows" :
    binary_suffix = '.exe'
warnings.filterwarnings('ignore')

# Colorize input `message` with `color`
def colorize(color, message):
        return color + message + Fore.RESET

# Prettify a message with a prefix: [`color``prefix``color_end`] `message`
def pretty_message(color, prefix, message):
        return "[" + colorize(color, prefix)  + "] " + message

# Pretty print a message with a prefix: [`color``prefix``color_end`] `message`
def print_pretty(color, prefix, message):
        print(pretty_message(color, prefix, message))

def print_header():
        ascii_header = text2art("LINKEDINATOR", "rand")
        print(colorize(Fore.RED, ascii_header))
        print(colorize(Fore.CYAN, "\t\t\tNeed a job\n"))

class   Linkedinator:
    def __init__(self):
        self.driver_path    = f"{os.getcwd()}/drivers/"
        self.LOGIN_URL      = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"

        parser              = argparse.ArgumentParser()
        parser.add_argument("-d", "--driver", help="Set the driver to use.", type=str, choices=["firefox", "chrome"], required=True)
        parser.add_argument("-g", "--gender", help="Get profile by gender. 1 = Woman, 2 = Man", type=int, choices=[1, 2])
        parser.add_argument("-r", "--range", help="Set \"mutual connection\" search argument. 4 = All, Default = Don't care", type=int, choices=[1, 2, 3, 4])
        parser.add_argument("-m", "--max", help="Set maximum connections requests.\tDefault = 50", type=int, default=50)
        parser.add_argument("-l", "--location", help="Set the browser binary location", type=str)
        parser.add_argument("-L", "--live", help="Run the bot in live mod", action="store_true")
        parser.add_argument("-P", "--premium", help="Connect only with Premium", action="store_true")
        parser.add_argument("--debug", help="Set debug flag", action="store_true")
        parser.add_argument("--auto", help="Connect automatically with everyone.", action="store_true")
        self.args = parser.parse_args()
        if "firefox" in self.args.driver :
            self.options        = webdriver.firefox.options.Options()
        elif "chrome" in self.args.driver:
            self.options        = webdriver.chrome.options.Options()
        self.options.add_argument('--profile-directory=Default')
        self.options.add_argument("--disable-plugins-discovery");
        self.options.add_argument('window-size=1200x900')
        if self.args.location:
            self.options.binary_location = self.args.location
        if "firefox" in self.args.driver :
            if not self.args.live:
                self.options.headless = True;
            self.driver = webdriver.Firefox(executable_path=self.driver_path+"geckodriver" + binary_suffix, options=self.options)
        elif "chrome" in self.args.driver:
            if not self.args.live:
                self.options.add_argument('headless');
            self.driver = webdriver.Chrome(executable_path=self.driver_path+"chromedriver" + binary_suffix, chrome_options=self.options)
        print_header()
        self.tags           = input("Enter your tags : ")
        self.user           = getpass("Enter your phone : ")
        self.password       = getpass("Enter your password : ")

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
            WebDriverWait(self.driver, 7).until(EC.visibility_of_element_located((By.CLASS_NAME, 'nav-item__profile-member-photo')))
        except Exception as e :
            if self.args.debug :
                print(e);
                traceback.print_exc()
            print_pretty(Fore.RED, "FAILED", "Connexion Failed...")
            sys.exit(1)
        if self.driver.find_element_by_class_name('nav-item__profile-member-photo') is not False :
            print_pretty(Fore.GREEN, "SUCCESS", "Connexion succeed !")
            self.driver.get(self.tags + str(i))
            while self.check_exists_by_xpath("//div[@class='search-no-results__container']") is False :
                # Get all profiles
                time.sleep(1);
                try :
                    self.driver.find_element_by_class_name("search-paywall__limit")
                    print_pretty(Fore.YELLOW, "REACH_MAX_SEARCH", "Limit of search reached.")
                except :
                    pass
                profiles = self.driver.find_elements_by_class_name('search-result__occluded-item')
                for profile in profiles:
                    if requests_count >= self.args.max:
                        print_pretty(Fore.RED, "MAX", "Limit of connection.")
                        sys.exit(0)
                    try :
                        connect = profile.find_element_by_class_name('search-result__action-button')
                        if connect.text[0] == 'S':
                            try :
                                premium = profile.find_element_by_class_name('premium-icon')
                                premium = "[" + Fore.CYAN + "Premium User"+ Fore.RESET + "]\n"
                            except :
                                premium = "Not premium\n"
                                pass
                            if self.args.premium and premium == "Not premium\n" :
                                continue
                            name        = profile.find_element_by_class_name('actor-name').text
                            synopsis    = profile.find_element_by_class_name('subline-level-1').text
                            try :
                                img     = profile.find_element_by_class_name('ivm-view-attr__img--centered').get_attribute('src')
                            except :
                                img = 'https://cdn.intra.42.fr/users/small_default.png'
                            g = gender.Detector()
                            g = g.get_gender(name.split(' ')[0])
                            gender_condition = 0
                            if not self.args.gender :
                                gender_condition = 1
                            elif self.args.gender == 1 and "female" in g :
                                gender_condition = 1
                            elif self.args.gender == 2 and "female" not in g :
                                gender_condition = 1
                            if not self.args.auto and gender_condition == 1 :
                                try:
                                    py_imgcat.imgcat(requests.get(img).content)
                                except :
                                    print_pretty(Fore.MAGENTA, ":/", "Can't display image in terminal, please check Readme.")
                                answer = input(premium + "[" + Fore.YELLOW + "?" + Fore.RESET + "] " + name + " | " + synopsis + " ? y/N : ").strip('\n\t\r ')
                            if answer == 'y' and gender_condition == 1 :
                                try :
                                    connect.click()
                                except Exception as e :
                                    if self.args.debug :
                                        traceback.print_exc()
                                        print(e);
                                    continue
                                WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.ID, 'send-invite-modal')))
                                elem = self.driver.find_element_by_id('send-invite-modal')
                                button = self.driver.find_element_by_xpath("//div[@class='artdeco-modal__actionbar text-align-right ember-view']/button[@class='ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
                                button.click()
                                requests_count += 1
                                if self.args.auto :
                                    try :
                                        py_imgcat.imgcat(requests.get(img).content)
                                    except :
                                        pass
                                    print(premium + "[" + Fore.GREEN + "+" + Fore.RESET + "] " + name + "\n" + synopsis + '\n').strip('\n\t\r ')
                                else :
                                    print_pretty(Fore.GREEN, "+", "Sended !")
                    except Exception as e:
                        if self.args.debug :
                            print(e)
                            traceback.print_exc()
                        pass
                i += 1
                print_pretty(Fore.CYAN, "...", "Loading page" + str(i) + "...")
                self.driver.get(self.tags + str(i))
            print_pretty(Fore.RED, "X", "No more result !")
            sys.exit(1)
        else:
            print_pretty(Fore.RED, "FAILED", "Connexion error.")

    def _close(self):
        self.driver.close()

def     linkedinator_launch():
    instance = Linkedinator()
    instance.login()
    instance.destroy()

if __name__ == '__main__':
    linkedinator_launch()
