from wsgidav.wsgidav_app import WsgiDAVApp
from cheroot import wsgi
import os

if not os.path.exists("uploads"):
    os.makedirs("uploads")

config = {
    "host": "0.0.0.0",
    "port": 8081,
    "provider_mapping": {"/": "./uploads"},
    "simple_dc": {"user_mapping": {"*": True}},  # No auth
    "verbose": 1,
    "logging": {"enable_loggers": []},
}

app = WsgiDAVApp(config)
server = wsgi.Server(bind_addr=(config["host"], config["port"]), wsgi_app=app)
print("WebDAV server running on http://0.0.0.0:8081/")
server.start()
