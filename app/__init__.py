# app/__init__.py
from flask import Flaskfrom, flask_sqlalchemy 
import SQLAlchemyfrom, flask_migrate 
import Migratefrom, flask_uploads 
import configure_uploads, UploadSet, ALLfrom, config 
import Config

db = SQLAlchemy()
migrate = Migrate()
videos = UploadSet('videos', ALL)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    configure_uploads(app, videos)
    
    from app import views
    app.register_blueprint(views.bp)

    return app