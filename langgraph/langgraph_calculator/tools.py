from langchain.tools import tool

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import helium
from selenium import webdriver
from bs4 import BeautifulSoup, Comment
import re

# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply `a` and `b`."""
#     return a * b


# @tool
# def add(a: int, b: int) -> int:
#     """Add `a` and `b`."""
#     return a + b


# @tool
# def divide(a: int, b: int) -> float:
#     """Divide `a` and `b`."""
#     return a / b

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
    return f"Navigated back to {helium.get_driver().current_url}"


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
    return f"Navigated to {helium.get_driver().current_url}"

@tool
def click_element(text: str) -> str:
    """
    Clicks on a clickable element with the given text.
    Args:
        text: The text of the clickable element
    """
    helium.click(text)
    return f"Clicked on element with text '{text}'"

@tool
def click_link(link: str) -> str:
    """
    Clicks on a link element with the given text.
    Args:
        link: The text of the link element
    """
    helium.click(helium.Link(link))
    return f"Clicked on a link with text '{link}'"

@tool
def extract_sanitized_html(max_chars: int = 2000) -> str:
    """
    Extracts and sanitizes the current page's HTML content.
    Includes URL, title, meta description, top headings, top links, buttons, forms and a text snippet.
    Args:
        max_chars: Maximum number of characters in the output summary
    """
    d = helium.get_driver()

    html = d.page_source or ""
    soup = BeautifulSoup(html, "html.parser")

    # remove noisy tags and comments
    for tag in soup(["script", "style", "noscript", "meta", "link", "svg", "iframe", "canvas"]):
        tag.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # quick extractions
    title = (soup.title.string.strip() if soup.title and soup.title.string else "")
    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag["content"].strip()

    # headings (collect a few)
    headings = []
    for h in soup.find_all(["h1", "h2", "h3"]):
        txt = h.get_text(" ", strip=True)
        if txt:
            headings.append(txt)
        if len(headings) >= 5:
            break

    # links and clickable elements (top few)
    links = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True) or a.get("aria-label") or a["href"]
        links.append((text, a["href"]))
        if len(links) >= 10:
            break

    buttons = []
    for el in soup.find_all(["button", "input"]):
        typ = el.get("type", "button")
        txt = el.get_text(" ", strip=True) or el.get("value") or el.get("aria-label") or ""
        if txt:
            buttons.append((txt, typ))
        if len(buttons) >= 10:
            break

    # forms summary
    forms = []
    for form in soup.find_all("form"):
        action = form.get("action", "")
        inputs = []
        for inp in form.find_all(["input", "select", "textarea"]):
            name = inp.get("name") or inp.get("id") or ""
            itype = inp.get("type", "")
            if name or itype:
                inputs.append(f"{name}:{itype}".strip(":"))
        forms.append({"action": action, "inputs": inputs})
        if len(forms) >= 5:
            break

    # visible text snippet
    visible_text = " ".join(soup.stripped_strings)
    visible_text = re.sub(r"\s+", " ", visible_text).strip()
    snippet = visible_text[: max(0, max_chars)]

    # assemble concise summary
    parts = []
    parts.append(f"URL: {d.current_url}")
    if title:
        parts.append(f"Title: {title}")
    if meta_desc:
        parts.append(f"Description: {meta_desc}")
    if headings:
        parts.append("Headings: " + " | ".join(headings))
    if links:
        parts.append("Links: " + ", ".join(f"'{t}' -> {href}" for t, href in links))
    if buttons:
        parts.append("Buttons: " + ", ".join(f"'{t}' ({typ})" for t, typ in buttons))
    if forms:
        forms_s = "; ".join(f"{f['action']}[{', '.join(f['inputs'])}]" for f in forms)
        parts.append("Forms: " + forms_s)
    parts.append("TextSnippet: " + snippet)

    result = "\n".join(parts)
    if len(result) > max_chars:
        return result[:max_chars].rstrip() + "..."
    return result

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
tools = [search_item_ctrl_f, go_back, close_popups, go_to_url, click_element, click_link, extract_sanitized_html]
tools_by_name = {tool.name: tool for tool in tools}
