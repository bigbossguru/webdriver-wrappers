import os
import platform
from pathlib import Path

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class FirefoxWebDriverWrapper:
    def __init__(
        self,
        headless: bool = False,
        incognito: bool = False,
        optimization: bool = False,
        agent: str | None = None,
        extra_arguments: list[str] | None = None,
        extra_options: list[tuple] | None = None,
    ) -> None:
        self.driver = None
        self.headless = headless
        self.options = webdriver.FirefoxOptions()

        if self.headless:
            self.options.add_argument("--headless")
            self.options.add_argument("--width=1920")
            self.options.add_argument("--height=1080")
    
        if incognito:
            self.options.add_argument("-private")

        if optimization:
            # Disable unnecessary features to improve performance
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--disable-extensions")
            self.options.set_preference("layers.acceleration.disabled", True)
            self.options.set_preference("webgl.disabled", True)
            self.options.set_preference("browser.safebrowsing.enabled", False)
            self.options.set_preference("datareporting.policy.dataSubmissionEnabled", False)
            self.options.set_preference("app.update.auto", False)
            self.options.set_preference("app.update.enabled", False)
            self.options.set_preference("extensions.enabled", False)
            self.options.set_preference("dom.webnotifications.enabled", False)
            self.options.set_preference("accessibility.enabled", False)
            self.options.set_preference("media.peerconnection.enabled", False)
            self.options.set_preference("gfx.font_rendering.directwrite.enabled", False)
            self.options.set_preference("browser.cache.disk.enable", False)
            self.options.set_preference("browser.cache.memory.enable", False)
            self.options.set_preference("network.http.connection.timeout", 30)
            self.options.set_preference("network.http.speculative-parallel-limit", 0)
            self.options.set_preference("browser.animation.enabled", False)
            self.options.set_preference("javascript.options.mem.gc_logging", False)

        fake_user_agent = UserAgent(platforms="pc", browsers="chrome")
        user_agent = agent or fake_user_agent.random
        self.options.set_preference("general.useragent.override", user_agent)

        if extra_arguments:
            for argument in extra_arguments:
                self.options.add_argument(argument)
        
        if extra_options:
            for option in extra_options:
                self.options.set_preference(*option)

    @staticmethod
    def _get_service() -> FirefoxService:
        if platform.machine() == "aarch64":
            webdriver_dir = Path(__file__).resolve().parent / "_bin" / "firefox"
            webdriver_path = webdriver_dir / "geckodriver"
            firefoxdriver_path = os.getenv("FIREFOXDRIVER", str(webdriver_path))
            return FirefoxService(executable_path=firefoxdriver_path)
        else:
            return FirefoxService(GeckoDriverManager().install())

    def open_driver(self) -> webdriver.Firefox:
        self.driver = webdriver.Firefox(
            service=self._get_service(), options=self.options
        )
        if not self.headless:
            self.driver.maximize_window()
        return self.driver

    def close_driver(self) -> None:
        if self.driver:
            self.driver.close()
            self.driver.quit()

    def __enter__(self) -> webdriver.Firefox:
        return self.open_driver()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        return self.close_driver()
