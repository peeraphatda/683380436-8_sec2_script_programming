import requests
from bs4 import BeautifulSoup

class SimpleWebScraper:
    def __init__(self, target_url):
        self.target_url = target_url

    def _get_html_content(self):
        print(f"Downloading content from: {self.target_url}")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(self.target_url, headers=headers, timeout=10)
            response.raise_for_status()
            print("Successfully downloaded content.")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error downloading page: {e}")
            return None

    def scrape_main_titles(self):
        html_content = self._get_html_content()
        if not html_content:
            return None
        soup = BeautifulSoup(html_content, 'html.parser')
        book_title_tag = soup.find('div', class_='page-header')
        book_title = book_title_tag.find('h1').get_text(strip=True) if book_title_tag and book_title_tag.find('h1') else "Book Title Not Found"
        refined_chapter_titles = []
        toctree_wrapper = soup.find('div', class_='toctree-wrapper')
        if toctree_wrapper:
            chapter_links = toctree_wrapper.select('li.toctree-l1 a.reference.internal')
            for link in chapter_links:
                title = link.get_text(strip=True)
                if title:
                    refined_chapter_titles.append(title)
        return {"book_title": book_title, "chapter_titles": refined_chapter_titles}
