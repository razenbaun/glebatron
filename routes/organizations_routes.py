from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import Organization, db

organization_bp = Blueprint('organizations', __name__)


@organization_bp.route('/organizations', methods=['GET'])
def get_organizations():
    organizations = Organization.query.all()
    return render_template('organizations.html', organizations=organizations)


@organization_bp.route('/organizations/add', methods=['GET', 'POST'])
def add_organization():
    if request.method == 'POST':
        organization_name = request.form['organization_name']
        phone_number = request.form['phone_number']
        fio_director = request.form['fio_director']
        address = request.form['address']
        city = request.form['city']

        new_organization = Organization(
            organization_name=organization_name,
            phone_number=phone_number,
            fio_director=fio_director,
            address=address,
            city=city
        )
        db.session.add(new_organization)
        db.session.commit()
        flash('Организация успешно добавлена!', 'success')
        return redirect(url_for('organizations.get_organizations'))

    return render_template('add_organization.html')


@organization_bp.route('/organizations/edit/<int:organization_id>', methods=['GET', 'POST'])
def edit_organization(organization_id):
    organization = Organization.query.get_or_404(organization_id)

    if request.method == 'POST':
        organization.organization_name = request.form['organization_name']
        organization.phone_number = request.form['phone_number']
        organization.fio_director = request.form['fio_director']
        organization.address = request.form['address']
        organization.city = request.form['city']

        db.session.commit()
        flash('Организация успешно обновлена!', 'success')
        return redirect(url_for('organizations.get_organizations'))

    return render_template('edit_organization.html', organization=organization)


@organization_bp.route('/organizations/delete/<int:organization_id>', methods=['POST'])
def delete_organization(organization_id):
    organization = Organization.query.get_or_404(organization_id)
    db.session.delete(organization)
    db.session.commit()
    flash('Организация успешно удалена!', 'success')
    return redirect(url_for('organizations.get_organizations'))
