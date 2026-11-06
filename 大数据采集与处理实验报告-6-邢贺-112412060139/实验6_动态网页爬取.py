# -*- coding: utf-8 -*-
# 安装依赖：python -m pip install selenium pandas


# %% 实验6 动态网页爬取

# %% 1. 利用 Selenium 登录的代码

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.EdgeOptions()
options.add_argument("--window-size=1440,1000")
service = Service(r"D:/msedgedriver64/msedgedriver.exe")
driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 60)

rank_url = "https://www.shanghairanking.cn/rankings/bcur/2025"
driver.get(rank_url)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-box tbody tr .name-cn")))

# %% 2. 利用 Selenium 解析数据的代码

def parse_page():
    page_data = []
    rows = driver.find_elements(By.CSS_SELECTOR, "#content-box tbody tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        page_data.append({
            "排名": cells[0].text.strip(),
            "学校名称": cells[1].find_element(By.CSS_SELECTOR, ".name-cn").text.strip(),
            "标签": "/".join(tag.text.strip() for tag in cells[1].find_elements(By.CSS_SELECTOR, ".tags")),
            "省市": cells[2].text.strip(),
            "类型": cells[3].text.strip()
        })
    return page_data

all_data = []
page = 1
started = time.perf_counter()
driver.get(rank_url)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-box tbody tr .name-cn")))

while True:
    page_data = parse_page()
    all_data.extend(page_data)
    print(f"第 {page} 页：{len(page_data)} 条")

    next_button = driver.find_element(By.CSS_SELECTOR, "#content-box .ant-pagination-next")
    if "ant-pagination-disabled" in next_button.get_attribute("class"):
        break

    first_school = page_data[0]["学校名称"]
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
    next_link = next_button.find_element(By.TAG_NAME, "a")
    ActionChains(driver).move_to_element(next_link).pause(0.5).click().perform()
    wait.until(lambda browser: browser.find_element(By.CSS_SELECTOR, "#content-box tbody tr .name-cn").text.strip() != first_school)
    time.sleep(0.5)
    page += 1

print(f"共采集 {len(all_data)} 条，耗时 {time.perf_counter() - started:.1f} 秒")

# %% 3. 数据存储的代码

df = pd.DataFrame(all_data)
df = df.drop_duplicates(subset=["学校名称"]).reset_index(drop=True)
df.to_csv("软科2025中国大学排名.csv", index=False, encoding="utf-8-sig")
print(f"已保存 {len(df)} 条数据")

# %% 4. 登录成功的网页截图

driver.get(rank_url)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-box tbody tr .name-cn")))
driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", driver.find_element(By.ID, "content-box"))
driver.save_screenshot("软科排名页面.png")
print("网页截图已保存：软科排名页面.png")

# %% 5. 存储到文件中的数据内容

saved_data = pd.read_csv("软科2025中国大学排名.csv", encoding="utf-8-sig", keep_default_na=False)
print(f"数据条数：{len(saved_data)}")
print(saved_data.head(15).to_string(index=False))

driver.quit()

# %% 百度自动检索

service = Service(r"D:/msedgedriver64/msedgedriver.exe")
driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 60)
driver.get("https://www.baidu.com")
search_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chat-textarea, #kw")))
search_box.send_keys("大数据采集与处理")
search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#chat-submit-button, #su")))
search_button.click()

# %% 百度检索结果

WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.ID, "content_left")))
titles = driver.find_elements(By.CSS_SELECTOR, "#content_left h3")
for index, title in enumerate(titles[:10], 1):
    print(f"{index}. {title.text}")
driver.save_screenshot("百度检索结果.png")
print("检索截图已保存：百度检索结果.png")

driver.quit()
