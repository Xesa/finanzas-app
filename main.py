import threading
from flask import Flask
from appcode.credentials import credentials_bp
import appcode.startup as startup

# Sets the app and Blueprints
app = Flask(__name__)
app.register_blueprint(credentials_bp)

if __name__ == '__main__':

    # Sets the config files
    startup.checkConfig()

    # Starts the server and the app
    ssh_thread = threading.Thread(target=startup.startServer())
    app_thread = threading.Thread(target=app.run(host='0.0.0.0', port=5000))

    ssh_thread.start()
    app_thread.start()

    # Waits until server shutdown
    ssh_thread.join()
    app_thread.join()