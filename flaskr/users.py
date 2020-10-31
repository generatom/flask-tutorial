from flask import Blueprint, flash, g, render_template, request, url_for
from flask import redirect
from werkzeug.exceptions import abort
from flaskr.db import get_db
from flaskr.auth import login_required


bp = Blueprint('users', __name__, url_prefix='/users')
