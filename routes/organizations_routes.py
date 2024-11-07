from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import Organization, Location, db

organizations_bp = Blueprint('organizations', __name__)


@organizations_bp.route('/organizations', methods=['GET'])
def get_organizations():
    organizations = Organization.query.all()
    return render_template('organizations.html', organizations=organizations)


@organizations_bp.route('/organizations/edit/<int:organization_id>', methods=['GET', 'POST'])
def edit_organization(organization_id):
    organization = Organization.query.get_or_404(organization_id)
    locations = Location.query.all()  # Предполагаем, что есть связи с локациями

    if request.method == 'POST':
        organization.organization_name = request.form['organization_name']
        organization.phone_number = request.form['phone_number']
        organization.fio_director = request.form['fio_director']
        organization.location_id = request.form['location_id']

        db.session.commit()
        flash('Организация успешно изменена!', 'success')
        return redirect(url_for('organizations.get_organizations'))

    return render_template('edit_organization.html', organization=organization, locations=locations)


@organizations_bp.route('/organizations/delete/<int:organization_id>', methods=['POST'])
def delete_organization(organization_id):
    organization = Organization.query.get_or_404(organization_id)
    db.session.delete(organization)
    db.session.commit()
    flash('Организация успешно удалена!', 'success')
    return redirect(url_for('organizations.get_organizations'))


@organizations_bp.route('/organizations/add', methods=['GET', 'POST'])
def add_organization():
    locations = Location.query.all()

    if request.method == 'POST':
        organization_name = request.form['organization_name']
        phone_number = request.form['phone_number']
        fio_director = request.form['fio_director']
        location_id = request.form['location_id']

        new_organization = Organization(
            organization_name=organization_name,
            phone_number=phone_number,
            fio_director=fio_director,
            location_id=location_id
        )

        db.session.add(new_organization)
        db.session.commit()

        flash('Организация успешно добавлена!', 'success')
        return redirect(url_for('organizations.get_organizations'))

    return render_template('add_organization.html', locations=locations)
