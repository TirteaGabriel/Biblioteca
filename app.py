from flask import Flask
from routes import app_routes
from models import db
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)  # AICI E UNICUL LOC
app.register_blueprint(app_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
