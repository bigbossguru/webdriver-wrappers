class UnsupportedFileFormatError(Exception):
    """Custom exception for unsupported file formats."""

    pass


class ChromiumNotInstalledError(Exception):
    """Raised when Chromium is not installed or not in the PATH."""

    pass


class ChromiumVersionError(Exception):
    """Raised when there is an error obtaining the Chromium version."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
