from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import Car, Rate, db

cars_bp = Blueprint('cars', __name__)


@cars_bp.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)


@cars_bp.route('/cars/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        model = request.form['model']
        year = request.form['year']
        rate_id = request.form['rate_id']
        status = request.form['status']

        new_car = Car(
            model=model,
            year=year,
            rate_id=rate_id,
            status=status
        )

        db.session.add(new_car)
        db.session.commit()

        flash('Автомобиль успешно добавлен!', 'success')
        return redirect(url_for('cars.get_cars'))

    rates = Rate.query.all()
    return render_template('add_car.html', rates=rates)


@cars_bp.route('/cars/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)

    if request.method == 'POST':
        car.model = request.form['model']
        car.year = request.form['year']
        car.rate_id = request.form['rate_id']
        car.status = request.form['status']

        db.session.commit()
        flash('Автомобиль успешно обновлен!', 'success')
        return redirect(url_for('cars.get_cars'))

    rates = Rate.query.all()
    return render_template('edit_car.html', car=car, rates=rates)


@cars_bp.route('/cars/delete/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()

    flash('Автомобиль успешно удален!', 'success')
    return redirect(url_for('cars.get_cars'))
