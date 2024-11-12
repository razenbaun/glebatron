from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import Car, Organization, Rate, db

cars_bp = Blueprint('cars', __name__)


@cars_bp.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)


@cars_bp.route('/cars/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        rate_id = request.form['rate_id']
        status = request.form['status']
        model = request.form['model']
        year = request.form['year']
        organization_id = request.form['organization_id']

        new_car = Car(rate_id=rate_id, status=status, model=model, year=year, organization_id=organization_id)
        db.session.add(new_car)
        db.session.commit()
        flash('Автомобиль успешно добавлен!', 'success')
        return redirect(url_for('cars.get_cars'))

    rates = Rate.query.all()
    organizations = Organization.query.all()
    return render_template('add_car.html', rates=rates, organizations=organizations)


@cars_bp.route('/cars/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    organizations = Organization.query.all()
    rates = Rate.query.all()

    if request.method == 'POST':
        car.organization_id = request.form['organization_id']
        car.rate_id = request.form['rate_id']
        car.model = request.form['model']
        car.year = request.form['year']
        car.status = request.form['status']

        db.session.commit()
        flash('Автомобиль успешно обновлен!', 'success')
        return redirect(url_for('cars.get_cars'))

    return render_template('edit_car.html', car=car, organizations=organizations, rates=rates)


@cars_bp.route('/cars/delete/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Автомобиль успешно удален!', 'success')
    return redirect(url_for('cars.get_cars'))
