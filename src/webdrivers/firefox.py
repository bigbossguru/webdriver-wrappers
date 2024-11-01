import os
import platform
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class WebDriverConnector:
    def __init__(
        self,
        headless: bool = True,
        incognito: bool = True,
        agent: str | None = None,
        optimization: bool = True,
    ) -> None:
        self.driver = None
        self.options = webdriver.FirefoxOptions()

        if headless:
            self.options.add_argument("--headless")
        if incognito:
            self.options.add_argument("--incognito")

        if optimization:
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--disable-extensions")
            self.options.add_argument("--window-size=1920,1080")

        user_agent = (
            agent
            or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        self.options.add_argument(f"--user-agent={user_agent}")

    @staticmethod
    def _get_firefox_service() -> FirefoxService:
        if platform.machine() == "aarch64":
            webdriver_dir = Path(__file__).resolve().parent / "_bin" / "firefox"
            webdriver_path = webdriver_dir / "geckodriver"
            firefoxdriver_path = os.getenv("FIREFOXDRIVER", str(webdriver_path))
            return FirefoxService(executable_path=firefoxdriver_path)
        else:
            return FirefoxService(GeckoDriverManager().install())

    def __enter__(self) -> webdriver.Firefox:
        self.driver = webdriver.Firefox(
            service=self._get_firefox_service(), options=self.options
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.driver:
            self.driver.close()
            self.driver.quit()
