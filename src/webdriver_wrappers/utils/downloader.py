from pathlib import Path

from webdriver_wrappers.utils.versions import get_chromium_version


PATH_BIN_CHROMEDRIVER_DIR = Path(__file__).resolve().parent.parent / "_bin" / "chrome"

def aarch64_webdriver_downloader() -> None:
    print(get_chromium_version())
