from blog import db, login_manager
from sqlalchemy.sql import func
from flask_login import UserMixin



@login_manager.user_loader 
def load_user(user_id): 
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    join_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    username = db.Column(db.String(30), nullable=False, unique=False)
    email = db.Column(db.String(120), nullable=False, unique=True) 
    password = db.Column(db.String(60), nullable=False) 
    is_admin = db.Column(db.Boolean,nullable=False, default=False) 

    articles = db.relationship("Article", backref="user", lazy=True) 
    stripe_customer = db.relationship("StripeCustomer", backref="user") 
    likes = db.relationship("Like", backref="user", passive_deletes=True) 


    def __repr__(self):
        return f"User('{self.username}'. '{self.email}')"
    

