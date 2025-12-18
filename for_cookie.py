from playwright.sync_api import sync_playwright
import random,time

# 替换为你的微软账号和密码（注意：不要暴露真实信息）
USERNAME = "name"
PASSWORD = "password"

def human_type(page, selector, text, min_delay, max_delay):
    for char in text:
        page.click(selector)  # 确保聚焦在输入框
        page.keyboard.type(char)  # 输入一个字符
        page.wait_for_timeout(random.randint(min_delay, max_delay))  # 随机延迟


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
        storage_state=None,  # 不加载历史登录态
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

    page = context.new_page()

    # 打开微软登录页面
    page.goto("https://login.live.com")
    duration0 = random.uniform(0.2, 2.5)
    time.sleep(duration0)
    # 模拟用户滑动页面
    page.mouse.wheel(0, random.randint(300, 800))
    page.wait_for_timeout(random.randint(300, 900))

    # 输入账号
    # page.fill('input[name="loginfmt"]', USERNAME)
    # page.click('input[type="submit"]')
    # page.fill('#usernameEntry', USERNAME)
    # 使用我们自定义的逐字输入函数
    human_type(page, '#usernameEntry', USERNAME, min_delay=80, max_delay=160)
    # page.click('input[type="submit"]')  # 点击“下一步”按钮
    duration1 = random.uniform(2.0, 5.5)
    time.sleep(duration1)
    page.click('button[data-testid="primaryButton"]')
    # page.wait_for_selector('#passwordInput')  # 等待密码框加载
    # input('等待下一步')
    # 输入密码

    page.wait_for_selector('#passwordEntry')
    duration2 = random.uniform(0.2, 2.5)
    time.sleep(duration2)
    # page.fill('#passwordEntry', PASSWORD)
    # 使用我们自定义的逐字输入函数
    human_type(page, '#passwordEntry',PASSWORD, min_delay=90, max_delay=200)
    # 在 1.0 到 5.5 秒之间随机停
    # 模拟用户滑动页面
    page.mouse.wheel(0, random.randint(300, 800))
    page.wait_for_timeout(random.randint(300, 900))

    duration3 = random.uniform(1.0, 5.5)
    time.sleep(duration3)
    page.click('button[data-testid="primaryButton"]')

    # # 等待密码页加载
    # page.wait_for_selector('input[name="passwd"]')
    # page.fill('input[name="passwd"]', PASSWORD)
    # page.click('input[type="submit"]')


    try:
        # 等待“保持登录状态？”页面，并点击“是”或“否”
        page.wait_for_selector('button[data-testid="secondaryButton"]', timeout=5000)
        duration4 = random.uniform(2.0, 5.5)
        time.sleep(duration4)
        page.click('button[data-testid="secondaryButton"]')
        # page.wait_for_selector('input[id="idBtn_Back"]', timeout=5000)
        # page.click('input[id="idBtn_Back"]')  # 点击“否”，你也可以选择点“是”按钮 id 是 idSIButton9
    except:
        pass  # 没弹出就跳过

    # 等待跳转完成（可根据实际情况设置）
    page.wait_for_timeout(5000)

    # 保存登录状态
    context.storage_state(path="bing_user.json")
    print(">>> 登录状态已保存为 bing_user.json")

    browser.close()
    duration = random.uniform(1.0, 5.5)
    time.sleep(duration)