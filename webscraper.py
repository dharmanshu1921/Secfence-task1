import http.client
import re
import socket
from urllib.parse import urlparse, urljoin

class WebScraper:
    def __init__(self, timeout=10):
        self.timeout = timeout

    def fetch_url(self, url):
        try:
            parsed_url = urlparse(url)
            scheme = parsed_url.scheme
            domain = parsed_url.netloc
            path = parsed_url.path if parsed_url.path else "/"

            if scheme == "https":
                conn = http.client.HTTPSConnection(domain, timeout=self.timeout)
            else:
                conn = http.client.HTTPConnection(domain, timeout=self.timeout)

            # mimic browser request
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            }
            conn.request("GET", path, headers=headers)
            
            response = conn.getresponse()

            # Handle redirects
            if response.status in (301, 302, 303, 307, 308):
                new_url = response.getheader("Location")
                conn.close()
                return self.fetch_url(urljoin(url, new_url))

            if response.status == 200:
                html_content = response.read().decode("utf-8", errors="ignore")
                conn.close()
                return html_content
            else:
                print(f"Failed to fetch {url}. Status code: {response.status}")
                conn.close()
                return None

        except (http.client.HTTPException, socket.timeout, socket.error) as e:
            print(f"Connection error: {e}")
            return None

    def extract_content(self, html_content):
        if not html_content:
            return [], []

        headings = re.findall(r'<h([1-6])[^>]*>(.*?)</h\1>', html_content, re.DOTALL | re.IGNORECASE)
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL | re.IGNORECASE)

        def clean_html(text):
            # Remove HTML tags, decode entities, normalize whitespace
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'&[a-z]+;', ' ', text, flags=re.IGNORECASE)
            text = re.sub(r'\s+', ' ', text).strip()
            return text

        # Clean and filter extracted content
        headings = [clean_html(h[1]) for h in headings if clean_html(h[1])]
        paragraphs = [clean_html(p) for p in paragraphs if clean_html(p)]

        return headings, paragraphs

    def scrape(self, url):
        html_content = self.fetch_url(url)
        if html_content:
            headings, paragraphs = self.extract_content(html_content)
            
            print("Extracted Headings:")
            for h in headings:
                print(h)
            
            print("\nExtracted Paragraphs:")
            for p in paragraphs:
                print(p)

scraper = WebScraper()
scraper.scrape("https://en.wikipedia.org/wiki/Shah_Rukh_Khan")