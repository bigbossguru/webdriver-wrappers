import os
import platform
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverConnector:
    def __init__(
        self,
        headless: bool = True,
        incognito: bool = True,
        agent: str | None = None,
        optimization: bool = True,
    ) -> None:
        self.driver = None
        self.options = webdriver.ChromeOptions()

        if headless:
            self.options.add_argument("--headless")
        if incognito:
            self.options.add_argument("--incognito")

        if optimization:
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--disable-extensions")
            self.options.add_argument("--window-size=1920,1080")
            self.options.add_argument("--disable-dev-shm-usage")
            self.options.add_argument("--ignore-certificate-errors")
            self.options.add_argument("--enable-unsafe-swiftshader")
            self.options.add_argument("--disable-application-cache")
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.managed_default_content_settings.stylesheets": 2,
            }
            self.options.add_experimental_option("prefs", prefs)

        user_agent = (
            agent
            or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        self.options.add_argument(f"--user-agent={user_agent}")

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
