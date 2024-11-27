import time
from webdriver_wrappers.chrome import ChromeWebDriverWrapper


def main() -> None:
    with ChromeWebDriverWrapper(
        headless=True,
        incognito=True,
        optimization=True,
        prefs=True,
        disable_selenium_logs=True,
        disable_automation_control=True,
        webdriver_type="chrome",
    ) as driver:
        driver.get("https://python.org")
        time.sleep(20)
        driver.save_screenshot("./example.png")


if __name__ == "__main__":
    main()
