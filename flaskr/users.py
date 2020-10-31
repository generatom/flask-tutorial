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
        'SELECT id, username, admin FROM user'
    ).fetchall()
    return render_template('users/list.html', users=users)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(id):
    user = get_user(id)

    if request.method == 'POST':
        username = request.form['username']
        admin = int(request.form['admin'])
        db = get_db()
        username_new = (username != user['username'])
        username_exists = db.execute('SELECT id FROM user WHERE username = ?',
                                     (username,)).fetchone() is not None
        error = None
        query = None
        if username_new:
            if username_exists:
                error = 'Username exists.'
            else:
                db.execute(
                    'UPDATE user SET username = ?, admin = ? WHERE id = ?',
                    (username, admin, id)
                )
        else:
            db.execute(
                'UPDATE user SET admin = ? WHERE id = ?', (admin, id)
            )

        if error:
            flash(error)
        else:
            db.commit()
            return redirect(url_for('users.list'))

    return render_template('users/edit.html', user=user)


def get_user(id):
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (id,)).fetchone()
    return user
