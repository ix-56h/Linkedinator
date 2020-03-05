#!/usr/bin/env python
import sys
import requests
from colorama import Fore
from art import *
""" https://www.linkedin.com/search/results/people/?keywords=test&origin=FACETED_SEARCH&page=1 """
""" not found keyword : search-no-results__container """
""" else work click on all button with class : search-result__action-button """

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

    def login(self):
        print("\nLet's connect\n")

    def start(self):
        page = 1
        response = make_request(domain+page, False)
        while response is not None and response.status_code == 200 and no_bad_keyword:
            print("[" + Fore.GREEN + "✓" + Fore.RESET + "]\t[%s/%s] succeed" % (domain, test))

def     linkedinator_launch():
    instance = Linkedinator()
    instance.login()
    instance.start()

if __name__ == '__main__':
    linkedinator_launch()
