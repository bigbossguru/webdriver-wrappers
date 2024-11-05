import os
import platform
from pathlib import Path

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverConnector:
    def __init__(
        self,
        headless: bool = False,
        incognito: bool = False,
        optimization: bool = False,
        agent: str | None = None,
        userdata_dir: Path | None = None,
        prefs: bool = False,
    ) -> None:
        self.driver = None
        self.options = webdriver.ChromeOptions()

        if headless:
            self.options.add_argument("--headless")
        if incognito:
            self.options.add_argument("--incognito")

        if optimization or headless:
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--disable-extensions")
            self.options.add_argument("--disable-dev-shm-usage")
            self.options.add_argument("--ignore-certificate-errors")
            self.options.add_argument("--enable-unsafe-swiftshader")
            self.options.add_argument("--disable-application-cache")

        if platform.machine() == "aarch64":
            self.options.add_argument("--window-size=1920,1080")
        else:
            self.options.add_argument("--start-maximized")

        if prefs:
            self.options.add_experimental_option(
                "prefs",
                {
                    "profile.managed_default_content_settings.images": 2,
                    "profile.managed_default_content_settings.stylesheets": 2,
                    "profile.managed_default_content_settings.fonts": 2,
                },
            )

        if userdata_dir:
            self.options.add_argument(f"--user-data-dir={str(userdata_dir)}")

        fake_user_agent = UserAgent()
        user_agent = agent or fake_user_agent.random
        self.options.add_argument(f"--user-agent={user_agent}")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)

    @staticmethod
    def _get_chrome_service() -> ChromeService:
        if platform.machine() == "aarch64":
            webdriver_dir = Path(__file__).resolve().parent / "_bin" / "chrome"
            webdriver_path = webdriver_dir / "chromedriver"
            chromedriver_path = os.getenv("CHROMEDRIVER", str(webdriver_path))
            return ChromeService(executable_path=chromedriver_path)
        else:
            return ChromeService(ChromeDriverManager().install())

    def __enter__(self) -> webdriver.Chrome:
        self.driver = webdriver.Chrome(
            service=self._get_chrome_service(), options=self.options
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.driver:
            self.driver.close()
            self.driver.quit()
