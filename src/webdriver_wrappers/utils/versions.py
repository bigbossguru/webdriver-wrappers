import subprocess

from webdriver_wrappers.utils.exceptions import (
    ChromiumNotInstalledError,
    ChromiumVersionError,
)


def get_chromium_version() -> str:
    try:
        output = subprocess.check_output(
            ["chromium", "--version"], stderr=subprocess.STDOUT
        )
        version = output.decode().strip()
        return version
    except FileNotFoundError:
        raise ChromiumNotInstalledError("Chromium is not installed or not in PATH.")
    except subprocess.CalledProcessError as e:
        raise ChromiumVersionError(f"Error occurred: {e.output.decode().strip()}")
