from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import Rate, db
from sqlalchemy import or_

rates_bp = Blueprint('rates', __name__)


@rates_bp.route('/rates', methods=['GET'])
def get_rates():
    search_query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    rates = Rate.query.filter(
        or_(
            Rate.type.ilike(f'%{search_query}%'),
            Rate.amount.cast(db.String).ilike(f'%{search_query}%')
        )
    ).paginate(page=page, per_page=per_page)

    return render_template('rates.html', rates=rates, search_query=search_query)


@rates_bp.route('/rates/add', methods=['GET', 'POST'])
def add_rate():
    if request.method == 'POST':
        amount = request.form['amount']
        rate_type = request.form['type']

        new_rate = Rate(
            amount=amount,
            type=rate_type
        )

        db.session.add(new_rate)
        db.session.commit()

        flash('Тариф успешно добавлен!', 'success')
        return redirect(url_for('rates.get_rates'))

    return render_template('add_rate.html')


@rates_bp.route('/rates/edit/<int:rate_id>', methods=['GET', 'POST'])
def edit_rate(rate_id):
    rate = Rate.query.get_or_404(rate_id)

    if request.method == 'POST':
        rate.amount = request.form['amount']
        rate.type = request.form['type']

        db.session.commit()
        flash('Тариф успешно обновлен!', 'success')
        return redirect(url_for('rates.get_rates'))

    return render_template('edit_rate.html', rate=rate)


@rates_bp.route('/rates/delete/<int:rate_id>', methods=['POST'])
def delete_rate(rate_id):
    rate = Rate.query.get_or_404(rate_id)
    db.session.delete(rate)
    db.session.commit()

    flash('Тариф успешно удален!', 'success')
    return redirect(url_for('rates.get_rates'))
