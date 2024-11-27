# webdrivers

## Install package

### Poetry

```
poetry add git+https://github.com/bigbossguru/webdriver-wrappers.git
```

### Pip

```
pip install git+https://github.com/bigbossguru/webdriver-wrappers.git
```

## Example

```
from webdriver_wrappers.chrome import ChromeWebDriverWrapper

def main() -> None:
    with ChromeWebDriverWrapper(headless=False, incognito=False, optimization=True) as driver:
        driver.get("https://python.org")
        driver.save_screenshot("./example.png")

if __name__ == "__main__":
    main()
```
