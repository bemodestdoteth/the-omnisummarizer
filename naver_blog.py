from playwright.sync_api import sync_playwright
from config import summary_decorator, agent_rotation

@summary_decorator
def get_full_text_naver_blog(url, user_agent):
    selector = "div.se-main-container"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent= user_agent)
        page.set_viewport_size({"width": 750, "height": 1334}) #Mobile website
        page.goto(url)
        full_pages = ''.join(x.inner_text() for x in page.query_selector_all(selector)).replace("\n", "").replace("200b","")
    return full_pages

if __name__ == "__main__":
    url = "https://blog.naver.com/bizucafe/223038684684" # Tesing Url
    print(get_full_text_naver_blog(url, agent_rotation()))