from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import User, db
from datetime import datetime

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@users_bp.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        fio = request.form['fio']
        email = request.form['email']
        phone_number = request.form['phone_number']
        passport_number = request.form['passport_number']
        date_of_birth = request.form['date_of_birth']

        try:
            date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            flash("Неверный формат даты рождения", "danger")
            return render_template('add_user.html')

        new_user = User(
            fio=fio,
            email=email,
            phone_number=phone_number,
            passport_number=passport_number,
            date_of_birth=date_of_birth
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
        user.fio = request.form['fio']
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        user.passport_number = request.form['passport_number']

        date_of_birth = request.form['date_of_birth']
        try:
            user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            flash("Неверный формат даты рождения", "danger")
            return render_template('edit_user.html', user=user)

        db.session.commit()
        flash('Пользователь успешно изменен!', 'success')
        return redirect(url_for('users.get_users'))

    return render_template('edit_user.html', user=user)


@users_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь успешно удален!', 'success')
    return redirect(url_for('users.get_users'))
