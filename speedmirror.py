#!/bin/python3

import os
import requests
from pythonping import ping
import bs4 as BeautifulSoup

def contains_readme(url):
    if url.endswith("/README"):
        return True
    else:
        return False

# Check if user is root
def check_root():
    if os.geteuid() != 0:
        print("You must be root to run this script.")
        exit(1)

# Ping url and return avg ping
def ping_url(url):
    print(f'Pinging: {url}')
    return ping(url).rtt_avg_ms

def ping_all_urls(domains):
    return list(map(ping_url, domains))

def create_source_list(link, https=False):
    if https:
        https_link = f'deb {link} kali-rolling main contrib non-free'
        with open('sources.list', 'w') as f:
            f.write(https_link)
    else:
        link = link.replace('https://', 'http://')
        http_link = f'deb {link} kali-rolling main contrib non-free'
        with open('sources.list', 'w') as f:
            f.write(http_link)
    print(f'Created sources.list file with {link}')

# Get all links from a url
def find_links(url):
    response = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(response.text, "html.parser")
    links = list(map(lambda x: x.get("href"), soup.find_all("a"))) # Get all links
    readme_links = list(filter(contains_readme, links)) # Filter out all links that don't contain "README"
    final_links = list(map(lambda x: x.replace('/README', ''), readme_links)) # remove /README from the end of the link
    return list(set(final_links)) # Remove duplicates

# Get domains from links
def get_domains(links):
    return list(map(lambda x: x.split('/')[2], links))

def get_fastest_mirror(domains):
    pings = ping_all_urls(domains)
    return pings.index(min(pings)), domains[pings.index(min(pings))], min(pings)

if __name__ == "__main__":

    url = "https://http.kali.org/README.mirrorlist"

    # Check if the user is root
    check_root()

    links = find_links(url)
    domains = get_domains(links)
    best_mirror = get_fastest_mirror(domains)
    best_mirror_link = links[best_mirror[0]]

    create_source_list(best_mirror_link, https=True)

    print('--------------------------------')
    print(best_mirror)
    print(f'index: {best_mirror[0]}')
    print(f'domain: {best_mirror[1]}')
    print(f'link: {best_mirror_link}')
    print(f'avg speed: {best_mirror[2]}ms')