from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import db, Deal, Car, Rate, Organization, User

deals_bp = Blueprint('deals', __name__)


@deals_bp.route('/deals', methods=['GET'])
def get_deals():
    deals = Deal.query.all()
    return render_template('deals.html', deals=deals)


@deals_bp.route('/deals/add', methods=['GET', 'POST'])
def add_deal():
    if request.method == 'POST':
        car_id = request.form['car_id']
        rate_id = request.form['rate_id']
        organization_id = request.form['organization_id']
        user_id = request.form['user_id']

        new_deal = Deal(
            car_id=car_id,
            rate_id=rate_id,
            organization_id=organization_id,
            user_id=user_id
        )

        db.session.add(new_deal)
        db.session.commit()
        flash('Сделка успешно создана!', 'success')
        return redirect(url_for('deals.get_deals'))

    cars = Car.query.all()
    rates = Rate.query.all()
    organizations = Organization.query.all()
    users = User.query.all()

    return render_template('add_deal.html', cars=cars, rates=rates, organizations=organizations, users=users)


@deals_bp.route('/deals/edit/<int:deal_id>', methods=['GET', 'POST'])
def edit_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)

    if request.method == 'POST':
        if request.form.get('close_deal') == 'close':
            deal.close_deal()
            flash('Сделка успешно закрыта!', 'success')
        db.session.commit()
        return redirect(url_for('deals.get_deals'))

    return render_template('edit_deal.html', deal=deal)


@deals_bp.route('/deals/delete/<int:deal_id>', methods=['POST'])
def delete_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    db.session.delete(deal)
    db.session.commit()

    flash('Сделка успешно удалена!', 'success')
    return redirect(url_for('deals.get_deals'))


@deals_bp.route('/deals/close/<int:deal_id>', methods=['POST'])
def close_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)

    if not deal.end_time:
        deal.end_time = datetime.utcnow()
        db.session.commit()
        flash('Сделка успешно закрыта!', 'success')
    else:
        flash('Сделка уже была закрыта!', 'warning')

    return redirect(url_for('deals.get_deals'))
