# agentic-web-scraper/main.py
import sys
import os

import logging
# Add the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from config_parser import ConfigParser
from scraper_agent import ScraperAgent
# Configure logging for main script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def main():
"""
Main entry point for the Agentic Web Scraper.
Loads config and runs the scraping agent.
"""
config_file_path = os.path.join(os.path.dirname(__file__), 'configs', 'example_site_config.json')
try:
config_parser = ConfigParser(config_file_path)
config = config_parser.load_config()
# Choose browser ('chrome' or 'firefox') and headless mode (True/False)
# Note: Headless mode may sometimes fail on complex sites that detect headless browsers.
# For debugging, set headless=False to see the browser actions.
scraper_agent = ScraperAgent(config, browser='chrome', headless=True)
scraper_agent.run()
except FileNotFoundError as e:
logging.error(f"Configuration file error: {e}")
logging.info("Please ensure 'configs/example_site_config.json' exists.")
except ValueError as e:
logging.error(f"Configuration validation error: {e}")
logging.info("Please check the format and required fields in your config file.")
except Exception as e:
logging.critical(f"An unexpected error occurred during execution: {e}")
if __name__ == "__main__":
main()