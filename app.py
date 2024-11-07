from flask import Flask
from models.model import db
from routes.organizations_routes import organizations_bp
from routes.locations_routes import locations_bp
from routes.users_routes import users_bp
from routes.cars_routes import cars_bp
from routes.rates_routes import rates_bp
from routes.deals_routes import deals_bp
from routes.index_routes import index_bp


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://glebatron:glebatron@localhost/glebatron'
    app.secret_key = 'glebatron'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(index_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(organizations_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(rates_bp)
    app.register_blueprint(cars_bp)
    app.register_blueprint(deals_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
