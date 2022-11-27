from flask_socketio import SocketIO
from . __version__ import __version__

socketio = SocketIO(cors_allowed_origins="*")
