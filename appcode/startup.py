import subprocess
import secrets
import pathlib
from config import Constants
from appcode import crypto

def startServer():

    # Sets the Serveo domain
    serveoDomain = Constants.get("serveo-domain", "p")
    address = serveoDomain + ":80:192.168.0.14:5000"

    # Sets the SSH command
    command = [
        "ssh",
        "-i", "serveo-key",
        "-R", address,
        "serveo.net"
    ]

    # Launches the SSH command in pseudo-terminal
    try:
        subprocess.Popen(command)
    except subprocess.CalledProcessError as err:
        print(err)

def checkConfig():

    # Checks if the config file exists and creates it if not
    if (not pathlib.Path('config-public.json').is_file()):
        open("config-public.json", "w").close()

    # Checks if the secrets file exists and creates it if not
    if (not pathlib.Path('config-secrets.json').is_file()):
        open("config-secrets.json", "w").close()

    # Checks if the basic config exists and creates it if not
    setFilePath()

    if (Constants.get('serveo-domain', "p") is None):
        setServeoDomain()

    if (Constants.get('API_TOKEN', "s") is None):
        setValidationToken()

    if (Constants.get('SECRET_TOKEN', "s") is None):
        crypto.setSecretToken()

def setFilePath():
    filePath = pathlib.Path().resolve()
    Constants.write("file-path", str(filePath), "p")

def setValidationToken():
    validationToken = secrets.token_urlsafe(32)[:32]
    Constants.write("API_TOKEN", validationToken, "s")

def setServeoDomain():
    serveoDomain = secrets.token_urlsafe(32)[:32]
    Constants.write("serveo-domain", serveoDomain, "p")
