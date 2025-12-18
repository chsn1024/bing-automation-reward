# 引入依赖
from playwright.sync_api import sync_playwright
import random, time

# 1. 读取关键词文件
#    keywords.txt 每行一个关键词，自动去掉空行和首尾空格
with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f if line.strip()]

# 2. 启动 Playwright
with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        args=[
            # 去掉自动化特征
            "--disable-blink-features=AutomationControlled",
            # 禁用 GPU，避免某些设备提示「正在受自动化工具控制」
            "--disable-gpu",
            # 禁用信息栏提示
            "--disable-infobars",
            # 禁用扩展
            "--disable-extensions",
        ]
    )

    context = browser.new_context(
        storage_state="bing_user.json",  # 加载登录历史
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        locale="en-US,en",  # 语言环境
        color_scheme="light",  # 浅色主题
        viewport={"width": 1280, "height": 720},
        permissions=[],  # 拒绝任何权限请求
        geolocation={"latitude": 0, "longitude": 0},  # 伪造地理位置
        # 如不需要代理，删除下面 proxy 参数即可
        # proxy={"server": "http://127.0.0.1:7890"}
    )

    # 注入高级伪装脚本
    context.add_init_script("""
                // 1. 去掉 webdriver 痕迹
                delete navigator.__proto__.webdriver;

                // 2. 伪装 plugins
                function mockPlugins() {
                    const pluginData = [
                        { name: "Chrome PDF Plugin", description: "Portable Document Format" },
                        { name: "Chrome PDF Viewer", description: "" },
                        { name: "Native Client", description: "" }
                    ];
                    const plugins = pluginData.map(p => {
                        const mimetypes = [{ type: "application/pdf", suffixes: "pdf" }];
                        const plugin = new Plugin(p.name, p.description, "internal-pdf-viewer");
                        mimetypes.forEach(mt => {
                            const mime = new MimeType(mt.type, mt.suffixes, p.name);
                            plugin[mt.type] = mime;
                        });
                        return plugin;
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => plugins
                    });
                }
                mockPlugins();

                // 3. 伪装 languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ["en-US", "en"]
                });

                // 4. 伪装 permissions
                const originalQuery = navigator.permissions.query;
                navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications'
                        ? Promise.resolve({ state: Notification.permission })
                        : originalQuery(parameters)
                );

                // 5. 伪装 chrome.runtime
                window.chrome = {
                    runtime: {
                        lastError: null,
                        sendMessage: () => {},
                        onMessage: { addListener: () => {} }
                    }
                };
            """)

    # 2-3 新建页面
    # page = context.new_page()
    # 2-3 新建页面
    page = context.new_page()



    # 2-4 首次打开 Bing
    page.goto("https://www.bing.com")
    # 等待 DOM 和网络空闲，确保页面渲染完毕
    page.wait_for_load_state("load")
    page.wait_for_load_state("domcontentloaded")

    # 3. 主循环：随机搜索关键词
    for i in range(10):
        # 3-1 随机选一个关键词并拼接随机数，降低重复率
        query = random.choice(keywords) + str(random.randint(1, 1000))
        print(f"[{i+1}/10] Searching: {query}")

        # 3-2 重新回到主页，防止残留状态
        # page.goto("https://www.bing.com/")
        # 等待搜索框加载
        page.wait_for_selector("textarea[name='q']", timeout=10000)
        time.sleep(random.uniform(1.5, 2.5))
        # 3-3 清空并输入搜索词
        page.click("textarea[name='q']")
        page.fill("textarea[name='q']", "")                      # 先清空
        # page.keyboard.type(query, delay=random.randint(50, 150)) # 模拟人工输入
        for char in query:
            page.keyboard.type(char)
            time.sleep(random.uniform(0.05, 0.2))  # 每个字符之间停顿

        duration = random.uniform(1.0,3.5)
        time.sleep(duration)
        # 3-4 回车触发搜索
        page.keyboard.press("Enter")

        # 3-5 等待网络空闲（页面加载完毕）
        page.wait_for_load_state("networkidle")


        # 3-6 模拟用户滚动行为
        for _ in range(random.randint(2, 4)):
            scroll_amount = random.randint(600, 1200)
            page.mouse.wheel(0, scroll_amount)
            time.sleep(random.uniform(1.5, 2.5))

        # 3-7 模拟点击一个搜索结果（约 70% 概率）
        if random.random() < 0.7:
            try:
                page.wait_for_selector("a", timeout=5000)
                links = page.query_selector_all("a")
                valid_links = [link for link in links if "/search?q=" not in (link.get_attribute("href") or "")]

                if valid_links:
                    link = random.choice(valid_links)
                    link.hover()
                    print("点击一个搜索结果...")
                    link.scroll_into_view_if_needed()
                    time.sleep(random.uniform(0.5, 1.5))
                    page.evaluate("""
                      Array.from(document.querySelectorAll("a[target='_blank']")).forEach(a => a.removeAttribute('target'));
                    """)
                    link.click()
                    page.wait_for_load_state("networkidle")
                    time.sleep(random.uniform(3, 6))
                    page.go_back()
            except Exception as e:
                print("未能点击搜索结果:", e)

        time.sleep(random.uniform(0.5, 1.5))
        page.go_back()


    # 4. 全部完成后关闭浏览器
    browser.close()