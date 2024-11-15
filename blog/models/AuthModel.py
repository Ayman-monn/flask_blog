from blog import db 
from sqlalchemy.sql import func

class User(db.Model): 
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
    

