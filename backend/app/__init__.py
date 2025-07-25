from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    db.init_app(app)
    
    from routes.notes import notes
    app.register_blueprint(notes)
    
    return app