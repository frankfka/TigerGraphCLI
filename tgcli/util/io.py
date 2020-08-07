import pathlib

# Directories
APP_DIR = pathlib.Path.home() / ".tgcli"

# Files
CONFIG_FILENAME = "config"
CONFIG_FILEPATH = APP_DIR / CONFIG_FILENAME
CREDENTIALS_FILENAME = "credentials"
CREDENTIALS_FILEPATH = APP_DIR / CREDENTIALS_FILENAME
