from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# # from webdriver_manager.chrome import ChromeDriverManager  # 可选，不手动下载也行
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import time

# 配置Chrome选项（可选）
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # 最大化窗口
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


# 初始化WebDriver（需替换为你的chromedriver路径）
driver = webdriver.Chrome(service=Service('D:\\appdate\\google_download\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'), options=options)
# 打开网页
driver.get("https://www.microsoft.com/zh-tw/rewards/about")
time.sleep(2)  # 等待页面加载
# input("按 Enter 键退出并关闭浏览器...")  # 等待你按键
try:
        # 方法1：直接点击那个链接
    login_link = driver.find_element(By.CSS_SELECTOR, 'a.cta[href="https://rewards.bing.com"]')
    login_link.click()
    print("已点击登入链接")
except Exception as e:
        print("点击登入失败：", e)

    # 通过XPath、CSS选择器或ID定位按钮并点击
    # button = driver.find_element(By.XPATH, "//button[@id='submit-button']")
    # button.click()

    # 等待观察效果
    # time.sleep(5)
# finally:
#     driver.quit()

# # 输入账号
# try:
#     email_input = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "usernameEntry"))
#     )
#     email_input.send_keys('自己邮箱')
#     driver.find_element(By.ID, "idSIButton9").click()  # 点击“下一步”
#     input("按 Enter 键退出并关闭浏览器")
#     print("已填写账号")
# except Exception as e:
#     print("填写账号失败:", e)
#     driver.quit()
#     exit()

try:
    email_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']"))
    )
    email_input.clear()
    for char in "chsnl@outlook.com":
        email_input.send_keys(char)
        time.sleep(0.1)  # 模拟人类输入
    email_input.send_keys("\n")  # 模拟按 Enter
    print("已填写账号")
except Exception as e:
    print("填写账号失败:", e)
    driver.quit()
    exit()
# try:
#     # 等待 email 输入框出现
#     email_input = WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//input[@type='email' or contains(@id, 'username')]")
#         )
#     )
#     email_input.clear()
#     email_input.send_keys("chsnl@outlook.com")
#     print("已成功输入邮箱")
# except Exception as e:
#     print("定位输入框失败:", e)
#     print("定位输入框失败:", e)




# # playwright 自动打开必应并搜索
# from playwright.sync_api import sync_playwright
# import random, time
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context(storage_state="bing_user.json")  # 登录后保存的 cookie
#     page = context.new_page()
#     page.goto("https://www.bing.com")
#
#     keywords = ["chatgpt", "python", "space", "news", "weather", "AI", "openai", "music"]
#     for i in range(30):
#         query = random.choice(keywords) + str(random.randint(1, 1000))
#         page.goto(f"https://www.bing.com/search?q={query}")
#         time.sleep(random.uniform(1, 2))
#
#     browser.close()

# from playwright.sync_api import sync_playwright
# import random, time
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context(storage_state="bing_user.json")
#     page = context.new_page()
#     page.goto("https://www.bing.com")
#     page.wait_for_load_state("load")
#
#     keywords = ["chatgpt", "python", "space", "news", "weather", "AI", "openai", "music"]
#     for i in range(30):
#         query = random.choice(keywords) + str(random.randint(1, 1000))
#         print(f"[{i+1}/30] Searching: {query}")
#         page.goto(f"https://www.bing.com/search?q={query}", wait_until="load")
#         page.wait_for_load_state("networkidle")
#         time.sleep(random.uniform(1.5, 3))
#
#     browser.close()



# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#
#     # 打开微软登录页面
#     page.goto("https://login.live.com")
#
#     # 等待你手动完成登录（或者自动填表）
#     print(">>> 请手动登录你的微软账号，登录完成后关闭此窗口 <<<")
#     input("按下回车以继续...")
#
#     # 保存登录状态（cookie）
#     context.storage_state(path="bing_user.json")
#     print(">>> 登录状态已保存为 bing_user.json")
#
#     browser.close()



 # 3-6 模拟用户滚动行为
        # for _ in range(random.randint(2, 4)):          # 随机滚动 2~4 次
        #     scroll_amount = random.randint(600, 1200)  # 每次滚动 600~1200 像素
        #     page.mouse.wheel(0, scroll_amount)
        #     time.sleep(random.uniform(1.5, 2.5))       # 每滚一次随机停顿
        #     # 等待搜索结果出来
        #     page.wait_for_selector("a")
        #
        #     # 随机点击一个搜索结果
        #     links = page.query_selector_all("a")
        #     valid_links = [link for link in links if "/search?q=" not in (link.get_attribute("href") or "")]
        #
        #     if valid_links:
        #         link = random.choice(valid_links)
        #         print("点击一个搜索结果...")
        #         link.scroll_into_view_if_needed()
        #         time.sleep(random.uniform(0.5, 1.5))
        #         link.click()
        #         page.wait_for_load_state("networkidle")
        #         time.sleep(random.uniform(3, 6))  # 模拟浏览网页
        #         page.go_back()


#
    # # 3-6 模拟用户滚动行为
    # for _ in range(random.randint(2, 4)):
    #     scroll_amount = random.randint(600, 1200)
    #     page.mouse.wheel(0, scroll_amount)
    #     time.sleep(random.uniform(1.5, 2.5))
    #
    # # 3-7 模拟点击一个搜索结果（约 70% 概率）
    # if random.random() < 0.7:
    #     try:
    #         page.wait_for_selector("a", timeout=5000)
    #         links = page.query_selector_all("a")
    #         valid_links = [link for link in links if "/search?q=" not in (link.get_attribute("href") or "")]
    #
    #         if valid_links:
    #             link = random.choice(valid_links)
    #             print("点击一个搜索结果...")
    #             link.scroll_into_view_if_needed()
    #             time.sleep(random.uniform(0.5, 1.5))
    #             link.click()
    #             page.wait_for_load_state("networkidle")
    #             time.sleep(random.uniform(3, 6))
    #             page.go_back()
    #     except Exception as e:
    #         print("未能点击搜索结果:", e)


# 2. 创建浏览器上下文
#    storage_state 复用已保存的登录态（bing_user.json）
#    user_agent 伪装成常见 Windows 桌面浏览器
# context = browser.new_context(
#     storage_state="bing_user.json",
#     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                "AppleWebKit/537.36 (KHTML, like Gecko) "
#                "Chrome/114.0.0.0 Safari/537.36"
# )

# 1. 启动浏览器（headless=False 可见模式，方便调试）
    # browser = p.chromium.launch(headless=False)
    # browser = p.chromium.launch(headless=False, args=[
    #     "--disable-blink-features=AutomationControlled"
    # ])
    #
    # context = browser.new_context(
    #     storage_state="bing_user.json",
    #     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    #                "AppleWebKit/537.36 (KHTML, like Gecko) "
    #                "Chrome/114.0.0.0 Safari/537.36",
    #     locale="en-US",
    #     color_scheme="light",
    #     viewport={"width": 1280, "height": 720},
    #     proxy={
    #         "server":"http://127.0.0.1:7890"
    #     }
    # )
    # # 👉 添加伪装脚本（防止被检测）
    # context.add_init_script("""
    # Object.defineProperty(navigator, 'webdriver', {
    #   get: () => undefined
    # });
    # window.navigator.chrome = {
    #   runtime: {}
    # };
    # Object.defineProperty(navigator, 'languages', {
    #   get: () => ['en-US', 'en']
    # });
    # Object.defineProperty(navigator, 'plugins', {
    #   get: () => [1, 2, 3, 4, 5]
    # });
    # """)