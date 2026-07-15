# Google Maps reviews tracker with playwright, Airtable
#
# Replace the following placeholders before running:
#
# keywords
# AIRTABLE_TOKEN
# BASE_ID
# TABLE_NAME

import time
import re
from playwright.sync_api import sync_playwright
from pyairtable import Api

url = "http://www.google.com/maps"
keywords = ["Your Ex.1", "Your Ex.2", "Your Ex.n"]
AIRTABLE_TOKEN = "Your token"
BASE_ID = "Your Base id"
TABLE_NAME = "Your table name"

api = Api(AIRTABLE_TOKEN)
table = api.table(BASE_ID, TABLE_NAME)

def scrape_google_maps(url):
    
    clear_old_data(table)

    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(
            locale="zh-TW",                         # chinese environment, or your language.
            viewport={'width': 1920, 'height': 1080} 
        )
        page = context.new_page()
        page.goto(url)
        page.get_by_role("button", name="全部拒絕").click()

        for keyword in keywords:
            print(">>> 正在前往店家頁面...")
            page.get_by_role("combobox").fill(keyword)
            page.get_by_role("combobox").press("ArrowDown")
            page.get_by_role("combobox").press("Enter")
            print(">>> 定位店家...")
            time.sleep(2)
            print(">>> 搜尋評論...")
            page.get_by_role("button", name="排序評論").click()
            page.get_by_role("menuitemradio").filter(has_text="最新").click()
            #page.get_by_role("menuitemradio", name="最新").click()               
            print(">>> 排序下捲...")
            # listing comments
            while True:
            # scroll
                page.mouse.wheel(0, 1000)
                #time.sleep(2)
                breaker = page.get_by_text(re.compile(r"天前|月前|年前"), exact=False)
                if breaker.count() > 0: break

            today_locators = page.get_by_text(re.compile(r"([A-Za-zÀ-ÿäöüÄÖÜß]+|[\u4e00-\u9fff]+).*(小時前|分鐘前|秒前).+"), exact=False) #.*([0-9]+\s則評論)?
            
            if today_locators.count() == 0: 
                print(f"{keyword} 搜索結束.\n")
                continue

            for review in today_locators.all():
                
                timeline, rating, who, what, language = "", "", "", "", "" # keyword already done.

                star_locator = review.locator('[aria-label*="星"], [title*="星"], [aria-label*="star"], [title*="star"], .kv9F6e, span[aria-label*="顆星"], span[role="img"]')
                if star_locator.count() == 0: star_locator = review.locator('span.kvMYJc') # edited, therefore html structure altered.
                
                if star_locator.count() == 0: print("?")                    
                else:    
                    star_label = star_locator.first.get_attribute("aria-label")
                    if star_label: 
                        rating += re.search(r"\d", star_label).group()
                        print(rating, "顆星")
                # if 'more' needed or not
                more = review.get_by_text("更多").first
                try:
                    if more.is_visible(): 
                        more.click(force=True)
                        print(">>> 展開評論...")
                        time.sleep(2)
                except: 
                    print("NO 'more' to click.")
                    pass

                try:
                    print(">>> 整理文字...")      
                    text = review.inner_text()
                    #print(text)
                    if len(text) > 0:
                        lines = re.findall(r'.+', text)
                        len_lines = len(lines)
                        if "業主回應" not in lines[0]: who += lines[0]  
                        else: who += "業主" 
                        language += re.findall(r'(?<=查看原文 \().+?(?=\))', text)[0]

                        for i in range(1, len_lines):
                            if "業主" in who: 
                                timeline += re.findall(r'(?<=業主回應 ).+', lines[0])[0]
                                what += "".join(lines[1: len_lines - 1])
                                if "提供翻譯" not in lines[-1]: what += lines[-1]
                                break
                            linesi = lines[i]
                            if "小時前" in linesi or "分鐘前" in linesi or "秒前" in linesi:
                                timeline += linesi
                                continue
                            if re.match(r'[^a-zA-Z0-9\u4e00-\u9fff]', linesi) or "則評論" in linesi or "張相片" in linesi or "在地嚮導" in linesi or "新" in linesi or "預訂網址" in linesi: continue                        
                            #if "上次造訪時間" in linesi or "等待時間" in linesi or "建議預定" in linesi or "提供翻譯" in linesi or "按讚" in linesi or "餐點類型" in linesi or "消費金額" in linesi or "預訂網址" in linesi or "親子友善程度" in linesi: break
                            if "提供翻譯" in linesi or "按讚" in linesi or "分享" in linesi: break
                            what += linesi + " | "                                         
                    
                    print(timeline, who, what, language)    
                    print("-" * 30)
                    try:
                        table.create({
                            "timeline": timeline,
                            "keyword": keyword,
                            "rating": rating,
                            "who": who,
                            "what": what,
                            "language": language,
                            "url": page.url
                        }) #, key_fields=["keyword", "what"]
                        print("✅")
                    except: print("寫入失敗")

                except: 
                    print('No words left.')
                    pass

            print(f"{keyword} 搜索結束.\n")  

        browser.close()
    

def clear_old_data(table, days=7):

    all_records = table.all()    
    to_delete = [r['id'] for r in all_records]     
    
    if to_delete:
        print(f">>> 正在清理 {len(to_delete)} 筆舊資料...")
        table.batch_delete(to_delete) 
        print(">>> 清理完成。")

if __name__ == "__main__": 

    scrape_google_maps(url)

