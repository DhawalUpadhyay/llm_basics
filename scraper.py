import re
from typing import Optional

import requests
from bs4 import BeautifulSoup


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_website_contents(url: str, timeout: int = 10) -> str:
    """Fetch a web page and return its main visible content.

    This removes scripts, styles, navigation, footer, headers, and other
    non-content elements before returning the cleaned text.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove non-content blocks
    for selector in [
        "script",
        "style",
        "header",
        "footer",
        "nav",
        "aside",
        "form",
        "noscript",
        "img",
        "svg",
        "iframe",
        ".advertisement",
        ".ads",
        ".cookie-banner",
        ".promo",
    ]:
        for element in soup.select(selector):
            element.decompose()

    # Prioritize main/content sections when available
    main_content = soup.find("main") or soup.find(id=re.compile(r"content|main|article", re.I))
    if main_content:
        content_soup = main_content
    else:
        content_soup = soup.body or soup

    # Remove empty tags and non-text elements
    for tag in content_soup.find_all(True):
        if tag.name in ["script", "style", "header", "footer", "nav", "aside", "form", "noscript"]:
            tag.decompose()

    text = content_soup.get_text(separator=" ", strip=True)
    return _clean_text(text)
