"""
Routes and sub-resources for the /terminal resource
"""
from flask import Blueprint, jsonify, request, session, current_app
from flask_socketio import emit, join_room, leave_room
import os
from ... import socketio
from csle_rest_api.rest_api import socketio
import pty
import struct
import fcntl
import subprocess
import termios
import select
import shlex
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants

# Creates a blueprint "sub application" of the main REST app
shell_socket_bp = Blueprint(
    api_constants.MGMT_WEBAPP.TERMINAL_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.TERMINAL_RESOURCE}")


