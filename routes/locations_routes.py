from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import Location, db

locations_bp = Blueprint('locations', __name__)


@locations_bp.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)


@locations_bp.route('/locations/edit/<int:location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)

    if request.method == 'POST':
        location.address = request.form['address']
        location.city = request.form['city']

        db.session.commit()
        flash('Локация успешно обновлена!', 'success')
        return redirect(url_for('locations.get_locations'))

    return render_template('edit_location.html', location=location)


@locations_bp.route('/locations/delete/<int:location_id>', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Локация успешно удалена!', 'success')
    return redirect(url_for('locations.get_locations'))


@locations_bp.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        address = request.form['address']
        city = request.form['city']

        new_location = Location(address=address, city=city)
        db.session.add(new_location)
        db.session.commit()
        flash('Локация успешно добавлена!', 'success')
        return redirect(url_for('locations.get_locations'))

    return render_template('add_location.html')
