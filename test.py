#!/usr/bin/env python3
import sys
import platform
import os
import time
import requests
import py_imgcat
import gender_guesser.detector as gender
import argparse
import cmd
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from colorama import Fore
from art import *
import urllib.parse
import warnings
import traceback

op_sys = platform.system()
binary_suffix = ''
if op_sys == "Windows" :
    binary_suffix = '.exe'
warnings.filterwarnings('ignore')

# Overriding of ArgumentParser function to avoid exit when parsing failed
class ArgumentParser(argparse.ArgumentParser):
    def _get_action_from_name(self, name):
        """Given a name, get the Action instance registered with this parser.
        If only it were made available in the ArgumentError object. It is 
        passed as it's first arg...
        """
        container = self._actions
        if name is None:
            return None
        for action in container:
            if '/'.join(action.option_strings) == name:
                return action
            elif action.metavar == name:
                return action
            elif action.dest == name:
                return action

    def error(self, message):
        exc = sys.exc_info()[1]
        if exc:
            exc.argument = self._get_action_from_name(exc.argument_name)
            raise exc
        super(ArgumentParser, self).error(message)

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

range_list = ['', '"F"', '"S"', '"O"', '"O"%2C"F"%2C"S"']

# Format url
def format_url(range, tags, url):
    if url:
        return urllib.parse.unquote(self.args.url).replace('\\', '') + '&page='
    elif range and range >= 1 and range <= 4:
        tags = 'https://www.linkedin.com/search/results/people/?facetNetwork=["'+range_list[range]+'"]&keywords='+ tags +'&origin=FACETED_SEARCH&page='
    return 'https://www.linkedin.com/search/results/people/?keywords='+ tags +'&origin=FACETED_SEARCH&page='

class Linkedinator(cmd.Cmd):
    """Simple command processor example."""
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.driver_path    = f"{os.getcwd()}/drivers/"
        self.connected      = 0
        self.prompt         = '$> '

        parser              = argparse.ArgumentParser()
        parser.add_argument("-d", "--driver", help="Set the driver to use.", type=str, choices=["firefox", "chrome"], required=True)
        parser.add_argument("-l", "--location", help="Set the browser binary location", type=str)
        parser.add_argument("-L", "--live", help="Run the bot in live mod", action="store_true")
        parser.add_argument("--debug", help="Set debug flag", action="store_true")
        try:
           self.args = parser.parse_args()
        except argparse.ArgumentError as exc:
            print(exc.message, '\n', exc.argument)
            return False

        print_pretty(Fore.YELLOW, "...", "Setting up selenium")
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
        print_pretty(Fore.CYAN, "O", "Success")

    def element_exist_by_class(self, element):
        try :
            self.driver.find_element_by_class_name(element)
            return True
        except :
            return False

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except:
            return False
        return True

    def do_connect(self, args):
        """Connect to your Linkedin account"""
        self.LOGIN_URL      = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"

        self.user           = getpass("Enter your phone number: ")
        self.password       = getpass("Enter your password : ")

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
        if self.driver.find_element_by_class_name('nav-item__profile-member-photo') is not False :
            print_pretty(Fore.GREEN, "SUCCESS", "Connexion succeed !")
            self.connected = 1
            self.prompt = Fore.GREEN+'Connected'+Fore.RESET+'> '

    def do_people_connect(self, arguments):
        if self.connected == 0:
            print_pretty(Fore.RED, "Error", "No active connection. Please, use `connect` command.")
            return
        
        parser = argparse.ArgumentParser(prog='people_connect')
        parser.add_argument("-g", "--gender", help="Get profile by gender. 1 = Woman, 2 = Man", type=int, choices=[1, 2])
        parser.add_argument("-r", "--range", help="Set \"mutual connection\" search argument. 4 = All, Default = Don't care", type=int, choices=[1, 2, 3, 4])
        parser.add_argument("-m", "--max", help="Set maximum connections requests.\tDefault = 50", type=int, default=50)
        parser.add_argument("-P", "--premium", help="Connect only with Premium", action="store_true")
        parser.add_argument("-u", "--url", help="Use custom search URL request.", type=str)
        parser.add_argument("--auto", help="Connect automatically with everyone.", action="store_true")
        try:
            args = parser.parse_args(arguments.split())
        except argparse.ArgumentError as exc:
            print(exc.message, '\n', exc.argument)
            return

        if not args.url :
            tags = input("Enter your tags : ")
        else :
            print_pretty(Fore.CYAN, "!", "Custom search request used. -u/--url")
        
        search_url = format_url(args.range, tags, args.url)

        while self.check_exists_by_xpath("//div[@class='search-no-results__container']") is False :
            # Get all profiles
            time.sleep(1);
            if element_exist_by_class("search-paywall__limit") == True:
                print_pretty(Fore.YELLOW, "REACH_MAX_SEARCH", "Limit of search reached.")
                pass
            profiles = self.driver.find_elements_by_class_name('search-result__occluded-item')
            for profile in profiles:
                if requests_count >= args.max:
                    print_pretty(Fore.RED, "MAX", "Limit of connection.")
                    return
                try :
                    connect = profile.find_element_by_class_name('search-result__action-button')
                    if connect.text[0] == 'S':
                        try :
                            premium = profile.find_element_by_class_name('premium-icon')
                            premium = "[" + Fore.CYAN + "Premium User"+ Fore.RESET + "]\n"
                        except :
                            premium = "Not premium\n"
                            pass
                        if args.premium and premium == "Not premium\n" :
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
                        if not args.gender :
                            gender_condition = 1
                        elif args.gender == 1 and "female" in g :
                            gender_condition = 1
                        elif args.gender == 2 and "female" not in g :
                            gender_condition = 1
                        if not args.auto and gender_condition == 1 :
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
                            if args.auto :
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
            self.driver.get(tags + str(i))
        print_pretty(Fore.RED, "X", "No more result !")

    def help_people_connect(self):
        #"--gender", help="Get profile by gender. 1 = Woman, 2 = Man", type=int, choices=[1, 2]
        #"--premium", help="Connect only with Premium", action="store_true"
        #"--range", help="Set \"mutual connection\" search argument. 4 = All, Default = Don't care", type=int, choices=[1, 2, 3, 4]
        #"--max", help="Set maximum connections requests.\tDefault = 50", type=int, default=50
        #"--url", help="Use custom search URL request.", type=str
        #"--auto", help="Connect automatically with everyone.", action="store_true")

        print('\n'.join([
            'people_connect [auto=False] [max=100] [premium_only=False] [range=0...4] [url=None]',
            'auto           = Add everyone automatically',
            'max            = Limit of connections',
            'premium_only   = Select premium people only',
            'range          = Network relation setting (4 = 1st & 2nd & 3nd degree)',
            'url            = Set custom search url'
        ]))
    
    def do_companies(self):
        if self.connected == 0:
            print_pretty(Fore.RED, "Error", "No active connection. Please, use `connect` command.")
            return
        return
    
    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print

if __name__ == '__main__':
    instance = Linkedinator()
    instance.cmdloop()
