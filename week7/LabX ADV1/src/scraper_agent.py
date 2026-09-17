# agentic-web-scraper/src/scraper_agent.py
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException,
StaleElementReferenceException
import logging
from .driver_manager import DriverManager

from .data_models import Product
from .utils import wait_for_element, robust_click, save_data_to_json, scroll_to_bottom
# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class ScraperAgent:
"""
An agentic web scraper that operates based on a provided configuration.
It can navigate, extract data, and handle pagination.
"""
def __init__(self, config, browser='chrome', headless=True):
self.config = config
self.driver_manager = DriverManager(browser_name=browser, headless=headless)
self.driver = None
self.scraped_products = []
self.max_pages = config.get("max_pages", 5) # Default to scrape max 5 pages
logging.info(f"Scraper Agent initialized with config for {config['start_url']}")
def _get_element_text(self, parent_element, selector, selector_type=By.CSS_SELECTOR):
"""Helper to safely get text from an element."""
try:
element = parent_element.find_element(selector_type, selector)
return element.text.strip()
except NoSuchElementException:
# logging.warning(f"Element not found for selector: {selector}")
return None
except StaleElementReferenceException:
# logging.warning(f"Stale element reference for selector: {selector}. Retrying might be needed.")
return None # Or handle retry logic here
def _get_element_attribute(self, parent_element, selector, attribute,
selector_type=By.CSS_SELECTOR):
"""Helper to safely get an attribute from an element."""
try:
element = parent_element.find_element(selector_type, selector)
return element.get_attribute(attribute).strip()
except NoSuchElementException:
# logging.warning(f"Element not found for selector: {selector} (attribute: {attribute})")
return None
except StaleElementReferenceException:

# logging.warning(f"Stale element reference for selector: {selector}. Retrying might be needed.")
return None
def _parse_product_data(self, item_element):
"""
Extracts product data from a single product item element based on config selectors.
"""
selectors = self.config["item_data_selectors"]
name = self._get_element_text(item_element, selectors.get("name", ""))
price = self._get_element_text(item_element, selectors.get("price", ""))
description = self._get_element_text(item_element, selectors.get("description", ""),
By.CSS_SELECTOR)
url = self._get_element_attribute(item_element, selectors.get("url", ""), "href",
By.CSS_SELECTOR)
image_url = self._get_element_attribute(item_element, selectors.get("image_url", ""), "src",
By.CSS_SELECTOR)
if name and price: # Basic validation for a valid product
return Product(name=name, price=price, description=description, url=url,
image_url=image_url)
return None
def scrape_page(self):
"""
Scrapes product items from the current page.
"""
logging.info(f"Scraping page: {self.driver.current_url}")
# Wait for product container to be present
try:
# Assumes item_container_selector finds the parent of all product items
# Or directly the items if it's a direct selector for each item.
# Using find_elements to get all items
item_elements = self.driver.find_elements(By.CSS_SELECTOR,
self.config["item_container_selector"])
# Fallback for XPath if CSS selector doesn't yield results
if not item_elements:
item_elements = self.driver.find_elements(By.XPATH,
self.config["item_container_selector"])

logging.info(f"Found {len(item_elements)} potential product items on this page.")
for item_element in item_elements:
product = self._parse_product_data(item_element)
if product:
self.scraped_products.append(product.to_dict())
# logging.debug(f"Extracted: {product.name} - {product.price}") # Use debug for verbose

output
else:
logging.warning("Could not parse product data from an item element.")
except NoSuchElementException:
logging.error(f"Item container selector '{self.config['item_container_selector']}' not found on
page.")
except Exception as e:
logging.error(f"An error occurred while scraping items: {e}")
def run(self):
"""
Executes the scraping process.
"""
self.driver = self.driver_manager.get_driver()
if not self.driver:
logging.error("Failed to get WebDriver. Exiting.")
return
try:
self.driver.get(self.config["start_url"])
current_page = 1
while current_page <= self.max_pages:
logging.info(f"Processing page {current_page} at {self.driver.current_url}")
self.scrape_page()
time.sleep(self.config.get("delay_between_pages", 2)) # Respectful delay
# Check for pagination
pagination_selector = self.config["pagination_selector"]
if pagination_selector:
try:
# Attempt to find the next page button/link using specified selector
# Use wait_for_element here for robustness
next_page_button = wait_for_element(self.driver, By.CSS_SELECTOR,

pagination_selector, timeout=5)
if not next_page_button:
next_page_button = wait_for_element(self.driver, By.XPATH, pagination_selector,

timeout=5)

if next_page_button and next_page_button.is_displayed() and

next_page_button.is_enabled():

logging.info(f"Clicking next page: {next_page_button.text or 'No text'}")
robust_click(self.driver, By.CSS_SELECTOR, pagination_selector) # Use robust click
current_page += 1
else:
logging.info("No more next page button found or not clickable. Ending pagination.")
break
except (NoSuchElementException, TimeoutException):
logging.info("Pagination element not found or timed out. Assuming last page.")
break
except Exception as e:
logging.error(f"Error during pagination: {e}. Ending pagination.")
break
else:
logging.info("No pagination selector configured. Scraping single page.")
break # No pagination configured, so stop after first page
except Exception as e:
logging.critical(f"An unhandled error occurred during scraping: {e}")
finally:
self.driver_manager.quit_driver()
logging.info(f"Scraping finished. Total products scraped: {len(self.scraped_products)}")
save_data_to_json(self.scraped_products, "scraped_products.json")