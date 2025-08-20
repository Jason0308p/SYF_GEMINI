import asyncio
import pandas as pd
from playwright.async_api import async_playwright
import datetime
import urllib.parse
import os

# --- 設定 ---
KEYWORDS_FILE = "keywords.xlsx"
OUTPUT_FILE = f"alibaba_scraped_data_{datetime.datetime.now().strftime("%Y%m%d")}.xlsx"
SCREENSHOTS_DIR = "product_screenshots"
TARGET_KEYWORDS = ["custom", "logo", "personalized", "客製化", "LOGO印刷"]
MAX_PRODUCTS_PER_KEYWORD = 3

async def scrape_product_page(page):
    """從產品頁面抓取詳細資訊"""
    await page.wait_for_load_state('domcontentloaded')
    product_data = {
        "產品英文名稱": "N/A", "產品中文名稱": "N/A", "價格": "N/A",
        "規格": "N/A", "尺寸": "N/A", "顏色": "N/A",
        "產品簡述": "N/A", "產品URL": page.url
    }
    try:
        title_element = await page.query_selector('h1')
        if title_element:
            product_data["產品英文名稱"] = await title_element.text_content()
            product_data["產品中文名稱"] = product_data["產品英文名稱"]

        price_element = await page.query_selector('div[class*="price"] span[class*="price"]')
        if price_element:
            product_data["價格"] = await price_element.text_content()

        desc_element = await page.query_selector('div[class*="description"]')
        if desc_element:
            product_data["產品簡述"] = (await desc_element.text_content())[:500]

        spec_details = ""
        detail_elements = await page.query_selector_all('div[class*="specs"] >> tr, div[class*="attributes"] >> div')
        for item in detail_elements:
            spec_details += await item.text_content() + "\n"
        product_data["規格"] = spec_details.strip()

    except Exception as e:
        print(f"在頁面 {page.url} 抓取資料時出錯: {e}")
    return product_data

async def main():
    """主執行程式"""
    # 建立主截圖資料夾
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    try:
        keywords_df = pd.read_excel(KEYWORDS_FILE)
        search_keywords = keywords_df["關鍵字"].dropna().tolist()
    except FileNotFoundError:
        print(f"錯誤: 找不到輸入檔案 '{KEYWORDS_FILE}'。請確認檔案存在於目錄中。")
        return
    except KeyError:
        print(f"錯誤: 在 '{KEYWORDS_FILE}' 中找不到 '關鍵字' 欄位。")
        return

    all_products_data = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        for keyword in search_keywords:
            print(f"--- 正在搜尋關鍵字: {keyword} ---")
            # 為每個關鍵字建立子資料夾
            keyword_screenshot_dir = os.path.join(SCREENSHOTS_DIR, keyword.replace(' ', '_'))
            os.makedirs(keyword_screenshot_dir, exist_ok=True)
            
            page = await context.new_page()
            try:
                encoded_keyword = urllib.parse.quote(keyword)
                search_url = f"https://www.alibaba.com/products/{encoded_keyword}.html"
                print(f"正在導航至搜尋頁面: {search_url}")
                
                await page.goto(search_url, wait_until='domcontentloaded', timeout=60000)
                print("搜尋頁面載入完成。")

                product_card_selector = "div.search-card-e-card"
                print(f"正在等待產品卡片選擇器: {product_card_selector}...")
                await page.wait_for_selector(product_card_selector, timeout=30000)
                print("產品卡片已找到。")

                product_cards = await page.query_selector_all(product_card_selector)
                product_links_to_visit = []
                for card in product_cards:
                    title_element = await card.query_selector('h2.search-card-e-title')
                    link_element = await card.query_selector('a.search-card-e-slider__link')

                    if title_element and link_element:
                        title_text = (await title_element.text_content()).lower()
                        if any(target in title_text for target in TARGET_KEYWORDS):
                            href = await link_element.get_attribute('href')
                            if href and not href.startswith('http'):
                                href = "https:" + href
                            product_links_to_visit.append(href)

                    if len(product_links_to_visit) >= MAX_PRODUCTS_PER_KEYWORD:
                        break
                
                print(f"找到 {len(product_links_to_visit)} 個符合條件的產品連結。")

                # **--- 截圖邏輯 ---**
                product_index = 0
                for link in product_links_to_visit:
                    product_index += 1
                    product_page = await context.new_page()
                    try:
                        await product_page.goto(link, wait_until='domcontentloaded')
                        print(f"正在抓取: {link}")
                        
                        # 產生截圖路徑並儲存
                        screenshot_path = os.path.join(keyword_screenshot_dir, f"product_{product_index}.png")
                        await product_page.screenshot(path=screenshot_path, full_page=True)
                        print(f"已儲存截圖至: {screenshot_path}")

                        scraped_data = await scrape_product_page(product_page)
                        all_products_data.append(scraped_data)
                    except Exception as e:
                        print(f"訪問或抓取頁面 {link} 時出錯: {e}")
                    finally:
                        await product_page.close()

            except Exception as e:
                print(f"處理關鍵字 '{keyword}' 時發生錯誤: {e}")
                await page.screenshot(path=f'error_{keyword}.png')
                print(f"已儲存錯誤截圖至 error_{keyword}.png")
            finally:
                await page.close()

        await browser.close()

    if all_products_data:
        output_df = pd.DataFrame(all_products_data)
        output_df.to_excel(OUTPUT_FILE, index=False)
        print(f"\n成功完成爬蟲！資料已儲存至 '{OUTPUT_FILE}'")
    else:
        print("\n爬蟲結束，沒有抓取到任何資料。")

if __name__ == "__main__":
    asyncio.run(main())