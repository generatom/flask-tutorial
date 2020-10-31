from flask import Blueprint, flash, g, render_template, request, url_for
from flask import redirect
from werkzeug.exceptions import abort
from flaskr.db import get_db
from flaskr.auth import admin_required


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
@admin_required
def list():
    db = get_db()
    users = db.execute(
        'SELECT username, admin FROM user'
    ).fetchall()
    return render_template('users/list.html', users=users)
