from langchain.tools import tool

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import helium
from selenium import webdriver
from bs4 import BeautifulSoup
from typing import Dict, Any


def create_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--window-size=1000,1350")
    chrome_options.add_argument("--disable-pdf-viewer")
    chrome_options.add_argument("--window-position=0,0")
    global driver
    driver = helium.start_chrome(headless=False, options=chrome_options)

@tool
def search_item_ctrl_f(text: str, nth_result: int = 1) -> str:
    """
    Searches for text on the current page via Ctrl + F and jumps to the nth occurrence.
    Args:
        text: The text to search for
        nth_result: Which occurrence to jump to (default: 1)
    """
    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    if nth_result > len(elements):
        raise Exception(
            f"Match n°{nth_result} not found (only {len(elements)} matches found)"
        )
    result = f"Found {len(elements)} matches for '{text}'."
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    result += f"Focused on element {nth_result} of {len(elements)}"
    return result


@tool
def go_back() -> str:
    """Goes back to previous page."""
    driver.back()
    # helium.get_driver().get_current_url()
    return f"Navigated back to {driver.current_url}"


@tool
def close_popups() -> str:
    """
    Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows!
    This does not work on cookie consent banners.
    """
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    return "Pop-ups closed"

@tool
def go_to_url(url: str) -> str:
    """
    Navigates to a given URL.
    Args:
        url: The URL to navigate to
    """
    helium.go_to(url)
    return f"Navigated to {driver.current_url}"

@tool
def click_element(text: str) -> str:
    """
    Clicks on a clickable element with the given text.
    Args:
        text: The text of the clickable element
    """
    if (helium.Text(text).exists()):
        helium.click(text)
        return f"Clicked on a link with text '{text}'"
    
    return f"Text '{text}' found on the page."

@tool
def click_link(link: str) -> str:
    """
    Clicks on a link element with the given text.
    Args:
        link: The text of the link element
    """
    if (helium.Link(link).exists()):
        helium.click(helium.Link(link))
        return f"Clicked on a link with text '{link}'"

    return f"No link with text '{link}' found on the page."
    
@tool
def extract_webpage_to_json() -> Dict[str, Any]:
    """
    Extracts structured information from the specified HTML webpage and returns it as a JSON-serializable Python dictionary.
    """
    html = driver.page_source or ""
    soup = BeautifulSoup(html, 'html.parser')

    # Example extraction logic (customize for structure/needs)
    data = {
        'title': soup.title.string if soup.title else None,
        'headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
        'content': [p.get_text(strip=True) for p in soup.find_all(['p', 'span', 'div'])],
        'links': [a['href'] for a in soup.find_all('a', href=True)],
        'list_items': [li.get_text(strip=True) for li in soup.find_all('li')]
    }

    return data

# @tool 
# def scroll_down(num_pixels: int) -> str:
#     """
#     Scrolls down the page by a given number of pixels.
#     Args:
#         num_pixels: The number of pixels to scroll down
#     """
#     helium.scroll_down(num_pixels=num_pixels)
#     return f"Scrolled down by {num_pixels} pixels"

# tools = [add, multiply, divide]
tools = [search_item_ctrl_f, go_back, close_popups, go_to_url, click_element, click_link, extract_webpage_to_json]
tools_by_name = {tool.name: tool for tool in tools}
