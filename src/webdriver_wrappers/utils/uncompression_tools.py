import zipfile
import tarfile
from pathlib import Path

from webdriver_wrappers.utils.exceptions import UnsupportedFileFormatError


def uncompression_webdrivers(webdriver_dir: Path) -> None:
    if (webdriver_dir / "chromedriver").exists() or (
        webdriver_dir / "geckodriver"
    ).exists():
        return None

    filespaths = list(webdriver_dir.glob("*.zip"))
    filespaths.extend(list(webdriver_dir.glob("*.tar.gz")))
    filespaths.extend(list(webdriver_dir.glob("*.tgz")))

    filepath: Path = filespaths[0]

    if filepath.suffix == ".zip":
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(webdriver_dir)

    elif (
        filepath.suffix == ".tar.gz"
        or filepath.suffix == ".tgz"
        or filepath.suffix == ".gz"
    ):
        with tarfile.open(filepath, "r:gz") as tar_ref:
            tar_ref.extractall(webdriver_dir)

    else:
        raise UnsupportedFileFormatError(
            f"Unsupported file format: {filepath}. Please provide a .zip or .tar.gz file."
        )
