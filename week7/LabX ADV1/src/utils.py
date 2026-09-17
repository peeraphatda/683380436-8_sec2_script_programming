# agentic-web-scraper/src/utils.py
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException,
WebDriverException
def save_data_to_json(data, filename, directory='data'):
"""Saves a list of dictionaries to a JSON file."""
os.makedirs(directory, exist_ok=True)
filepath = os.path.join(directory, filename)
try:
with open(filepath, 'w', encoding='utf-8') as f:
json.dump(data, f, indent=4, ensure_ascii=False)
print(f"Data saved to {filepath}")
return True
except IOError as e:
print(f"Error saving data to JSON file: {e}")
return False
def wait_for_element(driver, by, value, timeout=10):
"""
Waits for an element to be present on the DOM and visible.
Returns the element or raises a TimeoutException.
"""
try:
element = WebDriverWait(driver, timeout).until(
EC.presence_of_element_located((by, value))
)
# Further check if element is visible
WebDriverWait(driver, timeout).until(
EC.visibility_of(element)
)
return element
except TimeoutException:
print(f"Timeout waiting for element: {value}")
return None
except NoSuchElementException:
print(f"Element not found after wait: {value}")
return None

def robust_click(driver, by, value, max_attempts=3, delay_between_attempts=2):
"""
Attempts to click an element multiple times if it's not immediately clickable.
"""
for attempt in range(max_attempts):
try:
element = wait_for_element(driver, by, value)
if element:
element.click()
return True
else:
return False # Element not found even after waiting
except WebDriverException as e:
print(f"Click attempt {attempt + 1} failed: {e}")
if attempt < max_attempts - 1:
time.sleep(delay_between_attempts)
print(f"Failed to click element {value} after {max_attempts} attempts.")
return False
def scroll_to_bottom(driver):
"""Scrolls to the bottom of the page."""
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2) # Give some time for content to load