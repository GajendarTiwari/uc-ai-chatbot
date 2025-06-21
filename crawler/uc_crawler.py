# crawler/uc_crawler.py
import os
from urllib.parse import urljoin, urlparse
from typing import Set

import requests
from bs4 import BeautifulSoup

# OUTPUT_DIR relative to project root
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data/pages")
SEED_URLS = [
    "https://www.uc.edu/",
    "https://admissions.uc.edu/",
    "https://grad.uc.edu/",
    "https://ceas.uc.edu/",
    "https://financialaid.uc.edu/",
    "https://innovation.uc.edu/",
]

def is_valid_uc_url(url: str) -> bool:
    """
    Only follow links ending in uc.edu.
    """
    parsed = urlparse(url)
    netloc = parsed.netloc
    return netloc.endswith("uc.edu")

def save_text(url: str, text: str) -> None:
    """
    Persist page text under crawler/data/pages/.
    """
    # Make sure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_")
    path = os.path.join(OUTPUT_DIR, f"{safe_name}.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"[ERROR] Could not save {url} to {path}: {e}")

def crawl_url(session: requests.Session, url: str, visited: Set[str], depth: int) -> None:
    """
    Recursively crawl up to `depth` levels.
    """
    if depth < 1 or url in visited:
        return
    visited.add(url)

    try:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        save_text(url, text)

        # Find links
        for link in soup.find_all("a", href=True):
            full = urljoin(url, link["href"])
            if is_valid_uc_url(full):
                crawl_url(session, full, visited, depth - 1)
    except Exception as e:
        print(f"[ERROR] Failed to crawl {url}: {e}")

def main() -> None:
    """
    Run crawler. Adjust depth or add more SEED_URLS if needed.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    visited: Set[str] = set()
    with requests.Session() as sess:
        for seed in SEED_URLS:
            crawl_url(sess, seed, visited, depth=1)  # increase depth if needed

if __name__ == "__main__":
    main()
