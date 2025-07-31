from playwright.async_api import async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from urllib.parse import urljoin


async def search_movie(query):
    parsed = {
                    "title": "no title",
                    "link": "no link",
                    "rating": "no rating",
                    "description": "no description"
                }
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://mm.lordfilm15.ru")

        search_box = page.get_by_placeholder("Введите название").nth(0)
        await search_box.fill(query)
        await search_box.press("Enter")
        try:
            await page.wait_for_selector(".th-item", timeout=5000)
            stream_boxes = await page.locator("//div[contains(@class,'th-item')]").element_handles()
            box = stream_boxes[0]
            title_element = await box.query_selector("//div[contains(@class,'th-title')]")
            title = await title_element.text_content() if title_element else "No title"
            link_element = await box.query_selector("//a[contains(@class,'th-in with-mask')]")
            link = await link_element.get_attribute("href") if link_element else "No link"

            await page.goto(link)
            description_element = await page.query_selector("span[itemprop='description']")
            description = await description_element.text_content() if description_element else "No description"
            rating_element = await page.query_selector("//div[contains(@class,'frate frate-imd')]")
            rating = await rating_element.text_content() if rating_element else "No rating"
            poster_element = await page.query_selector("//div[contains(@class,'fposter img-wide')]")
            img_tag = await poster_element.query_selector("img")
            poster = await img_tag.get_attribute("src") if img_tag else "No poster"

            parsed = {
                    "title": title,
                    "link": link,
                    "rating": rating,
                    "description": description,
                    "poster": urljoin("https://mm.lordfilm15.ru", poster),
                }

        except PlaywrightTimeoutError:
            await page.goto("https://lordfilm-dune.store/")
            search_box = page.get_by_placeholder("Введите название").nth(0)
            await search_box.fill(query)
            await search_box.press("Enter")
            await page.wait_for_selector(".order", timeout=5000)
            stream_boxes = await page.locator("//a[contains(@class,'item')]").element_handles()
            box = stream_boxes[0]
            link = await box.get_attribute("href")
            await page.goto(link)
            title = await page.get_attribute('meta[property="og:title"]', "content")
            description = await page.get_attribute('meta[property="og:description"]', "content")
            link = await page.get_attribute('meta[property="og:url"]', "content")
            rating_element = await page.query_selector("//div[contains(@class,'imdb')]")
            rating = await rating_element.text_content() if rating_element else "No rating"
            poster_element = await page.query_selector("//div[contains(@class,'poster')]")
            img_tag = await poster_element.query_selector("img")
            poster = await img_tag.get_attribute("src") if img_tag else "No poster"

            parsed = {
                    "title": title,
                    "link": link,
                    "rating": rating,
                    "description": description,
                    "poster": poster,
                    }
        except Exception as e:
            print(f"Exception occured: {e}")
        finally:
            await page.close()
            await browser.close()
            return parsed
