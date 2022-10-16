#!/bin/python3

import os
import requests
from pythonping import ping
import bs4 as BeautifulSoup

response = requests.get("https://http.kali.org/README.mirrorlist")
soup = BeautifulSoup.BeautifulSoup(response.text, "html.parser")

def contains_readme(url):
    if url.endswith("/README"):
        return True
    else:
        return False

def check_root():
    if os.geteuid() != 0:
        return False
    else:
        return True

# Ping url and return avg ping
def ping_url(url):
    print(f'Pinging: {url}')
    return ping(url, verbose=True).rtt_avg_ms

def modify_source_list():
    pass

if __name__ == "__main__":

    # Check if the user is root
    if not check_root():
        print("You must be root to run this script.")
        exit(1)

    links = list(map(lambda x: x.get("href"), soup.find_all("a"))) # Get all links
    readme_links = list(filter(contains_readme, links)) # Filter out all links that don't contain "README"
    final_links = list(map(lambda x: x.replace('/README', ''), readme_links)) # remove /README from the end of the link
    final_links = list(set(final_links)) # Remove duplicates
    domains = list(map(lambda x: x.split("/")[2], final_links)) # Get the domain name from the link
    print(ping_url(domains[0]))