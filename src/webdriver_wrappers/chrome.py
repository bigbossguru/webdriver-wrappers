import os
import platform
import subprocess
from pathlib import Path
from typing import Literal

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.core.os_manager import ChromeType


class ChromeWebDriverWrapper:
    def __init__(
        self,
        headless: bool = False,
        incognito: bool = False,
        userdata_dir: str | Path | None = None,
        agent: str | None = None,
        optimization: bool = False,
        prefs: bool = False,
        disable_selenium_logs: bool = False,
        extra_arguments: list[str] | None = None,
        extra_options: list[tuple] | None = None,
        disable_automation_control: bool = False,
        debugger_address: str | None = None,
        webdriver_type: Literal["chrome", "chromium"] = "chrome",
    ) -> None:
        self.driver = None
        self.disable_log = disable_selenium_logs
        self.webdriver_type = webdriver_type
        self.options = webdriver.ChromeOptions()

        if debugger_address:
            self.options.debugger_address = debugger_address
            # return None

        if headless:
            self.options.add_argument("--headless=new")

        if incognito:
            self.options.add_argument("--incognito")

        if optimization:
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--disable-extensions")
            self.options.add_argument("--disable-dev-shm-usage")
            self.options.add_argument("--ignore-certificate-errors")
            self.options.add_argument("--disable-application-cache")
            self.options.add_argument("--disable-plugins")
            self.options.add_argument("--disable-translate")
            self.options.add_argument("--disable-notifications")
            self.options.add_argument("--disable-crash-reporter")
            self.options.add_argument("--disable-webrtc")
            self.options.add_argument("--disable-blink-features=WebRTC")
            self.options.add_argument("--disable-software-rasterizer")
            self.options.add_argument("--disable-webgl")
            self.options.add_argument("--disable-background-timer-throttling")
            self.options.add_argument("--disable-backgrounding-occluded-windows")
            self.options.add_argument("--disable-client-side-phishing-detection")
            self.options.add_argument("--disable-oopr-debug-crash-dump")
            self.options.add_argument("--no-crash-upload")
            self.options.add_argument("--disable-low-res-tiling")
            self.options.add_argument("--disable-default-apps")
            self.options.add_argument("--disable-dev-tools")
            self.options.add_argument("--disable-site-isolation-trials")


        if platform.machine() == "aarch64":
            self.options.add_argument("--window-size=1920,1080")
        else:
            self.options.add_argument("--start-maximized")

        if prefs:
            self.options.add_experimental_option(
                "prefs",
                {
                    "profile.managed_default_content_settings.stylesheets": 2,
                    "profile.managed_default_content_settings.fonts": 2,
                },
            )

        if userdata_dir:
            if isinstance(userdata_dir, str):
                userdata_dir = Path(userdata_dir)

            userdata_dir.mkdir(exist_ok=True)
            self.options.add_argument(f"--user-data-dir={str(userdata_dir)}")

        fake_user_agent = UserAgent(platforms="pc", browsers="chrome")
        user_agent = agent or fake_user_agent.random
        self.options.add_argument(f"--user-agent={user_agent}")

        if disable_automation_control:
            self.options.add_argument("--disable-blink-features=AutomationControlled")
            self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.options.add_experimental_option("useAutomationExtension", False)

        if extra_options:
            for option in extra_options:
                self.options.add_experimental_option(*option)

        if extra_arguments:
            for argument in extra_arguments:
                self.options.add_argument(argument)

    def _get_service(self) -> ChromeService:
        if platform.machine() == "aarch64":
            webdriver_dir = Path(__file__).resolve().parent / "_bin" / "chrome"
            webdriver_path = webdriver_dir / "chromedriver"
            chromedriver_path = os.environ.get("CHROMEDRIVER", str(webdriver_path))
            service = ChromeService(executable_path=chromedriver_path)
        else:
            if self.webdriver_type == "chromium":
                service = ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
            else:
                service = ChromeService(ChromeDriverManager().install())


        if self.disable_log and platform.system() == "Windows":
            service.creation_flags = subprocess.CREATE_NO_WINDOW

        return service

    def open_driver(self) -> webdriver.Chrome:
        self.driver = webdriver.Chrome(service=self._get_service(), options=self.options)
        return self.driver

    def close_driver(self) -> None:
        if self.driver:
            self.driver.close()
            self.driver.quit()

    def __enter__(self) -> webdriver.Chrome:
        return self.open_driver()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        return self.close_driver()
