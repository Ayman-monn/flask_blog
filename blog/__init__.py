from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from blog.config import DevelopmentCfg, ProductionCfg 


"""Enable for Development model"""
cfg = DevelopmentCfg()
"""Enable for Production model"""
# cfg = ProductionCfg()

bcrypt = Bcrypt() 
db = SQLAlchemy()
migrate = Migrate() 


def create_app(): 
    app = Flask(__name__, template_folder=cfg.VIEWS_DIR, static_folder=cfg.STATIC_DIR)
    app.config.from_object(cfg) 

    with app.app_context(): 
        bcrypt.init_app(app)
        db.init_app(app)
        migrate.init_app(app, db) 
    # routes 
    from blog.routes.MainRouter import MainRouter 
    from blog.routes.ArticleRouter import ArticleRouter
    from blog.routes.AuthRouter import AuthRouter
    from blog.routes.SubscribeRouter import SubscribeRouter
    app.register_blueprint(MainRouter) 
    app.register_blueprint(ArticleRouter) 
    app.register_blueprint(AuthRouter) 
    app.register_blueprint(SubscribeRouter)  

    return app 


from blog.models.AuthModel import User
from blog.models.ArticleModel import Article
from blog.models.SubscribeModel import StripeCustomer
from blog.models.LikeModel import Like 
