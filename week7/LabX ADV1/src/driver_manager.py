import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
class DriverManager:
"""
Manages the setup and teardown of Selenium WebDriver instances.
Automates driver download if not present.
"""
def __init__(self, browser_name='chrome', headless=True):
self.browser_name = browser_name.lower()
self.headless = headless
self.driver = None
def get_driver(self):
"""
Initializes and returns a WebDriver instance.
"""

if self.driver:
return self.driver
if self.browser_name == 'chrome':
options = webdriver.ChromeOptions()
if self.headless:
options.add_argument('--headless')
options.add_argument('--no-sandbox') # Required for some environments (e.g., Docker)
options.add_argument('--disable-dev-shm-usage') # Required for some environments
options.add_argument('--log-level=3') # Suppress console logs
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
try:
service = ChromeService(ChromeDriverManager().install())
self.driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
print(f"Error setting up Chrome driver: {e}")
print("Make sure Chrome browser is installed and try running 'pip install webdriver-manager'.")
return None
elif self.browser_name == 'firefox':
options = webdriver.FirefoxOptions()
if self.headless:
options.add_argument('--headless')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; rv:91.0)
Gecko/20100101 Firefox/91.0')
try:
service = FirefoxService(GeckoDriverManager().install())
self.driver = webdriver.Firefox(service=service, options=options)
except Exception as e:
print(f"Error setting up Firefox driver: {e}")
print("Make sure Firefox browser is installed and try running 'pip install webdriver-manager'.")
return None
else:
raise ValueError(f"Unsupported browser: {self.browser_name}. Choose 'chrome' or 'firefox'.")
# Set implicit wait time (optional, but good for dynamic pages)
self.driver.implicitly_wait(10) # waits up to 10 seconds for elements to appear
return self.driver

def quit_driver(self):
"""
Quits the WebDriver instance if it's running.
"""
if self.driver:
self.driver.quit()
self.driver = None
print("WebDriver quit successfully.")
# Note: For webdriver_manager to work, run 'pip install webdriver-manager'