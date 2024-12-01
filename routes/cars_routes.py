from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import Car, Organization, Rate, db
from sqlalchemy import or_, cast, String

cars_bp = Blueprint('cars', __name__)


@cars_bp.route('/cars', methods=['GET'])
def get_cars():
    search_query = request.args.get('q', '')
    status_filter = request.args.get('status', '')
    organization_filter = request.args.get('organization', type=int)
    rate_filter = request.args.get('rate', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 5

    query = Car.query

    if search_query:
        query = query.filter(
            or_(
                Car.model.ilike(f'%{search_query}%'),
                cast(Car.year, String).ilike(f'%{search_query}%')
            )
        )

    if organization_filter:
        query = query.filter(Car.organization_id == organization_filter)

    if rate_filter:
        query = query.filter(Car.rate_id == rate_filter)

    cars = query.paginate(page=page, per_page=per_page)

    organizations = Organization.query.all()
    rates = Rate.query.all()

    return render_template(
        'cars.html',
        cars=cars,
        search_query=search_query,
        organization_filter=organization_filter,
        rate_filter=rate_filter,
        organizations=organizations,
        rates=rates
    )


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
