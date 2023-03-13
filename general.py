from playwright.sync_api import sync_playwright
from config import summary_decorator, agent_rotation

@summary_decorator
def get_full_text_general(url, user_agent):
    substack_selector = "div .footer-slogan-blurb a[native=\"true\"]"
    selector_one = "article"
    selector_one = ":has(> p)"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent= user_agent)
        page.set_viewport_size({"width": 750, "height": 1334}) #Mobile website
        page.goto(url)
        full_pages = max((x.inner_text() for x in page.query_selector_all(selector_one)), key=len).replace("\n", "")
        print(full_pages)
        # full_pages = ''.join(x.inner_text() for x in page.query_selector_all(selector)).replace("\n", "")
    print(len(full_pages))
    return full_pages

if __name__ == "__main__":
    url = "https://blog.chain.link/smart-contract-use-cases/" # Tesing Url
    # url = "https://www.stakingrewards.com/journal/interview-with-evmos-where-evm-meets-interchain-composability/" # Tesing Url
    # url = "https://6thman.ventures/writing/simulating-token-economies-motivations-and-insights/" # Tesing Url
    print(get_full_text_general(url, agent_rotation()))
