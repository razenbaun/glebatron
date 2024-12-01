from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from models.model import db, Deal, Car, Rate, User
from sqlalchemy import or_

deals_bp = Blueprint('deals', __name__)


@deals_bp.route('/deals', methods=['GET'])
def get_deals():
    search_query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    deals = Deal.query.join(Car).join(Rate).join(User).filter(
        or_(
            Car.model.ilike(f'%{search_query}%'),
            User.fio.ilike(f'%{search_query}%'),
            Rate.type.ilike(f'%{search_query}%')
        )
    ).paginate(page=page, per_page=per_page)

    return render_template('deals.html', deals=deals, search_query=search_query)


@deals_bp.route('/deals/add', methods=['GET', 'POST'])
def add_deal():
    if request.method == 'POST':
        car_id = request.form['car_id']
        rate_id = request.form['rate_id']
        user_id = request.form['user_id']

        new_deal = Deal(
            car_id=car_id,
            rate_id=rate_id,
            user_id=user_id,
            start_time=datetime.now()
        )
        db.session.add(new_deal)
        db.session.commit()
        flash('Сделка успешно добавлена!', 'success')
        return redirect(url_for('deals.get_deals'))

    cars = Car.query.all()
    rates = Rate.query.all()
    users = User.query.all()
    return render_template('add_deal.html', cars=cars, rates=rates, users=users)


@deals_bp.route('/deals/edit/<int:deal_id>', methods=['GET', 'POST'])
def edit_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)

    if request.method == 'POST':
        deal.car_id = request.form['car_id']
        deal.rate_id = request.form['rate_id']
        deal.user_id = request.form['user_id']

        db.session.commit()
        flash('Сделка успешно изменена!', 'success')
        return redirect(url_for('deals.get_deals'))

    cars = Car.query.all()
    rates = Rate.query.all()
    users = User.query.all()
    return render_template('edit_deal.html', deal=deal, cars=cars, rates=rates, users=users)


@deals_bp.route('/deals/close/<int:deal_id>', methods=['POST'])
def close_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    deal.end_time = datetime.now()  # Закрываем сделку, ставя текущее время
    db.session.commit()
    flash('Сделка успешно закрыта!', 'success')
    return redirect(url_for('deals.get_deals'))


@deals_bp.route('/deals/delete/<int:deal_id>', methods=['POST'])
def delete_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    db.session.delete(deal)
    db.session.commit()
    flash('Сделка успешно удалена!', 'success')
    return redirect(url_for('deals.get_deals'))
