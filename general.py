from playwright.async_api import async_playwright
from config import summary_decorator, agent_rotation
import asyncio

@summary_decorator
async def get_full_text_general(url, user_agent):
    substack_selector = "div .footer-slogan-blurb a[native=\"true\"]"
    selector_one = "article"
    selector_one = ":has(> p)"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(user_agent= user_agent)
        await page.set_viewport_size({"width": 750, "height": 1334}) #Mobile website
        await page.goto(url)

        full_pages = ''
        elements = await page.query_selector_all(selector_one)
        for element in elements:
            inner_text = await element.inner_text()
            if len(inner_text.replace('\n', '')) > len(full_pages):
                full_pages = inner_text.replace('\n', '')
        # full_pages = max((x.inner_text() for x in await page.query_selector_all(selector_one)), key=len).replace("\n", "")
        # full_pages = ''.join(x.inner_text() for x in page.query_selector_all(selector)).replace("\n", "")
    return full_pages

if __name__ == "__main__":
    url = "https://bootcamp.uxdesign.cc/a-step-by-step-guide-to-building-a-chatbot-based-on-your-own-documents-with-gpt-2d550534eea5" # Tesing Url
    # url = "https://blog.chain.link/smart-contract-use-cases/" # Tesing Url
    # url = "https://www.stakingrewards.com/journal/interview-with-evmos-where-evm-meets-interchain-composability/" # Tesing Url
    # url = "https://6thman.ventures/writing/simulating-token-economies-motivations-and-insights/" # Tesing Url
    print(asyncio.run(get_full_text_general(url, agent_rotation())))