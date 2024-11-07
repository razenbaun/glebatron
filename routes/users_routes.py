from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import User, db

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@users_bp.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        phone_number = request.form['phone_number']
        fio = request.form['fio']

        new_user = User(
            email=email,
            phone_number=phone_number,
            fio=fio
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Пользователь успешно добавлен!', 'success')
        return redirect(url_for('users.get_users'))

    return render_template('add_user.html')


@users_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        user.fio = request.form['fio']

        db.session.commit()
        flash('Данные пользователя успешно обновлены!', 'success')
        return redirect(url_for('users.get_users'))

    return render_template('edit_user.html', user=user)


@users_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash('Пользователь успешно удалён!', 'success')
    return redirect(url_for('users.get_users'))
