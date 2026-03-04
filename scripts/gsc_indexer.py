import os
import sys
import json
import time
import argparse
import requests
from lxml import etree
import undetected_chromedriver as uc
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime

# --- Configuration ---
DAILY_LIMIT = 8
INDEXED_URLS_FILE = os.path.join(os.path.dirname(__file__), 'indexed_urls.json')
USER_DATA_DIR = os.path.join(os.path.dirname(__file__), 'chrome_profile')

class GSCIndexer:
    def __init__(self, site_url, dry_run=False):
        self.site_url = site_url.rstrip('/')
        self.sitemap_url = f"{self.site_url}/sitemap.xml"
        self.dry_run = dry_run
        self.indexed_data = self._load_indexed_data()
        self.driver = None

    def _load_indexed_data(self):
        if os.path.exists(INDEXED_URLS_FILE):
            try:
                with open(INDEXED_URLS_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_indexed_data(self):
        with open(INDEXED_URLS_FILE, 'w') as f:
            json.dump(self.indexed_data, f, indent=4)

    def fetch_sitemap_urls(self):
        print(f"Fetching sitemap: {self.sitemap_url}")
        try:
            # Disable SSL verification for sitemap fetch as it's often problematic on local environments
            response = requests.get(self.sitemap_url, verify=False)
            response.raise_for_status()
            root = etree.fromstring(response.content)
            # Handle potential namespaces in sitemap
            ns = {'ns': root.nsmap[None]} if None in root.nsmap else {}
            
            urls = []
            # Check for sitemap index or simple sitemap
            if 'sitemapindex' in root.tag:
                locs = root.xpath('//ns:loc', namespaces=ns)
                for loc in locs:
                    urls.extend(self._fetch_urls_from_sub_sitemap(loc.text, ns))
            else:
                locs = root.xpath('//ns:loc', namespaces=ns)
                urls = [loc.text for loc in locs]
            
            print(f"Discovered {len(urls)} URLs from sitemap.")
            return urls
        except Exception as e:
            print(f"Error fetching sitemap: {e}")
            return []

    def _fetch_urls_from_sub_sitemap(self, url, ns):
        try:
            response = requests.get(url)
            root = etree.fromstring(response.content)
            locs = root.xpath('//ns:loc', namespaces=ns)
            return [loc.text for loc in locs]
        except Exception:
            return []

    def setup_driver(self):
        print("Initializing undetected chromedriver...")
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
        # options.add_argument("--profile-directory=Default") # Can be customized
        
        self.driver = uc.Chrome(options=options)
        self.driver.maximize_window()

    def login_and_select_property(self):
        print("Navigating to GSC...")
        self.driver.get("https://search.google.com/search-console")
        
        # Wait for login if needed
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Search Console')]"))
            )
        except TimeoutException:
            print("Login might be required. Please login manually if the browser is waiting.")
            # We give more time for manual login if it's the first time
            WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Search Console')]"))
            )

        print("GSC Loaded.")
        # Select property
        # GSC usually has a property picker on the top left
        try:
            # Click property picker
            picker = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label^='Select property']"))
            )
            picker.click()
            time.sleep(2)
            
            # Find the property that matches site_url
            # Often it's listed exactly as the URL
            properties = self.driver.find_elements(By.XPATH, f"//div[@role='option']//span[contains(text(), '{self.site_url}')]")
            if properties:
                properties[0].click()
                print(f"Selected property: {self.site_url}")
            else:
                print(f"Property {self.site_url} not found in picker list. Trying to find by partial match.")
                # Try sibling match or something more robust if needed
                # For now, let's assume it's there.
        except Exception as e:
            print(f"Warning: Could not select property via picker: {e}")
            print("Trying direct navigation to land on the property...")
            # Direct URL often works too: https://search.google.com/search-console/index?resource_id=https://example.com/
            encoded_url = requests.utils.quote(self.site_url + "/", safe='')
            self.driver.get(f"https://search.google.com/search-console/index?resource_id={encoded_url}")
            time.sleep(5)

    def inspect_and_index(self, url):
        print(f"\nInspecting URL: {url}")
        
        # Input URL into inspection bar
        # Usually it's a search input on top
        try:
            # Find the search input
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder^='Inspect any URL']"))
            )
            search_box.clear()
            search_box.send_keys(url)
            search_box.send_keys(u'\ue007') # Enter key
            
            print("Waiting for inspection results...")
            # Wait for results to load (can take a while)
            # Look for "URL is on Google" or "URL is not on Google"
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'URL is on Google') or contains(text(), 'URL is not on Google')]"))
            )
            
            page_source = self.driver.page_source
            if "URL is on Google" in page_source:
                print(f"SUCCESS: {url} is already indexed.")
                self.indexed_data[url] = {"status": "indexed", "date": datetime.now().isoformat()}
                return False # Not indexed today
            else:
                print(f"URL NOT indexed. Requesting indexing...")
                if self.dry_run:
                    print("[Dry Run] Would click 'Request Indexing'")
                    return True
                
                # Click "Request Indexing"
                request_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button']//span[contains(text(), 'Request Indexing')]"))
                )
                request_button.click()
                
                print("Retrieving indexing request status (waiting up to 2 mins)...")
                # Wait for "Indexing requested" confirmation
                try:
                    WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Indexing requested')]"))
                    )
                    print("Index request successful.")
                    # Dismiss the dialog
                    got_it = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Got it')]")
                    got_it.click()
                    
                    self.indexed_data[url] = {"status": "requested", "date": datetime.now().isoformat()}
                    return True # Count as 1 indexed today
                except TimeoutException:
                    print("TIMEOUT or CAPTCHA: Indexing request confirmation did not appear.")
                    # Check for captcha
                    if "captcha" in self.driver.page_source.lower():
                        print("CAPTCHA detected! Please solve it manually.")
                    return False
                
        except Exception as e:
            print(f"Error during inspection for {url}: {e}")
            return False

    def run(self):
        urls = self.fetch_sitemap_urls()
        if not urls:
            return

        # Filter out already indexed/requested URLs (optional, but good for efficiency)
        # However, "requested" should probably be checked again after some time.
        # Let's focused on those that are UNKNOWN or marked NOT INDEXED recently.
        
        candidates = []
        for url in urls:
            if url not in self.indexed_data or self.indexed_data[url].get('status') != 'indexed':
                candidates.append(url)
        
        print(f"Found {len(candidates)} potential non-indexed URLs.")
        
        if not candidates:
            print("All URLs seem to be indexed already.")
            return

        self.setup_driver()
        try:
            self.login_and_select_property()
            
            count = 0
            for url in candidates:
                if count >= DAILY_LIMIT:
                    print(f"\nDaily limit of {DAILY_LIMIT} reached. Stopping.")
                    break
                
                if self.inspect_and_index(url):
                    count += 1
                    self._save_indexed_data()
                    # Sleep to be polite to GSC
                    time.sleep(10)
                
            print(f"\nExecution finished. Processed {count} indexing requests.")
        finally:
            if self.driver:
                print("Closing browser...")
                self.driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GSC URL Indexing Automation")
    parser.add_argument("--site-url", required=True, help="Site URL (e.g., https://example.com)")
    parser.add_argument("--dry-run", action="store_true", help="Don't actualy click request indexing")
    args = parser.parse_args()

    indexer = GSCIndexer(args.site_url, args.dry_run)
    indexer.run()
