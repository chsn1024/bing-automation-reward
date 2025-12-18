# 引入依赖
from playwright.sync_api import sync_playwright
import random, time

# 启动 Playwright 会话
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

    # 3. 新建页面（主标签页）
    page = context.new_page()

    # 4. 打开 Microsoft Rewards 任务中心
    page.goto("https://rewards.bing.com/")

    # 5. 等待任务卡片区域加载完成（mee-card 元素出现）
    page.wait_for_selector("mee-card", timeout=10000)
    # 鼠标在主页面随机移动
    for _ in range(random.randint(3, 6)):
        x, y = random.randint(0, 1200), random.randint(0, 700)
        page.mouse.move(x, y)
        time.sleep(random.uniform(0.3, 0.8))

    # 6. 模拟真实用户“向下滚动”浏览页面
    for i in range(5):
        page.mouse.wheel(0, 1000)  # 垂直滚动 1000 像素
        time.sleep(1)              # 每次滚动停顿 1 秒，避免过快

    # 7. 获取所有可点击的任务卡片（排除已禁用 ng-disabled='true' 的卡片）
    cards = page.query_selector_all("mee-card:not([ng-disabled='true'])")

    # 8. 只处理前 3 张卡片（可根据需要调整）
    for card in cards[:3]:
        card.hover()
        time.sleep(random.uniform(0.5, 1.0))
        try:
            # 9. 点击卡片 → 触发新标签页打开
            #    expect_page() 会在后台监听新页面事件
            with context.expect_page() as new_page_info:
                card.click()                         # 执行点击

            # 10. 获取新打开的标签页对象
            new_page = new_page_info.value

            # 11. 等待新页面完全加载
            new_page.wait_for_load_state()
            duration = random.uniform(0.3,1.5)
            time.sleep(duration)
            # 鼠标在主页面随机移动
            for _ in range(random.randint(3, 6)):
                x, y = random.randint(0, 1200), random.randint(0, 700)
                new_page.mouse.move(x, y)
                time.sleep(random.uniform(0.3, 0.8))
            # 12. 在新页面内模拟“真实用户滚动”行为
            for _ in range(random.randint(2, 4)):    # 随机滚动 2~4 次
                scroll_amount = random.randint(600, 1200)
                new_page.mouse.wheel(0, scroll_amount)
                time.sleep(random.uniform(1.5, 2.5)) # 随机停顿，降低机器人特征

            # 13. 打印新页面 URL（调试用）
            print("新页面 URL：", new_page.url)

            # 14. 切回主标签页并聚焦，防止后续定位错乱
            page.bring_to_front()
            time.sleep(random.uniform(1.5, 2.5))
            # 15. 关闭新标签页，保持窗口整洁
            new_page.close()
            time.sleep(random.uniform(0.5, 1.5))

        except Exception as e:
            # 16. 若卡片无法点击或出现其他异常，跳过并打印信息
            print("跳过一个无法点击的卡片", e)

    # 17. 所有任务完成后，等待人工确认（防止浏览器自动关闭）
    print('今日任务已完成，正在关闭页面；')

    # 18. 关闭浏览器
    browser.close()