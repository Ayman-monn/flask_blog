from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from blog.config import DevelopmentCfg, ProductionCfg 


"""Enable for Development model"""
cfg = DevelopmentCfg()
"""Enable for Production model"""
# cfg = ProductionCfg()

bcrypt = Bcrypt() 
db = SQLAlchemy()
migrate = Migrate() 
seeder = FlaskSeeder() 

def create_app(): 
    global app 
    app = Flask(__name__, template_folder=cfg.VIEWS_DIR, static_folder=cfg.STATIC_DIR)
    app.config.from_object(cfg) 

    with app.app_context(): 
        register_extention(app) 
        # routes 
        register_blueprints(app) 
        app.before_first_request(populate_database) 
    return app 

def register_extention(app): 
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db) 
    seeder.init_app(app, db) 
    return None 

def register_blueprints(app): 
    from blog.routes.MainRouter import MainRouter 
    from blog.routes.ArticleRouter import ArticleRouter
    from blog.routes.AuthRouter import AuthRouter
    from blog.routes.SubscribeRouter import SubscribeRouter
    app.register_blueprint(MainRouter) 
    app.register_blueprint(ArticleRouter) 
    app.register_blueprint(AuthRouter) 
    app.register_blueprint(SubscribeRouter)  
    return None 



from blog.models.AuthModel import User
from blog.models.ArticleModel import Article
from blog.models.SubscribeModel import StripeCustomer
from blog.models.LikeModel import Like 
def populate_database(): 
    db.create_all() 
    if not User.query.filter_by(username=cfg.OWNER_USERNAME).first(): 
        user = User(
            username=cfg.OWNER_USERNAME,
            email=cfg.OWNER_EMAIL,
            password=bcrypt.generate_password_hash(cfg.OWNER_PASSWORD).decode("utf-8"),
            is_admin=True
        )
        db.session.add(user) 
        db.session.commit() 
