from playwright.sync_api import sync_playwright
from config import summary_decorator, agent_rotation

@summary_decorator
def get_full_text_substack(url, user_agent):
    selector = "div[class=\"\"]"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent = user_agent)
        page.goto(url)
        page.wait_for_selector(selector=selector)  # wait for content to load
        full_pages = page.query_selector(selector).inner_text().replace("\n", "")
    return full_pages

if __name__ == "__main__":
    url = "https://www.notboring.co/p/designing-token-economies" # Tesing Url
    print(get_full_text_substack(url, agent_rotation()))