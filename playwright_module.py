import time
import asyncio
import traceback

from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright


scriptString = """  
navigator.webdriver = false  
Object.defineProperty(navigator, 'webdriver', {  
get: () => false  
})  
"""


def add_stealth(page):
    page.add_init_script(scriptString)
    return True


async def async_add_stealth(page):
    await page.add_init_script(scriptString)
    return True


def render_page(link, proxy=None, wait_for=None, sleep=1):
    for try_count in range(2):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(proxy=proxy)
                page = browser.new_page()
                add_stealth(page)
                page.goto(link, wait_until='load')
                if wait_for:
                    for try_ in range(2):
                        if wait_for not in page.content():
                            time.sleep(sleep // 2)
                            continue
                content = page.content()
                if not content:
                    browser.close()
                    continue
                browser.close()

            return content
        except Exception as e:
            print(e)
            continue


async def async_render_page(link, proxy=None, wait_for=None, sleep=1):
    for try_count in range(2):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(proxy=proxy)
                page = await browser.new_page()
                await async_add_stealth(page)
                await page.goto(link, wait_until='load')
                if wait_for:
                    for try_ in range(2):
                        content = await page.content()
                        if wait_for not in content:
                            await asyncio.sleep(sleep // 2)
                            continue
                content = await page.content()
                if not content:
                    await browser.close()
                    continue
                await browser.close()

            return content
        except Exception as e:
            print(e)
            # print(traceback.format_exc())
            continue


if __name__ == '__main__':
    url = ''
    render_page(url)