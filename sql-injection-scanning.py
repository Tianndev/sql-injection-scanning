import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, Timeout, HTTPError
from colorama import Fore, Style
import subprocess

def get_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return [link.get('href') for link in soup.find_all('a') if link.get('href') and link.get('href').startswith('http')]
    except (ConnectionError, Timeout, HTTPError) as e:
        print(f"{Fore.RED}Error accessing {url}: {e}{Style.RESET_ALL}")
        return []

def create_sitemap(url, depth, sitemap=None, visited=None):
    if not sitemap:
        sitemap = {}
    if not visited:
        visited = set()

    if depth == 0 or url in visited:
        return sitemap

    visited.add(url)
    print(f"Processing {Fore.GREEN}{url}, Depth: {depth}{Style.RESET_ALL}")
    links = get_links(url)
    sitemap[url] = links

    for link in links:
        if link not in sitemap:
            sitemap = create_sitemap(link, depth-1, sitemap, visited)
    return sitemap

def sql_injection_scan(url):
    try:
        subprocess.run(['sqlmap', '--batch', '--tamper', 'randomcomments', '--random-agent', '--level', '3', '--risk', '2', '--url', url], check=True)
        print(f"{Fore.GREEN}SQL injection scan completed for {url}.{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error while performing SQL injection scan for {url}: {e}{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}sqlmap not found. Please install sqlmap and ensure it is in your PATH.{Style.RESET_ALL}")

def ssl_scan(url):
    try:
        subprocess.run(['sslscan', url], check=True)
        print(f"{Fore.GREEN}SSL/TLS scan completed for {url}.{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error while performing SSL/TLS scan for {url}: {e}{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}sslscan not found. Please install sslscan and ensure it is in your PATH.{Style.RESET_ALL}")

if __name__ == "__main__":
    url = input("Masukan URL Website: ")
    # DEVELOPED BY: TIANN DEV
    depth = 2
    print("Creating site map...")
    sitemap = create_sitemap(url, depth)
    
    print("\nSecurity scan in progress (SQL injection)...")
    for page_url, links in sitemap.items():
        for link in links:
            print(f"\nSecurity scan for {link} in progress...")
            sql_injection_scan(link)
    
    print("\nSecurity scan in progress (SSL/TLS)...")
    for page_url, links in sitemap.items():
        for link in links:
            print(f"\nSecurity scan for {link} in progress...")
            ssl_scan(link)
